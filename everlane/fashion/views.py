from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import *
from .permissions import IsAdminUser
from .serializers import *

#register view

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


class RegisterAdminView(generics.CreateAPIView):
    serializer_class = AdminRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": AdminRegistrationSerializer(user).data,
                "message": "Admin registered successfully."
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
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
                "message": "Login successful."
            }, status=status.HTTP_200_OK)
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



class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        products = self.get_queryset()
        product_data = []
        for product in products:
            product_serializer = self.get_serializer(product)
            items = ProductItem.objects.filter(product=product)
            item_serializer = ProductItemSerializer(items, many=True)
            product_data.append({
                'product': product_serializer.data,
                'items': item_serializer.data,
                'is_out_of_stock': not items.exists() or all(item.stock == 0 for item in items)
            })
        return Response({
            'status': "success",
            'message': "Products retrieved successfully.",
            'response_code': status.HTTP_200_OK,
            'data': product_data
        })

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        product_serializer = self.get_serializer(product)
        items = ProductItem.objects.filter(product=product)
        item_serializer = ProductItemSerializer(items, many=True)
        return Response({
            'status': 'success',
            'message': 'Product details retrieved successfully.',
            'response_code': 200,
            'data': {
                'product': product_serializer.data,
                'items': item_serializer.data,
                'is_out_of_stock': not items.exists() or all(item.stock == 0 for item in items)
            }
        })

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        items_data = request.data.get('items', [])
        for item_data in items_data:
            ProductItem.objects.create(product=product, **item_data)
        return Response({
            'status': "success",
            'message': "Product created successfully.",
            'response_code': status.HTTP_201_CREATED,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        items_data = request.data.get('items', [])
        for item_data in items_data:
            item_id = item_data.get('id')
            if item_id:
                item = ProductItem.objects.get(id=item_id, product=product)
                item.size = item_data.get('size', item.size)
                item.stock = item_data.get('stock', item.stock)
                item.save()
            else:
                ProductItem.objects.create(product=product, **item_data)

        return Response({
            'status': "success",
            'message': "Product updated successfully.",
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        })

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': "success",
            'message': "Product deleted successfully.",
            'response_code': status.HTTP_204_NO_CONTENT,
            'data': None
        }, status=status.HTTP_204_NO_CONTENT)

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
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return Subcategory.objects.filter(category_id=category_id)
        return Subcategory.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response({
            'status': "success",
            'message': "Subcategories retrieved successfully.",
            'response_code': status.HTTP_200_OK,
            'data': data
        })

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
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get(self, request, *args, **kwargs):
        carts = self.get_queryset()
        serializer = self.get_serializer(carts, many=True)
        return Response({
            'status': 'success',
            'message': 'Cart list retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        })

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            cart = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Cart created successfully.',
                'response_code': status.HTTP_201_CREATED,
                'data': CartSerializer(cart).data
            })
        return Response({
            'status': 'failed',
            'message': 'Failed to create cart.',
            'response_code': status.HTTP_400_BAD_REQUEST,
            'data': serializer.errors
        })

class CartDetailView(generics.RetrieveDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))  # Ensure quantity is an integer

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'status': 'failed', 'message': 'Product not found.', 'response_code': status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve or create the cart for the user
        cart, created = Cart.objects.get_or_create(user=user)

        # Retrieve or create the cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            # Item already exists in cart, update the quantity
            cart_item.quantity += quantity
            cart_item.save()
            message = 'Quantity updated for the item in cart.'
        else:
            cart_item.quantity = quantity
            cart_item.save()
            message = 'Item added to cart.'

        return Response({
            'status': 'success',
            'message': message,
            'response_code': status.HTTP_200_OK,
            'data': CartSerializer(cart).data  # Optional: Return the updated cart data
        }, status=status.HTTP_200_OK)
    
class UpdateCartItemQuantityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        cart_item_id = request.data.get('cart_item_id')
        quantity = int(request.data.get('quantity', 1))  # Ensure quantity is an integer

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=user)
        except CartItem.DoesNotExist:
            return Response({'status': 'failed', 'message': 'Cart item not found.', 'response_code': status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

        if quantity <= 0:
            cart_item.delete()
            return Response({
                'status': 'success',
                'message': 'Item removed from cart.',
                'response_code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

        cart_item.quantity = quantity
        cart_item.save()

        return Response({
            'status': 'success',
            'message': 'Quantity updated successfully.',
            'response_code': status.HTTP_200_OK,
            'data': CartSerializer(cart_item.cart).data
        }, status=status.HTTP_200_OK)



#Banner views

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Banner
from .serializers import BannerSerializer

class AngularBannerListView(generics.ListAPIView):
    serializer_class = BannerSerializer

    def get_queryset(self):
        """
        Filter the banners to only include those for Angular.
        """
        return Banner.objects.filter(is_deleted=False, is_active=True, which='A')

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for Angular banners.
        """
        banners = self.get_queryset()
        serializer = self.get_serializer(banners, many=True)

        if not banners.exists():
            response_data = {
                'status': 'failed',
                'message': 'No Angular banners found.',
                'response_code': status.HTTP_404_NOT_FOUND,
                'data': []
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'status': 'success',
            'message': 'Angular banners retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


from rest_framework import generics, status
from rest_framework.response import Response
from .models import Banner
from .serializers import BannerSerializer

class FlutterBannerListView(generics.ListAPIView):
    serializer_class = BannerSerializer

    def get_queryset(self):
        """
        Filter the banners to only include those for Flutter.
        """
        return Banner.objects.filter(is_deleted=False, is_active=True, which='F')

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for Flutter banners.
        """
        banners = self.get_queryset()
        serializer = self.get_serializer(banners, many=True)

        if not banners.exists():
            response_data = {
                'status': 'failed',
                'message': 'No Flutter banners found.',
                'response_code': status.HTTP_404_NOT_FOUND,
                'data': []
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'status': 'success',
            'message': 'Flutter banners retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)




#Trending images listing api

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class TrendingProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(is_trending=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if queryset.exists():
            return Response({
                'status': "success",
                'message': 'Trending products retrieved successfully.',
                'response_code': status.HTTP_200_OK,
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': "failed",
            'message': 'No trending products found.',
            'response_code': status.HTTP_404_NOT_FOUND,
            'data': []
        }, status=status.HTTP_404_NOT_FOUND)




#seasons filteration api


from rest_framework import generics, status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class SeasonalProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        season = self.kwargs.get('season')
        filter_kwargs = {season: True}
        return Product.objects.filter(**filter_kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({
                'status': "failed",
                'message': f'No {self.kwargs.get("season")} products found.',
                'response_code': status.HTTP_404_NOT_FOUND,
                'data': []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': "success",
            'message': f'{self.kwargs.get("season").capitalize()} products retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)













    
        





