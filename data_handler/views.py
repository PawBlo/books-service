from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .models import Entry, Book, UserBook
from .serializers import EntrySerializer, BookSerializer,UserBookSerializer
from .service import Scraper

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

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_book(request):
    user = request.user
    isbn = request.data.get("isbn")
    isbn_book = Book.objects.filter(isbn = isbn).first()
    
    if isbn_book:
        print(isbn_book)
        serializer = BookSerializer(isbn_book)
        UserBook.objects.create(user=user,
                                       book=isbn_book,
                                       is_for_sale = False,
                                       condition = 'new')
        return Response({"exists": True, "book" : serializer.data}, status=status.HTTP_200_OK)
    else:
        print("isbn book:", isbn_book)
        print("isbn",  isbn)
        s = Scraper(isbn)
        img, title, author = s.get_info()
        Book.objects.create(title = title, author=author, cover_image = img, isbn =isbn  )
        isbn_book = Book.objects.filter(isbn = isbn).first()
        UserBook.objects.create(user=user,
                                       book=isbn_book,
                                       is_for_sale = False,
                                       condition = 'new')
        serializer = BookSerializer(isbn_book)
        return Response({"exists": True, "book" : serializer.data}, status=status.HTTP_200_OK)
        



