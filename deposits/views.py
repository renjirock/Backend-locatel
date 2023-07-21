from rest_framework import status, request as rf_request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from api.serializers import DepositsSerializer
from deposits.models import Deposits as Deposit
from bankAccount.models import BankAccount
import random
import string

# Create your views here.


class Deposits(APIView):

    def post(self, rf_request):
        try:
            user = User.objects.get(pk=rf_request.user.id)
            deposit = Deposit.objects.create(
                user=user,
                number_account=rf_request.data['number_account'],
                value=rf_request.data['value'],
                bank=rf_request.data['bank'],
                reference=''.join(random.choice(string.ascii_lowercase) for i in range(3)) + str(random.randrange(10000,99999))
            )
            balance = BankAccount.objects.get(user_id=rf_request.user.pk)
            if int(balance.balance) - int(rf_request.data['value']) > 0:
                deposit.save()
                balance.balance = int(balance.balance) - int(rf_request.data['value'])
                balance.save()
                return Response({'save': True, 'error': False}, status=status.HTTP_200_OK)

            else:
                Response({'save': False, 'error': True}, status=status.HTTP_200_OK)

        except:
            return Response({'error': True}, status= status.HTTP_404_NOT_FOUND)

    def get(self, rf_request):
        try:
            querysets = Deposit.objects.filter(user_id=rf_request.user.id).order_by('-created_at')
            deposits = []
            for queryset in querysets:
                deposit = DepositsSerializer(queryset)
                deposits.append(deposit.data)

            return Response({'deposit': deposits, 'error': False}, status=status.HTTP_200_OK)
        except:
            return Response({'error': True}, status=status.HTTP_404_NOT_FOUND)
