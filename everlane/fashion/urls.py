from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', CartView.as_view(), name='view-cart'),
    path('cart/remove/<int:pk>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('order/place/', PlaceOrderView.as_view(), name='place-order'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('login/', LoginView.as_view(), name='login')
]
