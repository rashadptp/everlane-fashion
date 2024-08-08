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

# class UserListView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        subcategory_id = self.request.query_params.get('subcategory', None)
        if subcategory_id is not None:
            queryset = queryset.filter(subcategory_id=subcategory_id)
        return queryset

    def list(self, request, *args, **kwargs):
        products = self.get_queryset()
        product_data = []
        for product in products:
            product_serializer = self.get_serializer(product)
            items = ProductItem.objects.filter(product=product)
            item_serializer = ProductItemSerializer(items, many=True)
            product_data.append(product_serializer.data)
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
                'response_code': status.HTTP_404_NOT_FOUND,
                'data': []
            }, status=status.HTTP_404_NOT_FOUND)


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
        
        if payment_method not in ['COD', 'ONLINE']:
            return Response({
                'status': 'failed',
                'message': 'Invalid payment method.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        
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

        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Create the order
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            payment_method=payment_method,
            is_completed=False if payment_method == 'ONLINE' else True
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

        if payment_method == 'ONLINE':
            # Integrate with a payment gateway here
            # Redirect the user to the payment gateway
            # payment_url = self.initiate_online_payment(order)   PAYMENT LATER
            return Response({
                'status': 'success',
                'message': 'Order placed successfully. Payment will be integrated later.',
                'response_code': status.HTTP_201_CREATED,
                'data': {
                    'order': OrderSerializer(order).data,
                    # 'payment_url': payment_url
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'success',
            'message': 'Order placed successfully.',
            'response_code': status.HTTP_201_CREATED,
            'data': OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)

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

from django.db.models import Q

class ProductSearchAPIView(APIView):
    def get(self, request, format=None):
        query = request.GET.get('query')
        if query:
            keywords = query.split()
            q_objects = Q()
            for keyword in keywords:
                q_objects |= Q(name__icontains=keyword) | Q(brand__icontains=keyword)

            results = Product.objects.filter(q_objects).distinct()

            if results.exists():
                serializer = ProductSerializer(results, many=True)
                return Response({
                    "success": True,
                    "message": "Products found.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "message": "No products found matching the query."
                }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "success": False,
            "message": "No query provided."
        }, status=status.HTTP_400_BAD_REQUEST)


        

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



        

























    
        





