from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),



    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('subcategories/', SubcategoryListView.as_view(), name='subcategory-list'),
    path('subcategories/<int:pk>/', SubcategoryDetailView.as_view(), name='subcategory-detail'),
    path('wishlists/', WishlistListView.as_view(), name='wishlist-list'),
    path('wishlists/<int:pk>/', WishlistDetailView.as_view(), name='wishlist-detail'),
    path('carts/', CartListView.as_view(), name='cart-list'),
    path('carts/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    
    
]
