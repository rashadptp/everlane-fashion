from django.urls import path
from .views import *

urlpatterns = [
     ##################################    REGISTRATION   ##############################################################
    path('register/', RegisterUserView.as_view(), name='register'),
    path('register/admin/', RegisterAdminView.as_view(), name='admin-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('forgot-username/', ForgotUsernameView.as_view(), name='forgot-username'),

    ######################################   PRODUCTS    ######################################################################
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products-paginated/', ProductPaginatedListView.as_view(), name='products-paginated'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('subcategories/', SubcategoryListView.as_view(), name='subcategory-list'),
    path('products/trending/', TrendingProductsView.as_view(), name='trending-products'),
    path('products/summer/', SeasonalProductsView.as_view(), {'season': 'summer'}, name='summer-products'),
    path('products/winter/', SeasonalProductsView.as_view(), {'season': 'winter'}, name='winter-products'),
    path('products/rainy/', SeasonalProductsView.as_view(), {'season': 'rainy'}, name='rainy-products'),
    path('products/autumn/', SeasonalProductsView.as_view(), {'season': 'autumn'}, name='autumn-products'),
    path('add-product-item/', AddProductItemView.as_view(), name='add-product-item'),


    ######################################    ORDERS    ######################################################################
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('place-order/', PlaceOrderView.as_view(), name='place-order'),
    path('update-order-status/<int:order_id>/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('cancel-order-item/<int:order_item_id>/', CancelOrderView.as_view(), name='cancel-order-item'),
    path('request-return/', RequestReturnView.as_view(), name='request-return'),
    path('process-return/', ProcessReturnView.as_view(), name='process-return'),
    path('return-pending/', ReturnPendingView.as_view(), name='return-pending'),
    path('completed-orders/',CompletedOrdersView.as_view(),name='completed-orders'),


    #################################      CARTS      ########################################################################
    path('carts/', CartListView.as_view(), name='cart-list'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('update-cart-item-quantity/', UpdateCartItemQuantityView.as_view(), name='update-cart-item-quantity'),
    path('cart-item/<int:item_id>/delete/', CartItemDeleteView.as_view(), name='cart-item-delete'),
    
    ##########################################  BANNERS  #######################################################
    path('banners/', AngularBannerListView.as_view(), name='banner-list'),
    path('bannerss/', FlutterBannerListView.as_view(), name='banner-list'),


    ##############################################  RECOMMENDATIONS  #########################################
    path('questionnaire/', QuestionnaireCreateView.as_view(), name='questionnaire'),
    path('recommendations/', RecommendationAPIView.as_view(), name='recommendations'),



    ############################################    WISHLIST   #################################################
    path('wishlist/', WishlistListView.as_view(), name='wishlist'),
    path('wishlist/add/', AddWishlistView.as_view(), name='add-wishlist'),
    path('wishlist/delete/<int:product_id>/', DeleteWishlistView.as_view(), name='delete-wishlist'),


    ############################################  ADDRESS #######################################################
    path('addresses/default/', DefaultAddressView.as_view(), name='default-address'),
    path('addresses/', AddressListView.as_view(), name='address-list'),
    path('addresses/create/', AddressCreateView.as_view(), name='address-create'),
    path('addresses/<int:pk>/delete/', AddressDeleteView.as_view(), name='address-delete'),
    

    ########################################## PROFILE ########################################################
    path('profile/', UserProfileView.as_view(), name='user-profile-detail'), 
    path('profile/update/',ProfileUpdateView.as_view(), name='user-profile-update'),
    path('profile/change-password/',PasswordChangeView.as_view(), name='change-password'),
    
    ########################################   PAYMENT  ##########################################################
    path('payment/execute/', ExecutePaymentView.as_view(), name='payment-execute'),
    path('payment/cancel/', CancelPaymentView.as_view(), name='payment-cancel'),
    path('notification/', UserNotificationsAPIView.as_view(), name='notification'),
    path('notification/<int:pk>/delete/', NotificationDeleteView.as_view(), name='notification-delete'),

    
    
    #######################################  DONATIONS      #############################

    path('disasters/', DisasterListCreateView.as_view(), name='disaster-list-create'),
    path('disasters/approve/<int:disaster_id>/', ApproveDisasterView.as_view(), name='disaster-approve'),
    path('disasters/pending/', AdminDisasterApprovalListView.as_view(), name='admin-disaster-approval-list'),
    path('donations/', DressDonationCreateView.as_view(), name='dress-donation-create'),
    path('user-donations/', UserDonationListView.as_view(), name='user-donation-list'),
    path('disasters/<int:disaster_id>/donations/', DisasterDonationsView.as_view(), name='disaster-donations'),
    path('my-disasters/', UserDisastersView.as_view(), name='user-disasters'),
    path('pickups/',PickupListView.as_view(),name='pickup-list'),
     
    

    






]
    


    
    
    

