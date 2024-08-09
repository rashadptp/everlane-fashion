from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('register/admin/', RegisterAdminView.as_view(), name='admin-register'),
    path('login/', LoginView.as_view(), name='login'),



    # path('users/', UserListView.as_view(), name='user-list'),
    # path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('request-return/', RequestReturnView.as_view(), name='request-return'),
    path('process-return/', ProcessReturnView.as_view(), name='process-return'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('subcategories/', SubcategoryListView.as_view(), name='subcategory-list'),
    path('subcategories/<int:pk>/', SubcategoryDetailView.as_view(), name='subcategory-detail'),
    path('carts/', CartListView.as_view(), name='cart-list'),
    # path('carts/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('update-cart-item-quantity/', UpdateCartItemQuantityView.as_view(), name='update-cart-item-quantity'),
    path('cart-item/<int:item_id>/delete/', CartItemDeleteView.as_view(), name='cart-item-delete'),
    path('place-order/', PlaceOrderView.as_view(), name='place-order'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('update-order-status/<int:order_id>/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('banners/', AngularBannerListView.as_view(), name='banner-list'),
    path('bannerss/', FlutterBannerListView.as_view(), name='banner-list'),
    path('products/trending/', TrendingProductsView.as_view(), name='trending-products'),
    path('products/summer/', SeasonalProductsView.as_view(), {'season': 'summer'}, name='summer-products'),
    path('products/winter/', SeasonalProductsView.as_view(), {'season': 'winter'}, name='winter-products'),
    path('products/rainy/', SeasonalProductsView.as_view(), {'season': 'rainy'}, name='rainy-products'),
    path('products/autumn/', SeasonalProductsView.as_view(), {'season': 'autumn'}, name='autumn-products'),
    path('questionnaire/', QuestionnaireCreateView.as_view(), name='questionnaire'),
    path('wishlist/', WishlistListView.as_view(), name='wishlist'),
    path('wishlist/add/', AddWishlistView.as_view(), name='add-wishlist'),
    path('wishlist/delete/<int:pk>/', DeleteWishlistView.as_view(), name='delete-wishlist'),
    path('addresses/default/', DefaultAddressView.as_view(), name='default-address'),
    path('addresses/', AddressListView.as_view(), name='address-list'),
    path('addresses/create/', AddressCreateView.as_view(), name='address-create'),
    path('addresses/<int:pk>/delete/', AddressDeleteView.as_view(), name='address-delete'),
    path('recommendations/', RecommendationAPIView.as_view(), name='recommendations'),
    # path('search/', ProductSearchAPIView.as_view(), name='product-search'),
    






]
    


    
    
    

