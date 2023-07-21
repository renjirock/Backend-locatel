from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import RegisterSerializer
from rest_framework import generics
from django.contrib.auth.models import User


class Logout(APIView):
    def get(self, request, format= None):
        request.user.auth_token.delete()
        return Response(status= status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
