from random import randrange
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from bankAccount.models import BankAccount
from deposits.models import Deposits
from withdraw.models import Withdraws


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'balance': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        bank = BankAccount.objects.create(
            user=user,
            balance=1000000,
            number_account=randrange(1000000, 9999999)
        )
        bank.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('balance', 'number_account')


class DepositsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposits
        fields = ('value', 'number_account', 'reference', 'bank', 'created_at')


class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraws
        fields = ('value', 'created_at')

