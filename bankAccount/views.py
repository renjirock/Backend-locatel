from rest_framework import status, generics, request as rf_request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from api.serializers import UserSerializer, AccountSerializer
from bankAccount.models import BankAccount


class Account(APIView):

    def get(self, rf_request, format=None):
        try:
            queryset = User.objects.get(pk=rf_request.user.id)
            user = UserSerializer(queryset)

            return Response({'user': user.data, 'error': False}, status=status.HTTP_200_OK)

        except:
            return Response({'error': True}, status=status.HTTP_404_NOT_FOUND)

    def put(self, rf_request, format=None):
        try:
            User.objects.filter(pk=rf_request.user.id).update(
                email=rf_request.data['email'],
                first_name=rf_request.data['first_name'],
                last_name=rf_request.data['last_name']
            )

            return Response({'save': True, 'error': False}, status=status.HTTP_200_OK)

        except:
            return Response({'error': True}, status=status.HTTP_404_NOT_FOUND)


class Balance(APIView):

    def get(self, rf_request):
        try:
            queryset = BankAccount.objects.get(user_id=rf_request.user.pk)
            account = AccountSerializer(queryset)
            return Response(account.data, status=status.HTTP_200_OK)

        except:
            return Response({'error': True}, status=status.HTTP_404_NOT_FOUND)
