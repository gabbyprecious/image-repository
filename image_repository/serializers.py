import django.contrib.auth.password_validation as validators
from django.contrib.auth import get_user_model
from django.core import exceptions
from rest_framework import serializers
from rest_framework.serializers import ImageField, DecimalField
from image_repository.models import Image

User = get_user_model()

class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)

    def validate_email(self, email):
        """
        Raises exception if email already exist
        :return:
        """
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                raise serializers.ValidationError("user with that email already exists")
        except User.DoesNotExist:
            return email
        return email

    def create(self, validated_data):
        """
        Create the user at DB level
        :param validated_data:
        :return:
        """
        email = validated_data.get("email")
        username = validated_data.get("username")
        password = validated_data.get("password")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )

class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(trim_whitespace=False)
    username = serializers.CharField()


class LoginMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    username = serializers.CharField()
    success = serializers.BooleanField()

class ImageSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    uploaded_by = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    # type_of_document =  serializers.ChoiceField(choices=DOCUMENT_TYPE.CHOICES)
    class Meta:
        model = Image
        fields = [
            "id",
            "owner",
            "uploaded_by",
            "image",
            'description',
            'price'
        ]
