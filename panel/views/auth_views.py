from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from ..models import User  # Import directly from your models

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True}
        }

    def create(self, validated_data):
        """
        Create and return a new user instance, given the validated data.
        """
        # Use the custom create_user method from UserManager
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class SignupAPIView(APIView):
    """
    API endpoint for user signup.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user signup.
        """
        serializer = UserSignupSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully',
                'user_id': str(user.id),
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CustomLoginAPIView(APIView):
    """
    API endpoint for user login with email and password.
    Returns an authentication token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user login.
        """
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({
                'error': 'Please provide both email and password'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate using email
        user = authenticate(request, username=email, password=password)

        if user:
            # Get or create token for the user
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user_id': str(user.id),
                'email': user.email,
            }, status=status.HTTP_200_OK)

        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)