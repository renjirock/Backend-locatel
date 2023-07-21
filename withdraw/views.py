import random
import datetime
from rest_framework import status, request as rf_request
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from api.serializers import WithdrawSerializer
from bankAccount.models import BankAccount
from withdraw.models import Withdraws
from rest_framework import generics
from django.utils import timezone
# Create your views here.


class Withdraw(APIView):
    def post(self, rf_request):
        try:
            user = User.objects.get(pk=rf_request.user.pk)
            withdraw = Withdraws.objects.create(
                user=user,
                value=rf_request.data['value'],
                token=random.randrange(100000, 999999)
            )
            balance = BankAccount.objects.get(user_id=rf_request.user.pk)
            if int(balance.balance) - int(rf_request.data['value']) > 0:
                withdraw.save()
                return Response({'token': withdraw.token, 'error': False}, status=status.HTTP_200_OK)
            else:
                Response({'token': False, 'error': True}, status=status.HTTP_200_OK)
        except:
            return Response({'error': True}, status=status.HTTP_404_NOT_FOUND)

    def get(self, rf_request):
        try:
            querysets = Withdraws.objects.filter(user_id=rf_request.user.id).order_by('-created_at')
            withdraws = []
            for queryset in querysets:
                deposit = WithdrawSerializer(queryset)
                withdraws.append(deposit.data)

            return Response({'withdraws': withdraws, 'error': False}, status=status.HTTP_200_OK)
        except:
            return Response({'error': True}, status=status.HTTP_404_NOT_FOUND)


class ConfirmWithdraw(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def get(self, rf_request):
        try:
            withdraw = Withdraws.objects.get(token=rf_request.query_params['token'])
            if withdraw.created_at + datetime.timedelta(hours=0.5) > timezone.now():
                balance = BankAccount.objects.get(user_id=withdraw.user_id)
                balance.balance = int(balance.balance) - int(withdraw.value)
                balance.save()
                withdraw.delete()
                return Response({'withdraw': True, 'error': False}, status=status.HTTP_200_OK)
            else:
                withdraw.delete()
                return Response({'withdraw': False, 'error': True}, status=status.HTTP_200_OK)

        except OSError:
            return Response({'error': True}, status=status.HTTP_404_NOT_FOUND)
