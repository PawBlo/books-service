from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([AllowAny])  # Użytkownicy niezalogowani mogą się rejestrować
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Tworzenie użytkownika
    user = User.objects.create_user(username=username, password=password)
    user.save()
    
    # Tworzenie tokena
    token, created = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])  # Użytkownicy niezalogowani mogą się logować
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()

    if user and user.check_password(password):
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])  # Użycie tokenu lub sesji do uwierzytelnienia
@permission_classes([IsAuthenticated])  # Dostęp tylko dla zalogowanych użytkowników
def secured_view(request):
    return Response({'message': 'You are authenticated!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])  # Użycie tokenu lub sesji do uwierzytelnienia
@permission_classes([IsAuthenticated])  # Dostęp tylko dla zalogowanych użytkowników
def logout(request):
    user = request.user
    try:
        token = Token.objects.get(user=user)
        token.delete()
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'error': 'Token does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

