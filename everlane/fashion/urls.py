from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('order/place/', PlaceOrderView.as_view(), name='place-order'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
]
