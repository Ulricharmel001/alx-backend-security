from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from .serializers import UserSignupSerializer, UserLoginSerializer

# Signup API
@method_decorator(ratelimit(key='ip', rate='5/m', method='POST'), name='post')
class SignupAPI(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # Check if the request has been rate limited
        if getattr(request, 'limited', False):
            return Response(
                {"error": "Rate limit exceeded. Please try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        return super().post(request, *args, **kwargs)


# Login API
@method_decorator(ratelimit(key='ip', rate='10/m', method='POST'), name='post')
class LoginAPI(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Check if the request has been rate limited
        if getattr(request, 'limited', False):
            return Response(
                {"error": "Rate limit exceeded. Please try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        return Response({
            "username": user.username,
            "email": user.email,
            "message": "Login successful"
        })
