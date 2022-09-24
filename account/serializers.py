
from rest_framework import serializers

from account.models import Account
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Account
        fields = ['first_name','last_name', 'email', 'password','user_type']

    def is_valid(self, *, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)
    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Account
        fields = ['token']

