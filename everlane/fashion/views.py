from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserRegistrationSerializer(user).data,
                "message": "User registered successfully."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Login view

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Generate or get an existing token for the user
            
        return Response({
            'status': "failed",
            'message': 'Invalid username or password.',
            'response_code': status.HTTP_400_BAD_REQUEST,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)





from rest_framework import generics
from .models import User, Product, Order, Category, Subcategory
from .serializers import *

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        categories = self.get_queryset()
        serializer = self.get_serializer(categories, many=True)
        response_data = {
            'status': 'success',
            'message': 'Categories retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }
        return Response(response_data)



class SubcategoryListView(generics.ListCreateAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

class SubcategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class WishlistListView(generics.ListCreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

class WishlistDetailView(generics.RetrieveDestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class CartListView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartDetailView(generics.RetrieveDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        return Response({'status': 'success', 'message': 'Item added to cart'}, status=status.HTTP_200_OK)
