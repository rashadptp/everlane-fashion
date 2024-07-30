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
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'status': "success",
                'message': 'User logged in successfully.',
                'response_code': status.HTTP_200_OK,
                'data': {
                    'token': token.key
                }
            }, status=status.HTTP_200_OK)
        return Response({
            'status': "failed",
            'message': 'Invalid username or password.',
            'response_code': status.HTTP_400_BAD_REQUEST,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        
        # Retrieve or create the cart item
        cart_item, created = CartItem.objects.get_or_create(
            user=self.request.user,
            product_id=product_id,
            defaults={'quantity': 1}
        )
        
        if not created:
            # If the item already exists, increment the quantity by 1
            cart_item.quantity += 1
            cart_item.save()
        
        # Serialize the updated cart item
        serializer = CartItemSerializer(cart_item)
        return Response({
            'status': 'success',
            'message': 'Item added to cart successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

from rest_framework.views import APIView

class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        
        if not cart_items:
            return Response({'error': 'No items in cart'}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        order = Order.objects.create(user=user, total_amount=total_amount)
        order.items.set(cart_items)
        order.save()

        # Clear the cart after placing the order
        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class WishlistView(generics.ListCreateAPIView):
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RemoveFromWishlistView(generics.DestroyAPIView):
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)

    def get_object(self):
        # Assuming the item ID is passed in the URL
        return WishlistItem.objects.get(pk=self.kwargs['pk'], user=self.request.user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'status': 'success',
            'message': 'Item removed from wishlist successfully.',
            'response_code': status.HTTP_204_NO_CONTENT,  # 204 indicates successful deletion with no content
            'data': None  # No data to return after deletion
        })


class CartView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'message': 'Cart items retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        })
    

class RemoveFromCartView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Assuming the item ID is passed in the URL
        return CartItem.objects.get(pk=self.kwargs['pk'], user=self.request.user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'status': 'success',
            'message': 'Item removed from cart successfully.',
            'response_code': status.HTTP_204_NO_CONTENT,
        })
    
class IncrementCartItemView(APIView):
    
    def post(self, request, *args, **kwargs):
        cart_item_id = request.data.get('cart_item_id')
        increment_value = request.data.get('increment_value', 1)  # Default to increment by 1 if not provided
        
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        except CartItem.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Cart item not found.",
                "response_code": status.HTTP_404_NOT_FOUND,
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)
        
        cart_item.quantity += int(increment_value)
        cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response({
            "status": "success",
            "message": "Cart item quantity updated successfully.",
            "response_code": status.HTTP_200_OK,
            "data": serializer.data
        }, status=status.HTTP_200_OK)