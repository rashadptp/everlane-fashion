from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import *
from .permissions import IsAdminUser
from .serializers import *
import joblib
import pandas as pd

#register view

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            return Response({
                'status': "success",
                'message': 'User registered successfully.',
                'response_code': status.HTTP_201_CREATED,
                'data': UserRegistrationSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        else:

            return Response({
                'status': "failed",
                'message': 'User registration failed.',
                'response_code': status.HTTP_400_BAD_REQUEST,
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class RegisterAdminView(generics.CreateAPIView):
    serializer_class = AdminRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            return Response({
                'status': "success",
                'message': "Admin registered successfully.",
                'response_code': status.HTTP_201_CREATED,
                'data': AdminRegistrationSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': "failed",
                'message': "Admin registration failed.",
                'response_code': status.HTTP_400_BAD_REQUEST,
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

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
                'status': "success",
                 'message': 'Login successful',
                 'response_code': status.HTTP_200_OK,
                 'token': token.key,
                  'user_id': user.pk,
                   'username': user.username
                       }, status=status.HTTP_200_OK)

        return Response({
            'status': "failed",
            'message': 'Invalid username or password',
            'response_code': status.HTTP_400_BAD_REQUEST,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        

# Logout view
           
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Get the user's token
            token = Token.objects.get(user=request.user)
            # Delete the token to log the user out
            token.delete()
            
            return Response({
                'status': "success",
                'message': 'Logged out successfully.',
                'response_code': status.HTTP_200_OK,
                'data': None
            }, status=status.HTTP_200_OK)
        
        except Token.DoesNotExist:
            return Response({
                'status': "failed",
                'message': 'Logout failed. Token does not exist.',
                'response_code': status.HTTP_400_BAD_REQUEST,
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'status': "failed",
                'message': 'Logout failed.',
                'response_code': status.HTTP_400_BAD_REQUEST,
                'data': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)





# new product list and search

from django.db.models import Q

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        # Filter by subcategory
        subcategory_id = self.request.query_params.get('subcategory', None)
        if subcategory_id is not None:
            queryset = queryset.filter(subcategory_id=subcategory_id)

        # Search by name or brand
        search_query = self.request.query_params.get('query', None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(brand__icontains=search_query)
            )

        return queryset

    def list(self, request, *args, **kwargs):
        products = self.get_queryset()
        product_data = []
        for product in products:
            product_serializer = self.get_serializer(product)
            items = ProductItem.objects.filter(product=product)
            item_serializer = ProductItemSerializer(items, many=True)
            product_data.append( product_serializer.data)

        return Response({
            'status': "success",
            'message': "Products retrieved successfully.",
            'response_code': status.HTTP_200_OK,
            'data': product_data
        })

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        product_data=[]
        product_serializer = self.get_serializer(product)
        items = ProductItem.objects.filter(product=product)
        item_serializer = ProductItemSerializer(items, many=True)
        product_data.append(product_serializer.data)
        return Response({
            'status': 'success',
            'message': 'Product details retrieved successfully.',
            'response_code': 200,
            'data': product_serializer.data
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


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class CartListView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get_queryset(self):
        # Filter carts to show only those belonging to the authenticated user
        user = self.request.user
        return Cart.objects.filter(user=user)

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
            cart = serializer.save(user=request.user)  # Ensure the cart is created for the authenticated user
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


# class CartDetailView(generics.RetrieveDestroyAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer

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
        
        cart.total_price = sum(item.product.price * item.quantity for item in cart.items.filter(is_active=True, is_deleted=False))
        cart.save()

        return Response({
            'status': 'success',
            'message': message,
            'response_code': status.HTTP_200_OK,
            'data': CartSerializer(cart).data  # Optional: Return the updated cart data
        }, status=status.HTTP_200_OK)
    

class CartItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        cart_item_id = kwargs.get('item_id')

        try:
            # Ensure the cart item belongs to the authenticated user
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Cart item not found or does not belong to you.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({
            'status': 'success',
            'message': 'Cart item deleted successfully.',
            'response_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    
class UpdateCartItemQuantityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        cart_item_id = request.data.get('cart_item_id')
        action = request.data.get('action')  # 'increase' or 'decrease'

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=user, is_active=True, is_deleted=False)
        except CartItem.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Cart item not found.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
            message = 'Quantity increased.'
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                message = 'Quantity decreased.'
            else:
                return Response({
                    'status': 'failed',
                    'message': 'Quantity cannot be less than 1.',
                    'response_code': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'status': 'failed',
                'message': 'Invalid action.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        # Update the total price of the cart
        cart = cart_item.cart
        cart.total_price = sum(item.product.price * item.quantity for item in cart.items.filter(is_active=True, is_deleted=False))
        cart.save()

        return Response({
            'status': 'success',
            'message': message,
            'response_code': status.HTTP_200_OK,
            'data': CartSerializer(cart).data  # Return the updated cart data
        }, status=status.HTTP_200_OK)



#Banner views

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Banner
from .serializers import BannerSerializer

class AngularBannerListView(generics.ListAPIView):
    serializer_class = BannerSerializer

    def get_queryset(self):
        category_id=self.request.query_params.get('category_id')
        queryset= Banner.objects.filter(is_deleted=False, is_active=True, which='A')
        if category_id:
            queryset= queryset.filter(category_id=category_id)
        return queryset

        
       

    def get(self, request, *args, **kwargs):
        
        banners = self.get_queryset()
        serializer = self.get_serializer(banners, many=True)

        if not banners.exists():
            response_data = {
                'status': 'failed',
                'message': 'No banners found.',
                'response_code': status.HTTP_404_NOT_FOUND,
                'data': []
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'status': 'success',
            'message': 'banners retrieved successfully.',
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
        category_id=self.request.query_params.get('category_id')
        queryset= Banner.objects.filter(is_deleted=False, is_active=True, which='F')
        if category_id:
            queryset= queryset.filter(category_id=category_id)
        return queryset


    def get(self, request, *args, **kwargs):
        
        banners = self.get_queryset()
        serializer = self.get_serializer(banners, many=True)

        if not banners.exists():
            response_data = {
                'status': 'failed',
                'message': 'No banners found.',
                'response_code': status.HTTP_404_NOT_FOUND,
                'data': []
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'status': 'success',
            'message': 'banners retrieved successfully.',
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
    serializer_class = SeosonSerializer

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

#Questionnaire   


class QuestionnaireCreateView(generics.UpdateAPIView):
    serializer_class = QuestionnaireSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            questionnaire = serializer.save()
            return Response({
                'status': "success",
                'message': 'Questionnaire submitted successfully.',
                'response_code': status.HTTP_201_CREATED,
                'data': QuestionnaireSerializer(questionnaire).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': "failed",
            'message': 'Failed to submit questionnaire.',
            'response_code': status.HTTP_400_BAD_REQUEST,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    


#wishlist view

class WishlistListView(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        
        return Wishlist.objects.filter(user=self.request.user, is_deleted=False)

    def get(self, request, *args, **kwargs):
        wishlists = self.get_queryset()
        if wishlists.exists():
            serializer = self.get_serializer(wishlists, many=True)
            return Response({
                'status': 'success',
                'message': 'Wishlist retrieved successfully.',
                'response_code': status.HTTP_200_OK,
                'data': serializer.data
            })
        else:
            return Response({
                'status': 'failed',
                'message': 'No items found in your wishlist.',
                'response_code': status.HTTP_200_OK,
                'data': []
            }, status=status.HTTP_200_OK)


# #Add to wishlist view


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import WishlistSerializer

class AddWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            
            wishlist = serializer.save(user=request.user)
            return Response({
                'status': 'success',
                'message': 'Product added to wishlist successfully.',
                'response_code': status.HTTP_201_CREATED,
                'data': WishlistSerializer(wishlist).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'failed',
            'message': 'Failed to add product to wishlist.',
            'response_code': status.HTTP_400_BAD_REQUEST,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class DeleteWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
        
            wishlist_item = Wishlist.objects.get(pk=pk, user=request.user)
        except Wishlist.DoesNotExist:
          
            return Response({
                'status': 'failed',
                'message': 'Wishlist item not found.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        
        
        wishlist_item.delete()
        
        return Response({
            'status': 'success',
            'message': 'Wishlist item deleted successfully.',
            'response_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)


#Address view

class DefaultAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            default_address = Address.objects.get(user=request.user, is_default=True)
            serializer = AddressSerializer(default_address)
            return Response({
                'status': 'success',
                'message': 'Default address retrieved successfully.',
                'response_code': status.HTTP_200_OK,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Default address not found.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)


class AddressListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user, is_deleted=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():

            serializer = self.get_serializer(queryset, many=True)
            return Response({
            'status': 'success',
            'message': 'Addresses retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

        else:
            
            return Response({
                'status': 'failed',
                'message': 'No addresses found.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)


class AddressCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                'status': 'success',
                'message': 'Address created successfully.',
                'response_code': status.HTTP_201_CREATED,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'failed',
                'message': 'Address creation failed.',
                'response_code': status.HTTP_400_BAD_REQUEST,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class AddressDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def delete(self, request, *args, **kwargs):
        try:
            address = self.get_object()
            address.is_deleted = True
            address.save()
            return Response({
                'status': 'success',
                'message': 'Address deleted successfully.',
                'response_code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Address not found.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)




class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        payment_method = request.data.get('payment_method')
        order_type = request.data.get('order_type')  # 'delivery' or 'donate'
        address_id = request.data.get('address_id')  # For delivery option
        disaster_id = request.data.get('disaster_id')  # For donation option
        pickup_location_id = request.data.get('pickup_location_id')  # For donation option

        # Validate payment method
        if payment_method not in ['COD', 'ONLINE']:
            return Response({
                'status': 'failed',
                'message': 'Invalid payment method.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate order type
        if order_type not in ['delivery', 'donate']:
            return Response({
                'status': 'failed',
                'message': 'Invalid order type.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        # Restrict COD for donations
        if order_type == 'donate' and payment_method == 'COD':
            return Response({
                'status': 'failed',
                'message': 'COD is not available for donations.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get the user's active cart
        try:
            cart = Cart.objects.get(user=user, is_active=True, is_deleted=False)
        except Cart.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'No active cart found for the user.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        cart_items = CartItem.objects.filter(cart=cart, is_active=True, is_deleted=False)
        if not cart_items.exists():
            return Response({
                'status': 'failed',
                'message': 'No items in the cart to place an order.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the total amount
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Create the order
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            payment_method=payment_method,
            is_completed=False if payment_method == 'ONLINE' else True,
            is_donated=True if order_type == 'donate' else False
        )

        # Create order items from cart items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear the cart
        cart_items.delete()
        cart.save()

        # If the order is a donation
        if order_type == 'donate':
            try:
                disaster = Disaster.objects.get(id=disaster_id)
                pickup_location = PickupLocation.objects.get(id=pickup_location_id)
            except Disaster.DoesNotExist:
                return Response({
                    'status': 'failed',
                    'message': 'Invalid disaster selected.',
                    'response_code': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
            except PickupLocation.DoesNotExist:
                return Response({
                    'status': 'failed',
                    'message': 'Invalid pickup location selected.',
                    'response_code': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)

            # Assign disaster and pickup location to the order
            order.disaster = disaster
            order.pickup_location = pickup_location
            order.save()

            if payment_method == 'ONLINE':
                # Integrate with a payment gateway here
                return Response({
                    'status': 'success',
                    'message': 'Order placed successfully as a donation. Payment will be integrated later.',
                    'response_code': status.HTTP_201_CREATED,
                    'data': {
                        'order': OrderSerializer(order).data,
                        # 'payment_url': payment_url  # Placeholder for payment URL
                    }
                }, status=status.HTTP_201_CREATED)

            return Response({
                'status': 'success',
                'message': 'Order placed successfully as a donation.',
                'response_code': status.HTTP_201_CREATED,
                'data': OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)

        # If the order is for delivery
        if order_type == 'delivery':
            try:
                address = Address.objects.get(id=address_id, user=user, is_deleted=False)
            except Address.DoesNotExist:
                return Response({
                    'status': 'failed',
                    'message': 'Invalid address selected.',
                    'response_code': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)

            # Assign the delivery address to the order
            order.delivery_address = address
            order.save()

            if payment_method == 'ONLINE':
                # Integrate with a payment gateway here
                return Response({
                    'status': 'success',
                    'message': 'Order placed successfully for delivery. Payment will be integrated later.',
                    'response_code': status.HTTP_201_CREATED,
                    'data': {
                        'order': OrderSerializer(order).data,
                        # 'payment_url': payment_url  # Placeholder for payment URL
                    }
                }, status=status.HTTP_201_CREATED)

            return Response({
                'status': 'success',
                'message': 'Order placed successfully for delivery.',
                'response_code': status.HTTP_201_CREATED,
                'data': OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'failed',
            'message': 'Unknown error occurred.',
            'response_code': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)
    # def initiate_online_payment(self, order):
    #     # Placeholder for initiating an online payment
    #     # This should be replaced with actual payment gateway integration code
    #     payment_url = "https://payment-gateway-url.com"
    #     return payment_url



class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Optionally filter orders by the authenticated user
        user = self.request.user
        return Order.objects.filter(user=user, is_deleted=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'message': 'Orders retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        })


class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Order not found or does not belong to you.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        status = request.data.get('status')
        if status not in dict(Order.STATUS_CHOICES):
            return Response({
                'status': 'failed',
                'message': 'Invalid status.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        order.status = status
        order.save()

        return Response({
            'status': 'success',
            'message': 'Order status updated successfully.',
            'response_code': status.HTTP_200_OK,
            'data': OrderSerializer(order).data
        }, status=status.HTTP_200_OK)


# Search view

# from django.db.models import Q

# class ProductSearchAPIView(APIView):
#     def get(self, request, format=None):
#         query = request.GET.get('query')
#         if query:
#             keywords = query.split()
#             q_objects = Q()
#             for keyword in keywords:
#                 q_objects |= Q(name__icontains=keyword) | Q(brand__icontains=keyword)

#             results = Product.objects.filter(q_objects).distinct()

#             if results.exists():
#                 serializer = ProductSerializer(results, many=True)
#                 return Response({
#                     "success": True,
#                     "message": "Products found.",
#                     "data": serializer.data
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response({
#                     "success": False,
#                     "message": "No products found matching the query."
#                 }, status=status.HTTP_404_NOT_FOUND)
#         return Response({
#             "success": False,
#             "message": "No query provided."
#         }, status=status.HTTP_400_BAD_REQUEST)


        

# class RecommendDressView(APIView):
#     def post(self, request, *args, **kwargs):
#         skin_color = request.data.get('skin_color')
#         height = request.data.get('height')
#         gender = request.data.get('gender')
#         preferred_season = request.data.get('preferred_season')
#         usage_of_dress = request.data.get('usage_of_dress')

#         # Load the pre-trained model
#         model_path = 'recommendation_model.pkl'
#         clf = joblib.load(model_path)

#         # Create the input DataFrame
#         input_data = pd.DataFrame({
#             'skin_type': [skin_color],
#             'height': [height],
#             'gender': [gender],
#             'season': [preferred_season],
#             'usage': [usage_of_dress]
#         })
#         input_data = pd.get_dummies(input_data)

#         # Predict the recommended dress
#         dress_ids = clf.predict(input_data)
#         recommended_dresses = Product.objects.filter(id__in=dress_ids)

#         serializer = ProductSerializer(recommended_dresses, many=True)
#         return Response({
#             'status': 'success',
#             'message': 'Dresses recommended successfully.',
#             'response_code': status.HTTP_200_OK,
#             'data': serializer.data
#         })

class RecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Retrieve user attributes
        skin_color = user.skin_color
        height = user.height
        gender = user.gender
        preferred_season = user.preferred_season
        usage_of_dress = user.usage_of_dress

        # Start with basic filters
        filters = {
            'is_active': True,
            'is_deleted': False,
        }

        # Add season filter
        if preferred_season == 'SUMMER':
            filters['summer'] = True
        elif preferred_season == 'WINTER':
            filters['winter'] = True
        elif preferred_season == 'MONSOON':
            filters['rainy'] = True
        elif preferred_season == 'AUTUMN':
            filters['autumn'] = True

        # Add dynamic filters for user attributes
        if skin_color:
            filters['skin_colors__icontains'] = skin_color
        if height:
            filters['heights__icontains'] = height
        if gender:
            filters['genders__icontains'] = gender
        if usage_of_dress:
            filters['usages__icontains'] = usage_of_dress

        # Apply filters
        recommended_products = Product.objects.filter(**filters).distinct()
        
        # Log filters and results
        print(f"Applied filters: {filters}")
        print(f"Recommended products: {recommended_products}")

        # Serialize the filtered products
        serializer = RecommendSerializer(recommended_products, many=True)

        return Response({
            'status': 'success',
            'message': 'Recommendations retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)



        



############ RETURN ################
class RequestReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order_item_id = request.data.get('order_item_id')
        return_reason = request.data.get('return_reason')

        try:
            order_item = OrderItem.objects.get(id=order_item_id, order__user=request.user)
        except OrderItem.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Order item not found or does not belong to you.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        if order_item.is_returned:
            return Response({
                'status': 'failed',
                'message': 'Return has already been requested for this item.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        order_item.is_returned = True
        order_item.return_reason = return_reason
        order_item.return_requested_on = timezone.now()
        order_item.return_status = 'PENDING'
        order_item.save()

        return Response({
            'status': 'success',
            'message': 'Return requested successfully.',
            'response_code': status.HTTP_200_OK,
            'data': OrderItemSerializer(order_item).data
        }, status=status.HTTP_200_OK)


class ProcessReturnView(APIView):
    permission_classes = [IsAdminUser]  # Only allow admin users to process returns

    def post(self, request, *args, **kwargs):
        order_item_id = request.data.get('order_item_id')
        action = request.data.get('action')  # 'approve' or 'reject'

        try:
            order_item = OrderItem.objects.get(id=order_item_id)
        except OrderItem.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Order item not found.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        if not order_item.is_returned:
            return Response({
                'status': 'failed',
                'message': 'No return request found for this item.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        order = order_item.order

        if action == 'approve':
            order_item.is_returned = True
            order_item.save()

            order_item.return_status = 'APPROVED'
            order_item.refund_amount = order_item.price * order_item.quantity
            order_item.refund_date = timezone.now()
            order_item.save()

            # Process refund (if necessary)
            # Here, integrate with a payment gateway to process the refund for online payments

            return Response({
                'status': 'success',
                'message': 'Return approved and refund processed.',
                'response_code': status.HTTP_200_OK,
                'data': ReturnSerializer(order).data
            }, status=status.HTTP_200_OK)

        elif action == 'reject':
            order_item.return_status = 'REJECTED'
            order_item.save()

            return Response({
                'status': 'success',
                'message': 'Return request rejected.',
                'response_code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'failed',
            'message': 'Invalid action provided.',
            'response_code': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)







###############################################    DONATION      ##########################################################
class DisasterListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        disasters = Disaster.objects.filter(is_approved=True)
        serializer = DisasterSerializer(disasters, many=True)
        return Response({
            'status': 'success',
            'message': 'Disasters retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DisasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({
                'status': 'success',
                'message': 'Disaster created successfully. Awaiting approval.',
                'response_code': status.HTTP_201_CREATED,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'failed',
            'message': 'Invalid data.',
            'response_code': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
class AdminDisasterApprovalListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        disasters_to_approve = Disaster.objects.filter(is_approved=False)
        serializer = DisasterSerializer(disasters_to_approve, many=True)
        return Response({
            'status': 'success',
            'message': 'Disasters awaiting approval retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class ApproveDisasterView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, disaster_id):
        try:
            disaster = Disaster.objects.get(id=disaster_id)
        except Disaster.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Disaster not found.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        disaster.is_approved = True
        disaster.save()

        return Response({
            'status': 'success',
            'message': 'Disaster approved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': DisasterSerializer(disaster).data
        }, status=status.HTTP_200_OK)


class DressDonationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DressDonationSerializer(data=request.data)
        if serializer.is_valid():
            disaster = serializer.validated_data['disaster']
            
            men_dresses = serializer.validated_data.get('men_dresses', 0)
            women_dresses = serializer.validated_data.get('women_dresses', 0)
            kids_dresses = serializer.validated_data.get('kids_dresses', 0)
            
            if (disaster.fulfilled_men_dresses + men_dresses > disaster.required_men_dresses or
                disaster.fulfilled_women_dresses + women_dresses > disaster.required_women_dresses or
                disaster.fulfilled_kids_dresses + kids_dresses > disaster.required_kids_dresses):
                return Response({
                    'status': 'failed',
                    'message': 'Donation exceeds the required dresses for this disaster.',
                    'response_code': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Record the donation
            donation = serializer.save(user=request.user)

            # Update the disaster's fulfillment status
            disaster.update_fulfillment(men_dresses, women_dresses, kids_dresses)

            return Response({
                'status': 'success',
                'message': 'Dress donation recorded successfully.',
                'response_code': status.HTTP_201_CREATED,
                'data': DressDonationSerializer(donation).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'failed',
            'message': 'Invalid data.',
            'response_code': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class UserDonationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        donations = user.donations.all()
        serializer = DressDonationSerializer(donations, many=True)
        return Response({
            'status': 'success',
            'message': 'User donations retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data,
            'donation_count': donations.count()
        }, status=status.HTTP_200_OK)






    
        
class DisasterDonationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, disaster_id, *args, **kwargs):
        try:
            disaster = Disaster.objects.get(id=disaster_id)
        except Disaster.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Disaster not found.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user is the one who registered the disaster or an admin
        if not (request.user == disaster.user or request.user.is_staff):
            return Response({
                'status': 'failed',
                'message': 'You do not have permission to view these donations.',
                'response_code': status.HTTP_403_FORBIDDEN
            }, status=status.HTTP_403_FORBIDDEN)

        donations = DressDonation.objects.filter(disaster=disaster)
        serializer = DressDonationSerializer(donations, many=True)

        return Response({
            'status': 'success',
            'message': 'Donations retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)



class UserDisastersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Retrieve disasters registered by the current user
        disasters = Disaster.objects.filter(user=request.user)

        if not disasters.exists():
            return Response({
                'status': 'success',
                'message': 'You do not have any registered disasters.',
                'response_code': status.HTTP_200_OK,
                'data': []
            }, status=status.HTTP_200_OK)

        serializer = DisasterSerializer(disasters, many=True)
        return Response({
            'status': 'success',
            'message': 'Disasters retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
