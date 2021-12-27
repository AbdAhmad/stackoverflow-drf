from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer

from rest_framework import viewsets, permissions, generics, serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):

    username = request.data['username']
    password = request.data['password']
    confirmPassword = request.data['confirmPassword']

    if User.objects.filter(username=username).exists():
        return Response({'username': 'Username already taken'})

    if len(password) < 8:
        return Response({'password': 'Password is too short'})

    if password.isdigit():
        return Response({'password': 'Password cannot be entirely numeric'})

    if password != confirmPassword:
        return Response({'password': 'Two passwords do not match'})


    # user = User.objects.create(username=username, password=password)
    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()
    return Response({'success': 'User Created'})

    # serializer = UserSerializer(data=user, many=False)

    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data)

    # if not serializer.is_valid():
    #     return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})


# class Register(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]


# @api_view(['POST'])
# def login_user(request):

#     username = request.data['username']
#     password = request.data['password']

#     user = authenticate(username=username, password=password)

#     if user is not None:
#         login(request, user)
#         return Response({'status': 200, 'message': "Welcome " + username})
#     else:
#         return Response({"status" : 404, "message": "wrong credentials"})


@api_view(['GET'])
def logout_user(request):
    logout(request)
    return Response({"message": "User logged out"})