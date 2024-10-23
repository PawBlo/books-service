from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .models import Entry, Book, UserBook
from .serializers import EntrySerializer, BookSerializer,UserBookSerializer
from .service import Scraper
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_book(request):
    serializer = EntrySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_entries(request):
    entries = Entry.objects.filter(user=request.user)
    serializer = EntrySerializer(entries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_book_to_user(request):
    user = request.user
    isbn = request.data.get("isbn")

    try:
        book = Book.objects.get(isbn=isbn)
    except Book.DoesNotExist:
        return Response({'error' : 'Book not found'},status=status.HTTP_400_BAD_REQUEST )
    if UserBook.objects.filter(user=user, book=book).exists():
        return Response({'error': 'User already has this book'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_book  = UserBook.objects.create(user=user,
                                       book=book,
                                       is_for_sale = False,
                                       condition = 'new')
    serializer = UserBookSerializer(user_book )
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_books(request):
    user = request.user
    books = UserBook.objects.filter(user=user)
    
    serializer = UserBookSerializer(books, many=True)
    for data in serializer.data:
        print(data)
        data.pop('user')
    return Response(serializer.data, status=200)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_books(request):
    user = request.user
    books = UserBook.objects
    
    # Serializowanie wielu obiektów wymaga many=True
    serializer = UserBookSerializer(books, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_book(request):
    user = request.user
    isbn = request.data.get("isbn")

    # Pobranie obrazów z request.FILES
    front_image = request.FILES.get('front_image')
    back_image = request.FILES.get('back_image')

    # Sprawdzenie, czy książka istnieje w bazie
    isbn_book = Book.objects.filter(isbn=isbn).first()

    # Jeśli książka już istnieje
    if isbn_book:
        # Zapisanie zdjęć użytkownika do UserBook
        user_book = UserBook.objects.create(
            user=user,
            book=isbn_book,
            is_for_sale=False,
            condition='new',
        )
        
        if front_image:
            front_image_name = f"front_{isbn}_{user.username}.jpg"
            front_image_path = default_storage.save(f'user_books/front_images/{front_image_name}', ContentFile(front_image.read()))
            user_book.front_image = front_image_path  # Zapisanie ścieżki do pliku w bazie

        if back_image:
            back_image_name = f"back_{isbn}_{user.username}.jpg"
            back_image_path = default_storage.save(f'user_books/back_images/{back_image_name}', ContentFile(back_image.read()))
            user_book.back_image = back_image_path  # Zapisanie ścieżki do pliku w bazie

        user_book.save()

        # Serializacja i odpowiedź
        serializer = BookSerializer(isbn_book)
        UserBook.objects.create(user=user,
                                       book=isbn_book,
                                       is_for_sale = False,
                                       condition = 'new')
        return Response({"exists": True, "book" : serializer.data}, status=status.HTTP_200_OK)
    else:
        s = Scraper(isbn)
        img, title, author = s.get_info()

        isbn_book = Book.objects.create(title=title, author=author, cover_image=img, isbn=isbn)

        user_book = UserBook.objects.create(
            user=user,
            book=isbn_book,
            is_for_sale=False,
            condition='new',
        )

        if front_image:
            front_image_name = f"front_{isbn}_{user.username}.jpg"
            front_image_path = default_storage.save(f'user_books/front_images/{front_image_name}', ContentFile(front_image.read()))
            user_book.front_image = front_image_path

        if back_image:
            back_image_name = f"back_{isbn}_{user.username}.jpg"
            back_image_path = default_storage.save(f'user_books/back_images/{back_image_name}', ContentFile(back_image.read()))
            user_book.back_image = back_image_path

        user_book.save()

        serializer = BookSerializer(isbn_book)
        return Response({"exists": True, "book" : serializer.data}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_latest_books(request):
    recent_books = UserBook.objects.order_by('-created_at')[:5]
    serializer = UserBookSerializer(recent_books, many=True)
    return Response({'latest_books' : serializer.data}, status=status.HTTP_200_OK)

        

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_users_with_book(request):
    search_query = request.query_params.get('searchQuery')
    
    if not search_query:
        return Response({'error': 'Search query is required'}, status=status.HTTP_400_BAD_REQUEST)

    books = Book.objects.filter(title__iregex=fr'\b{search_query}.*')

    if not books.exists():
        return Response({'error': 'No books found matching the search query'}, status=status.HTTP_404_NOT_FOUND)

    user_books = UserBook.objects.filter(book__in=books).select_related('user', 'book')

    if not user_books.exists():
        return Response({'message': 'No users found with the specified books'}, status=status.HTTP_404_NOT_FOUND)

    result = []
    for user_book in user_books:
        result.append({
            'user': user_book.user.username,
            'title': user_book.book.title, 
            'isbn': user_book.book.isbn,
            'condition': user_book.condition,
            'is_for_sale': user_book.is_for_sale,
            'cover_image': request.build_absolute_uri(user_book.book.cover_image.url) if user_book.book.cover_image else None,
        })

    return Response({'results': result}, status=status.HTTP_200_OK)

