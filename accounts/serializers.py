import logging
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from .models import User
logger = logging.getLogger(__name__)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validates user credentials and generates JWT tokens.
        """
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        try:
            user = authenticate(username=email, password=password)

            if not user:
                raise serializers.ValidationError('Invalid email or password.')

            if not user.is_active:
                raise serializers.ValidationError("User account is inactive.")

            # Update last login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

            # Generate tokens
            refresh = RefreshToken.for_user(user)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'phone': user.phone,
                    # 'user_type': user.user_type,
                }
            }
        except Exception as e:
            logger.error(f"Login failed: {str(e)}", exc_info=True)
            raise serializers.ValidationError("Login process failed. Please try again.")
        

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = [
            'email', 'name', 'phone', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        try: 
            password = validated_data.pop('password')
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user
        
        except Exception as e:
            logger.error(f"User creation failed: {str(e)}", exc_info=True)
            raise serializers.ValidationError("Failed to create user.")