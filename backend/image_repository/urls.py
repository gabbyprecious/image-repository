from django.urls import path

from image_repository.views.user_auth import SignUpView, LoginView
from image_repository.views.image_views import ImageViewset, BuyImageView

urlpatterns = [
    path("users/signup", SignUpView.as_view({"post": "create"}), name="signup"),
    path("users/login", LoginView.as_view({"post": "login"}), name="login"),
    path("users/add_image", ImageViewset.as_view({"post": "create"}), name="add_image"),
    path("users/buy_image", BuyImageView.as_view({"post": "buy_image"}), name="buy_image"),
]