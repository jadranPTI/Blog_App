from django.shortcuts import render
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt import authentication
from rest_framework import generics 
from .serializers import UserLoginSerializer, UserCreateSerializer
# from .permissions import IsAdminUserType
from .models import User


logger = logging.getLogger(__name__)
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"User login failed: {str(e)}", exc_info=True)
            return Response({"detail": "Login failed. Please check your credentials."}, status=status.HTTP_400_BAD_REQUEST)



class UserCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            serializer = UserCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            print(user)
            return Response(
                {
                    'message': 'User created successfully.',
                    'user': {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "phone": user.phone,
                        # "user_type": user.user_type,
                    },
                },status=status.HTTP_200_OK
            )
        
        except Exception as e:
            logger.error(f"User creation failed: {str(e)}", exc_info=True)
            return Response({"detail": "User creation failed. Please check the provided data"}, status=status.HTTP_400_BAD_REQUEST)