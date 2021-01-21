import stripe
import environ
from cloudinary import uploader

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from image_repository.models import Image, Sales
from image_repository.serializers import ImageSerializer

from image_repo.settings import env

stripe.api_key = env("STRIPE_API_KEY")

class ImageViewset(ModelViewSet):
    model = Image
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data["uploaded_by"] = user.id
        serializer.initial_data["owner"] = user.id
        serializer.is_valid(raise_exception=True)
        image = uploader.upload(request.data["image"], folder="Stock Image")
        serializer.save(owner=user, uploaded_by=user, image=image["secure_url"])
        
        return Response( 
            {
                "success": True,
                "message": "User has upload a picture",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    
    def update(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass

class BuyImageView(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def buy_image(self, request):
        image = Image.objects.get(id=request.data["image"])
        try:
            pay = stripe.PaymentIntent.create(
                amount=image.price, currency='usd', 
                payment_method_types=['card'],
                receipt_email=request.user.email,
            )
            sales = Sales.objects.create(seller=image.owner,
                                        buyer=request.user,
                                        image=image,
                                    )
            image.owner = sales.buyer
            image.save()
            return Response( 
            {
                "success": True,
                "message": "User has bought an image",
                "data": {"payment_id": pay.id, "buyer": sales.buyer.email, "seller": sales.seller.email} 
            },
            status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response( 
            {
                "success": False,
                "message": "An error occured when buying image, retry",
                "data": str(e),
            },
            status=status.HTTP_403_FORBIDDEN,
            )