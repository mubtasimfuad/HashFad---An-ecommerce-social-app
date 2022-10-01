
from os import access
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

from account.models import Account, ActivatorKey
from django.contrib.auth.password_validation import validate_password


class SignUpSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Account
        fields = ['first_name','last_name', 'email', 'password',"confirm_password",'user_type']
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs
   
    def create(self, validated_data):
        validated_data.pop('confirm_password') 
        return Account.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Account
        fields = ['token']

class EmailActivationSerializer(serializers.ModelSerializer):
    activation_key = serializers.CharField()

    def validate_activation_key(self, activation_key):
        if not len(activation_key)==10:
            raise serializers.ValidationError("Wrong Key")
        return activation_key

    class Meta:
        model = ActivatorKey
        fields = ['activation_key']

class SignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=5)
    password = serializers.CharField(write_only=True)
    tokens = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ["email","password","tokens"]
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account is not verified')
       
        return {
            'email': user.email,
            'tokens': user.tokens,
        }

        return attrs


