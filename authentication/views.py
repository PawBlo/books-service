from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password


@api_view(['POST'])
@permission_classes([AllowAny])  # Użytkownicy niezalogowani mogą się rejestrować
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    if len(username) < 5:
        return Response({'error' : 'Invalid username'},status=status.HTTP_400_BAD_REQUEST)
    if len(password) < 5:
        return Response({'error' : 'Invalid password'},status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.create_user(username=username, password=password, email = email)
        user.save()
    except:
        return Response({'error' : 'username exists'},status=status.HTTP_400_BAD_REQUEST)
    
    # Tworzenie tokena
    token, created = Token.objects.get_or_create(user=user)

    return Response({'token': token.key,'username': username, 'email' : email}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])  # Użytkownicy niezalogowani mogą się logować
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()

    if user and user.check_password(password):
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username' : username, 'email' : user.email}, status=status.HTTP_200_OK)

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

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    new_password = request.data.get('new_password')
    old_password = request.data.get('old_password')
    if len(new_password) <5:
        return Response({'error': 'Invalid new password'}, status=status.HTTP_400_BAD_REQUEST)
    if not check_password(old_password, user.password):
           return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user.set_password(new_password)
        user.save()
        Token.objects.filter(user=user).delete()
        new_token, created = Token.objects.get_or_create(user=user)

        return Response({'message': 'Changed password successfully.', 'token' : new_token.key}, status=status.HTTP_200_OK) 
    except:
        return Response({'error': 'Invalid new password'}, status=status.HTTP_400_BAD_REQUEST)
    