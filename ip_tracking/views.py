from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSignupSerializer, UserLoginSerializer

# Signup API
class SignupAPI(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]


# Login API
class LoginAPI(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # You can return a token here if you use DRF TokenAuth or JWT
        return Response({
            "username": user.username,
            "email": user.email,
            "message": "Login successful"
        })
