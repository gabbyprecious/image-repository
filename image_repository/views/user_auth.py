from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from image_repository.helpers import generate_auth_token
from image_repository.serializers import SignUpSerializer, UserSerializer, UserLoginSerializer, LoginMessageSerializer

User = get_user_model()


class SignUpView(GenericViewSet):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()

    def create(self, request):
        """
        Create User,
        Send just company name, email and pass for company account
        And email, username, password, first name and last name for personal account
        (POST REQUEST)
        """

        serializer = SignUpSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": serializer.errors, "success": False}, status=status.HTTP_403_FORBIDDEN)
        user = serializer.save()

        user_serializer = UserSerializer(user)
        token = generate_auth_token(user)["access"]
        response = Response(
            {"user": user_serializer.data, "success": True},
            status=status.HTTP_201_CREATED,
        )
        response.set_cookie(
            "Authorization",
            value=f"Bearer {token}",
            httponly=True,
            max_age=settings.COOKIE_TIME,
            expires=settings.COOKIE_TIME,
            samesite="None",
            secure=settings.COOKIE_SECURE,  # Cookie is sent from client only over HTTP when flag turned on
        )
        return response

class LoginView(GenericViewSet):

    def login(self, request):
        """
        Login User and return authentication token (POST REQUEST)
        :param request:
        :return:
        """

        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": serializer.errors, "success": False}, status=status.HTTP_403_FORBIDDEN)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid Credentials", "success": False}, status=status.HTTP_401_UNAUTHORIZED)

        token = generate_auth_token(user)["access"]
        content = {
            "success": True,
            "message": "You've successfully logged in",
            "email": user.email,
        }
        serializer_content = LoginMessageSerializer(content)
        response = Response(serializer_content.data, status=status.HTTP_200_OK)
        response.set_cookie(
            "Authorization",
            value=f"Bearer {token}",
            httponly=False,
            max_age=settings.COOKIE_TIME,
            expires=settings.COOKIE_TIME,
            samesite="None",
            secure=settings.COOKIE_SECURE,  # Cookie is sent from client only over HTTP when flag turned on
        )
        return response
