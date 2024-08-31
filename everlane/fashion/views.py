from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import *
from .permissions import IsAdminUser
from .serializers import *
import pandas as pd
import json
from django.core.serializers.json import DjangoJSONEncoder
from .variables import STATUS_CHOICES
import uuid
from paypalrestsdk import Payment,configure
import paypalrestsdk
from django.conf import settings
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.core.files.base import ContentFile
from decimal import Decimal
from django.db.models import F
import tensorflow as tf
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import numpy as np
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
from reportlab.lib import colors
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.core.files.base import ContentFile
from decimal import Decimal
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from django.core.mail import send_mail
import random
import string
from django.contrib.auth import get_user_model

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
           
            token = Token.objects.get(user=request.user)
            
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

####################PRODUCT LIST WITH PAGINATION###############################

# from rest_framework.pagination import PageNumberPagination
# from django.db.models import Q

# class ProductPagination(PageNumberPagination):
#     page_size = 10  # Number of products per page
#     page_size_query_param = 'page_size'
#     max_page_size = 100


# class ProductListView(generics.ListAPIView):
#     serializer_class = ProductSerializer
#     pagination_class = ProductPagination

#     def get_queryset(self):
#         queryset = Product.objects.all()

#         # Filter by subcategory
#         subcategory_id = self.request.query_params.get('subcategory', None)
#         if subcategory_id is not None:
#             queryset = queryset.filter(subcategory_id=subcategory_id)

#         # Search by name or brand
#         search_query = self.request.query_params.get('query', None)
#         if search_query:
#             queryset = queryset.filter(
#                 Q(name__icontains=search_query) | Q(brand__icontains=search_query)
#             )

#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             product_data = []
#             for product in page:
#                 product_serializer = self.get_serializer(product)
#                 items = ProductItem.objects.filter(product=product)
#                 item_serializer = ProductItemSerializer(items, many=True)
#                 product_data.append(product_serializer.data)

#             return self.get_paginated_response(product_data)

#         product_data = []
#         for product in queryset:
#             product_serializer = self.get_serializer(product)
#             items = ProductItem.objects.filter(product=product)
#             item_serializer = ProductItemSerializer(items, many=True)
#             product_data.append(product_serializer.data)

#         return Response({
#             'status': "success",
#             'message': "Products retrieved successfully.",
#             'response_code': status.HTTP_200_OK,
#             'data': product_data
#         })

###without pagination####


#OLD CODE#

#product list/search

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

#product detail

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
   

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

#product creation

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
        
#product updation

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

#product delete

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

#add product item
 
class AddProductItemView(generics.CreateAPIView):
    serializer_class = ProductItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        size = request.data.get('size')
        stock = request.data.get('stock')

       
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Product not found.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        # Validate size
        if size not in [choice[0] for choice in SIZES]:
            return Response({
                'status': 'failed',
                'message': 'Invalid size.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate stock
        if stock is None or int(stock) < 0:
            return Response({
                'status': 'failed',
                'message': 'Stock must be a non-negative integer.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create ProductItem
        product_item = ProductItem.objects.create(
            product=product,
            size=size,
            stock=stock
        )

        return Response({
            'status': 'success',
            'message': 'Product item added successfully.',
            'response_code': status.HTTP_201_CREATED,
            'data': ProductItemSerializer(product_item).data
        }, status=status.HTTP_201_CREATED)


#categorylist

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

#subcategory list

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

#cartlist view,cart created

class CartListView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]  
    

    def get_queryset(self):
        
        user = self.request.user
        return Cart.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        carts = self.get_queryset()
        serializer = self.get_serializer(carts, many=True)
        for cart in serializer.data:
            cart['items'] = sorted(cart['items'], key=lambda item: item['id'])
        
        return Response({
            'status': 'success',
            'message': 'Cart list retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        })

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            cart = serializer.save(user=request.user)  
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

#add to cart view

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')
        size = request.data.get('size')
        quantity = int(request.data.get('quantity', 1))  

        try:
            product_item = ProductItem.objects.get(product_id=product_id, size=size)
        except ProductItem.DoesNotExist:
            return Response({'status': 'failed', 'message': 'Product id with size or product not found', 'response_code': status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

        
        cart, created = Cart.objects.get_or_create(user=user)

        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_item=product_item)

        if not created:
           
            cart_item.quantity += quantity
            cart_item.save()
            message = 'Quantity updated for the item in cart.'
        else:
            cart_item.quantity = quantity
            cart_item.save()
            message = 'Item added to cart.'

        cart.total_price = sum(
            item.product_item.product.price * item.quantity 
            for item in cart.items.filter(is_active=True, is_deleted=False)
            if item.product_item  
        )
        cart.save()

        return Response({
            'status': 'success',
            'message': message,
            'response_code': status.HTTP_200_OK,
            'data': CartSerializer(cart).data  
        }, status=status.HTTP_200_OK)

#cart item delete 

class CartItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        cart_item_id = kwargs.get('item_id')

        try:
           
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Cart item not found or does not belong to you.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        
        cart = cart_item.cart

       
        cart_item.delete()

       
        cart.total_price = sum(item.product_item.product.price * item.quantity for item in cart.items.filter(is_active=True, is_deleted=False))
        cart.save()

        return Response({
            'status': 'success',
            'message': 'Cart item deleted successfully.',
            'response_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

#updatecartitemquantity
 
class UpdateCartItemQuantityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        cart_item_id = request.data.get('cart_item_id')
        action = request.data.get('action')  

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

        
        cart = cart_item.cart
        cart.total_price = sum(item.product_item.product.price * item.quantity for item in cart.items.filter(is_active=True, is_deleted=False))
        cart.save()

        return Response({
            'status': 'success',
            'message': message,
            'response_code': status.HTTP_200_OK,
            'data': CartSerializer(cart).data  
        }, status=status.HTTP_200_OK)

#Banner views

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

#banner view

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


###Trending images listing api without using pagination###

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

##seasons without pagination###


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

    


#Questionnaire view

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

#Add to wishlist view

class AddWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        
        if not product_id:
            return Response({
                'status': 'failed',
                'message': 'Product ID is required.',
                'response_code': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Product not found.',
                'response_code': status.HTTP_404_NOT_FOUND,
            }, status=status.HTTP_404_NOT_FOUND)
        
        
        if Wishlist.objects.filter(user=request.user, product=product).exists():
            return Response({
                'status': 'failed',
                'message': 'Product already in wishlist.',
                'response_code': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
        wishlist = Wishlist.objects.create(user=request.user, product=product)
        
        return Response({
            'status': 'success',
            'message': 'Product added to wishlist successfully.',
            'response_code': status.HTTP_201_CREATED,
            'data': WishlistSerializer(wishlist).data
        }, status=status.HTTP_201_CREATED)

#wishlist delete

class DeleteWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id, *args, **kwargs):
       
        products = Product.objects.filter(id=product_id)
        
        if not products.exists():
            return Response({
                'status': 'failed',
                'message': 'Product not found.',
                'response_code': status.HTTP_404_NOT_FOUND,
            }, status=status.HTTP_404_NOT_FOUND)
        
        
        product = products.first()
        
        
        wishlist_items = Wishlist.objects.filter(product=product, user=request.user)
        
        if not wishlist_items.exists():
            return Response({
                'status': 'failed',
                'message': 'Wishlist item not found.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        
        
        wishlist_items.delete()
        
        
        return Response({
            'status': 'success',
            'message': 'Wishlist item deleted successfully.',
            'response_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)


#Default Address view

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

#Address list view

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
                'response_code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

#Address creation view

class AddressCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        data = request.data
        user = request.user

        
        required_fields = ['mobile', 'pincode', 'locality', 'address', 'city', 'state']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return Response({
                'status': 'failed',
                'message': f'Missing fields: {", ".join(missing_fields)}.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create the Address instance
        address = Address.objects.create(
            user=user,
            mobile=data['mobile'],
            pincode=data['pincode'],
            locality=data['locality'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            landmark=data.get('landmark', ''),  
            is_default=data.get('is_default', False),
            is_active=data.get('is_active', True),
            is_deleted=data.get('is_deleted', False)
        )

       
        serializer = AddressSerializer(address)
        return Response({
            'status': 'success',
            'message': 'Address created successfully.',
            'response_code': status.HTTP_201_CREATED,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


#Address delete view

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

#place order view

class PlaceOrderView(APIView):
    
    permission_classes = [IsAuthenticated]
    @staticmethod
    def initialize_paypal():
        configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })
        
        
    def post(self, request, *args, **kwargs):
        user = request.user
        
        payment_method = request.data.get('payment_method')
        order_type = request.data.get('order_type')  
        address_id = request.data.get('address_id')  
        disaster_id = request.data.get('disaster_id')  
        pickup_location_id = request.data.get('pickup_location_id')  
      
       
        if payment_method not in ['COD', 'ONLINE']:
            return Response({
                'status': 'failed',
                'message': 'Invalid payment method.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        
        if order_type not in ['delivery', 'donate']:
            return Response({
                'status': 'failed',
                'message': 'Invalid order type.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

       
        if order_type == 'donate' and payment_method == 'COD':
            return Response({
                'status': 'failed',
                'message': 'COD is not available for donations.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        
        try:
            cart = Cart.objects.filter(user=user, is_active=True, is_deleted=False).first()   
          
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

       
        total_amount = 0 

        for item in cart_items:
            product_price = item.product_item.product.price  
            quantity = item.quantity  
            total_amount += product_price * quantity
        

       
        disaster = None
        pickup_location = None
        if order_type== 'donate':
            disaster = Disaster.objects.filter(id=disaster_id).first()
            if not disaster:
                return Response({
            'status': 'failed',
            'message': 'Invalid disaster selected.',
            'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

            pickup_location = PickupLocation.objects.filter(id=pickup_location_id).first()
            if not pickup_location:
                return Response({
                'status': 'failed',
                'message': 'Invalid pickup location selected.',
                'response_code': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
        
        

        if order_type == 'delivery':
            address = Address.objects.filter(id=address_id, user=user, is_deleted=False).first()
            if not address:
                return Response({
                    'status': 'failed',
                    'message': 'Invalid address selected.',
                    'response_code': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)

        
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            payment_method=payment_method,
            is_completed=False if payment_method == 'ONLINE' else True,
            is_donated=True if order_type == 'donate' else False
        )

        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_item=item.product_item,
                quantity=item.quantity,
                price=item.product_item.product.price
            )
        cart_items_data = {}
        for item in cart_items:
            cart_items_data[item.product_item.id] = {
            'quantity': item.quantity,
            'price': str(item.product_item.product.price),   
    }

        CartHistory.objects.create(
        user=user,
        cart_data=json.dumps(cart_items_data, cls=DjangoJSONEncoder)
    )
       
        

        
        if order_type == 'donate':
            order.disaster = disaster
            order.pickup_location = pickup_location
            order.save()
            

            if payment_method == 'ONLINE':
            #payment by paypal   
                PlaceOrderView.initialize_paypal()

                payment = Payment({
                    "intent": "sale",
                    "payer": {
                        "payment_method": "paypal"
                    },
                    "redirect_urls": {
                        "return_url": "http://localhost:4200/shopping/payment",
                        "cancel_url": "http://localhost:4200/shopping/payment"
                    },
                    "transactions": [{
                        "item_list": {
                            "items": [{
                                "name": "Cart Items",
                                "sku": "001",
                                "price": str(total_amount),
                                "currency": "USD",
                                "quantity": 1
                            }]
                        },
                        "amount": {
                            "total": str(total_amount),
                            "currency": "USD"
                        },
                        "description": "This is the payment transaction description."
                    }]
                })

                if payment.create():
                    
                    order.paypal_payment_id = payment.id
                    order.save()

                    for link in payment.links:
                        if link.rel == "approval_url":
                            order.payment_status = 'Pending'
                            order.save()
                            return Response({
                                'status': 'success',
                                'message': 'Order placed successfully. Redirecting to PayPal.',
                                'approval_url': link.href,
                                'response_code': status.HTTP_201_CREATED
                            }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        'status': 'failed',
                        'message': 'Error occurred while processing PayPal payment.',
                        'response_code': status.HTTP_400_BAD_REQUEST
                    }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'status': 'success',
                'message': 'Order placed successfully as a donation.',
                'response_code': status.HTTP_201_CREATED,
                'data': OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)

        
        if order_type == 'delivery':
            order.delivery_address = address
            order.save()

            if payment_method == 'ONLINE':
                
                PlaceOrderView.initialize_paypal()

                payment = Payment({
                    "intent": "sale",
                    "payer": {
                        "payment_method": "paypal"
                    },
                    "redirect_urls": {
                        "return_url": "http://localhost:4200/shopping/payment",
                        "cancel_url": "http://localhost:4200/shopping/payment"
                    },
                    "transactions": [{
                        "item_list": {
                            "items": [{
                                "name": "Cart Items",
                                "sku": "001",
                                "price": str(total_amount),
                                "currency": "USD",
                                "quantity": 1
                            }]
                        },
                        "amount": {
                            "total": str(total_amount),
                            "currency": "USD"
                        },
                        "description": "This is the payment transaction description."
                    }]
                })

                if payment.create():
                    
                    order.paypal_payment_id = payment.id
                    order.save()

                    for link in payment.links:
                        if link.rel == "approval_url":
                            order.payment_status = 'Pending'
                            order.save()
                            return Response({
                                'status': 'success',
                                'message': 'Order placed successfully. Redirecting to PayPal.',
                                'approval_url': link.href,
                                'response_code': status.HTTP_201_CREATED
                            }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        'status': 'failed',
                        'message': 'Error occurred while processing PayPal payment.',
                        'response_code': status.HTTP_400_BAD_REQUEST
                    }, status=status.HTTP_400_BAD_REQUEST)

            order.payment_status = 'Completed'
            order.save()
            cart_items.delete()
            cart.save()
            invoice_number = str(uuid.uuid4()).replace('-', '').upper()[:10]
            invoice = Invoice.objects.create(
            order=order,
            user=user,
            invoice_number=invoice_number,
            total_amount=total_amount,
            )
            generate_invoice_pdf(invoice)


            return Response({
                'status': 'success',
                'message': 'Order placed successfully for delivery.',
                'response_code': status.HTTP_201_CREATED,
                'data':  OrderSerializer(order).data
    
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'failed',
            'message': 'Unknown error occurred.',
            'response_code': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)

#order cancel view

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]  

    def delete(self, request, order_id, *args, **kwargs):
        try:
           
            order = Order.objects.get(id=order_id, user=request.user)

            if order.order_status == 'Completed':
                return Response({
                    'status': 'failed',
                    'message': 'Order is already completed and cannot be canceled.',
                    'response_code': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)

            if order.payment_method == 'ONLINE':
                return Response({
                    'status': 'failed',
                    'message': 'Online payment orders cannot be canceled.',
                    'response_code': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)

            
            order.delete()

            return Response({
                'status': 'success',
                'message': 'Order canceled and deleted successfully.',
                'response_code': status.HTTP_200_OK,
            }, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Order not found or does not belong to you.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e),
                'response_code': status.HTTP_500_INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#order list view

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        user = self.request.user
        if user.is_admin:  
            return Order.objects.filter(is_deleted=False, is_completed=True).order_by("-id")
        else:  
            return Order.objects.filter(user=user, is_deleted=False, is_completed=True).order_by("-id")


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'message': 'Orders retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        })

#update order status view 

class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def patch(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()

        if not order:
            return Response({
            'status': 'failed',
            'message': 'Order not found',
            'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        order_status = request.data.get('order_status')
    

        if order_status not in dict(STATUS_CHOICES):
            return Response({
                'status': 'failed',
                'message': 'Invalid status.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        
        order.order_status = order_status
        order.save()
       
        
       
        return Response({
            'status': 'success',
            'message': 'Order status updated successfully.',
            'response_code': status.HTTP_200_OK,
            'data': OrderSerializer(order).data
        }, status=status.HTTP_200_OK)


#notification

class UserNotificationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
        serializer = NotificationSerializer(notifications, many=True)
       
        return Response({
            'status': 'success',
            'message': 'Notification retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

#recommendation

class RecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        
        skin_color = user.skin_color
        height = user.height
        gender = user.gender
        preferred_season = user.preferred_season
        usage_of_dress = user.usage_of_dress

        
        filters = {
            'is_active': True,
            'is_deleted': False,
        }

        
        if preferred_season == 'SUMMER':
            filters['summer'] = True
        elif preferred_season == 'WINTER':
            filters['winter'] = True
        elif preferred_season == 'MONSOON':
            filters['rainy'] = True
        elif preferred_season == 'AUTUMN':
            filters['autumn'] = True

       
        if skin_color:
            filters['skin_colors__contains'] = {skin_color.title(): True}

        if height:
            filters['heights__contains'] = {height.title(): True}

        
        if gender:
            filters['genders__contains'] = gender.upper()

        if usage_of_dress:
            filters['usages__contains'] = {usage_of_dress.title(): True}

        
        recommended_products = Product.objects.filter(**filters).distinct()

        
        serializer = RecommendSerializer(recommended_products, many=True,context={'request': request})
        

        return Response({
            'status': 'success',
            'message': 'Recommendations retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

#return request
 
class RequestReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order_item_id = request.data.get('order_item_id')
        return_quantity = request.data.get('return_quantity', 1)
        return_reason = request.data.get('return_reason')

        try:
            return_quantity = int(return_quantity)
        except ValueError:
            return Response({
                'status': 'failed',
                'message': 'Invalid return quantity.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        order_item = OrderItem.objects.filter(id=order_item_id, order__user=request.user).first()

        if not order_item:
            return Response({
                'status': 'failed',
                'message': 'Order item not found or does not belong to you.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        if return_quantity > (order_item.quantity - order_item.returned_quantity):
            return Response({
                'status': 'failed',
                'message': 'Return quantity exceeds available quantity.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

       
        order_item.is_returned = True
        order_item.returned_quantity += return_quantity
        order_item.return_reason = return_reason
        order_item.return_requested_on = timezone.now()
        order_item.return_status = 'PENDING'

       
        if order_item.is_fully_returned:
            order_item.return_status = 'PENDING'
        
        order_item.save()

       
        refund_amount = return_quantity * order_item.price
        order_item.refund_amount = refund_amount
        order_item.refund_date = timezone.now()
        order_item.save()

        return Response({
            'status': 'success',
            'message': 'Return requested successfully.',
            'response_code': status.HTTP_200_OK,
            'data': OrderItemSerializer(order_item).data
        }, status=status.HTTP_200_OK)

#return pending view

class ReturnPendingView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        return_to_approve = OrderItem.objects.filter(is_returned=True,return_status="PENDING")
        serializer = OrderItemSerializer(return_to_approve, many=True,context={'request': request})

        return Response({
            'status': 'success',
            'message': 'Return awaiting approval retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

#return process  

class ProcessReturnView(APIView):
    permission_classes = [IsAdminUser]  

    def post(self, request, *args, **kwargs):
        order_item_id = request.data.get('order_item_id')
        action = request.data.get('action')  

       
        order_item = OrderItem.objects.filter(id=order_item_id).first()

        if not order_item:
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

        if action == 'approve':
            
            order_item.return_status = 'APPROVED'
            order_item.refund_amount = order_item.price * order_item.returned_quantity  
            order_item.refund_date = timezone.now()
            order_item.save()

            
            if order_item.returned_quantity >= order_item.quantity:
                order_item.return_status = 'RETURNED'
                order_item.save()

           

            return Response({
                'status': 'success',
                'message': 'Return approved and refund processed.',
                'response_code': status.HTTP_200_OK,
                'data': OrderItemSerializer(order_item).data  
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


# user profile view


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response({
            'status': 'success',
            'message': 'User profile retrieved successfully',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

#profile update view

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        
        data = request.data
        user = request.user

        
        updateable_fields = ['username', 'first_name', 'last_name', 'email', 'mobile'] 
        updated_data = {field: data[field] for field in updateable_fields if field in data}

        
        if not updated_data:
            return Response({
                'status': 'failed',
                'message': 'No valid fields provided for update.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        
        for field, value in updated_data.items():
            setattr(user, field, value)
        user.save()

        serializer = ProfileSerializer(user)
        return Response({
            'status': 'success',
            'message': 'User profile updated successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

#password change view

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
       
        data = request.data
        user = request.user

        
        required_fields = ['old_password', 'new_password']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return Response({
                'status': 'error',
                'message': f'Missing fields: {", ".join(missing_fields)}.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        
        if not user.check_password(data['old_password']):
            return Response({
                'status': 'error',
                'message': 'Old password is incorrect.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        
        user.set_password(data['new_password'])
        user.save()

        return Response({
            'status': 'success',
            'message': 'Password updated successfully.',
            'response_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)




###############################################    DONATION      ##########################################################

#disasterlist and disaster registration view

class DisasterListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        disasters = Disaster.objects.filter(is_approved=True).exclude(
            fulfilled_men_dresses__gte=F('required_men_dresses'),
            fulfilled_women_dresses__gte=F('required_women_dresses'),
            fulfilled_kids_dresses__gte=F('required_kids_dresses')
        )
        serializer = DisasterSerializer(disasters, many=True)
        return Response({
            'status': 'success',
            'message': 'Disasters retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        data = request.data
        user=request.user

        required_fields = ['name', 'adhar', 'location', 'description', 'required_men_dresses', 'required_women_dresses', 'required_kids_dresses']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return Response({
                'status': 'failed',
                'message': f'Missing fields: {", ".join(missing_fields)}.',
                'response_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

            

       

            
        disaster = Disaster(
            name=data['name'],
            user=user,
            adhar=data['adhar'],
            location=data['location'],
            description=data['description'],
            required_men_dresses=int(data.get('required_men_dresses', 0)),
            required_women_dresses=int(data.get('required_women_dresses', 0)),
            required_kids_dresses=int(data.get('required_kids_dresses', 0)),
            created_by=request.user
        )
        disaster.save()

       
        serializer = DisasterSerializer(disaster)
        return Response({
            'status': 'success',
            'message': 'Disaster created successfully. Awaiting approval.',
            'response_code': status.HTTP_201_CREATED,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
#disaster pending list view

class AdminDisasterApprovalListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        disasters_to_approve = Disaster.objects.filter(is_approved=False,is_deleted=False)
        serializer = DisasterSerializer(disasters_to_approve, many=True)
        return Response({
            'status': 'success',
            'message': 'Disasters awaiting approval retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

#approve disaster view

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

        if request.data.get('approve', True): 
            disaster.is_approved = True
            disaster.save()
            return Response({
                'status': 'success',
                'message': 'Disaster approved successfully.',
                'response_code': status.HTTP_200_OK,
                'data': DisasterSerializer(disaster).data
            }, status=status.HTTP_200_OK)
        else:  
            disaster.soft_delete()
            return Response({
                'status': 'success',
                'message': 'Disaster rejected and deleted successfully.',
                'response_code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

############################################################    AI    #############################################################################

#dress donation view

torn_model = tf.keras.models.load_model('quality_check_torn.h5')
dirty_model = tf.keras.models.load_model('quality_check_dirty.h5')

class DressDonationCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def preprocess_image(self, image_file: InMemoryUploadedFile):
        """Preprocess the image for prediction."""
        image = Image.open(image_file)
        image = image.resize((100,100))  
        image = np.array(image) / 255.0  
        image = np.expand_dims(image, axis=0)  
        return image

    def check_quality(self, image_file):
        """Check if the image is torn or dirty."""
        preprocessed_image = self.preprocess_image(image_file)
        
        
        is_torn = torn_model.predict(preprocessed_image)[0][0] > 0.5
        is_dirty = dirty_model.predict(preprocessed_image)[0][0] > 0.5
        
        return is_torn, is_dirty
        

    def post(self, request, *args, **kwargs):
        serializer = DressDonationSerializer(data=request.data)
        if serializer.is_valid():
            disaster = serializer.validated_data['disaster']
            
            men_dresses = serializer.validated_data.get('men_dresses', 0)
            women_dresses = serializer.validated_data.get('women_dresses', 0)
            kids_dresses = serializer.validated_data.get('kids_dresses', 0)
            total_dresses = men_dresses + women_dresses + kids_dresses

            #  the quality check
            images = request.FILES.getlist('images')
            print(len(images))
            if total_dresses != len(images):
                return Response({
                    'status': 'failed',
                    'message': 'The number of dresses does not match the number of images uploaded.',
                    'response_code': status.HTTP_200_OK
                }, status=status.HTTP_200_OK)

            for image in images:
                is_torn, is_dirty = self.check_quality(image)
                if is_dirty or is_torn:
                    return Response({
                        'status': 'error',
                        'message': 'One or more dresses are dirty or torn. Please upload clean dresses and good condition.',
                        'response_code': status.HTTP_200_OK
                    }, status=status.HTTP_200_OK)
                
            
            if (disaster.fulfilled_men_dresses + men_dresses > disaster.required_men_dresses or
                disaster.fulfilled_women_dresses + women_dresses > disaster.required_women_dresses or
                disaster.fulfilled_kids_dresses + kids_dresses > disaster.required_kids_dresses):
                return Response({
                    'status': 'failed',
                    'message': 'Donation exceeds the required dresses for this disaster.',
                    'response_code': status.HTTP_200_OK
                }, status=status.HTTP_200_OK)
            
            
            donation = serializer.save(user=request.user)

            
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


#user donation list view

class UserDonationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        donations = user.donations.all()
        serializer = DressDonationListSerializer(donations, many=True)
        return Response({
            'status': 'success',
            'message': 'User donations retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data,
            'donation_count': donations.count()
        }, status=status.HTTP_200_OK)


#disaster donation view

class DisasterDonationsView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get(self, request, disaster_id, *args, **kwargs):
        disaster = Disaster.objects.filter(id=disaster_id).first()
        if not disaster:
            return Response({
            'status': 'failed',
            'message': 'Disaster not found.',
            'response_code': status.HTTP_404_NOT_FOUND
        }, status=status.HTTP_404_NOT_FOUND)


        
        if not (request.user == disaster.user or request.user.is_admin):
            return Response({
                'status': 'failed',
                'message': 'You do not have permission to view these donations.',
                'response_code': status.HTTP_403_FORBIDDEN
            }, status=status.HTTP_403_FORBIDDEN)

        donations = DressDonation.objects.filter(disaster=disaster)
        serializer = DressDonationListSerializer(donations, many=True)

        return Response({
            'status': 'success',
            'message': 'Donations retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


#user disaster view

class UserDisastersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
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


#invoice generation

def generate_invoice_pdf(invoice):

    file_name = f'invoice_{invoice.invoice_number}.pdf'
    
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    styles = getSampleStyleSheet()
    
  
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=20,
        textColor=colors.HexColor('#0d47a1')  
    )
    
    heading_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#424242')  
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=8,
        textColor=colors.HexColor('#212121')  
    )
    
    
    order = invoice.order
    user = order.user
    

    company_info = """
    <font size=12><b>Everlane Style</b></font><br/>
    Near MP Tower<br/>
    Thondayad<br/>
    Calicut, Kerala, 670601<br/>
    Phone: (+91) 456-7890<br/>
    Email: contact@everlane.com
    """
    story.append(Paragraph(company_info, normal_style))
    story.append(Spacer(1, 12)) 
    
   
    header_data = [
        ['Invoice Number:', invoice.invoice_number],
        ['Date:', invoice.created_at.strftime('%Y-%m-%d')],
        ['Due Date:', invoice.created_at.strftime('%Y-%m-%d')],  
        ['Customer Name:', user.get_full_name() or user.username],
    ]
    
    header_table = Table(header_data, colWidths=[2.5*inch, 4.5*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d47a1')),  
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#212121')),  
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  
        ('TOPPADDING', (0, 0), (-1, 0), 12),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 12))  
    
    
    item_data = [['Description', 'Quantity', 'Unit Price', 'Total']]
    
    
    for item in order.items.all():
        item_data.append([
            item.product_item.product.name,
            item.quantity,
            f"Rs.{item.price:.2f}",
            f"Rs. {(Decimal(item.quantity) * item.price).quantize(Decimal('0.01')):.2f}"
        ])
    
    item_table = Table(item_data, colWidths=[3*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d47a1')),  
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#212121')), 
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),  
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  
    ]))
    story.append(item_table)
    story.append(Spacer(1, 12))  
    
  
    totals_data = [
        ['Subtotal', f"Rs. {invoice.total_amount:.2f}"],
        ['Tax (5%)', f"Rs. {(invoice.total_amount * Decimal('0.05')).quantize(Decimal('0.01')):.2f}"],  
        ['Total', f"Rs. {(invoice.total_amount+((invoice.total_amount * Decimal('0.05')).quantize(Decimal('0.01')))):.2f}"]
    ]
    
    totals_table = Table(totals_data, colWidths=[3*inch, 1.5*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d47a1')),  
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#212121')),  
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ('LINEABOVE', (0, 2), (-1, 2), 2, colors.black),  
    ]))
    story.append(totals_table)
    story.append(Spacer(1, 24))  
    
    
    footer_info = """
    <font size=10>
    <b>Thank you for your business!</b><br/>
    Please make payment if not.<br/>
    For any queries, contact us at (123) 456-7890 or email us at contact@everlane.com.
    </font>
    """
    story.append(Paragraph(footer_info, normal_style))
    
   
    doc.build(story)
    
    
    buffer.seek(0)
    pdf_file = ContentFile(buffer.getvalue())
    
    invoice.pdf.save(file_name, pdf_file)


#execute payment

class ExecutePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')

        try:
            payment = Payment.find(payment_id)

            if payment.execute({"payer_id": payer_id}):
                user = request.user
                cart = Cart.objects.filter(user=user, is_active=True, is_deleted=False).first() 
                cart_items = CartItem.objects.filter(cart=cart, is_active=True, is_deleted=False)
                cart_items.delete()
                cart.save()
                order = Order.objects.get(paypal_payment_id=payment_id)
                order.payment_status = 'Completed'
                order.is_completed = True
                order.save()

                invoice_number = str(uuid.uuid4()).replace('-', '').upper()[:10]
                invoice = Invoice.objects.create(
                    order=order,
                    user=order.user,
                    invoice_number=invoice_number,
                    total_amount=order.total_amount,
                )
                generate_invoice_pdf(invoice)

                return Response({
                    'status': 'success',
                    'message': 'Payment completed successfully and order placed.',
                    'response_code': status.HTTP_200_OK,
                    'data': OrderSerializer(order).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'failed',
                    'message': 'Payment execution failed.',
                    'response_code': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)

        except Order.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'Order not found.',
                'response_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e),
                'response_code': status.HTTP_500_INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#cancel payment

class CancelPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
       
        payment_id = request.GET.get('token')
 
        try:
            order = Order.objects.get(paypal_payment_id=payment_id)
            order.payment_status = 'Canceled'
            order.save()
        except Order.DoesNotExist:
            
            pass
        
       
        return Response({
                'status': 'failed',
                'message': 'Payment Canceled.',
                'response_code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
    

#pickup list

class PickupListView(generics.ListCreateAPIView):
    queryset = PickupLocation.objects.all()
    serializer_class = PickupLocationSerializer

    def get(self, request, *args, **kwargs):
        pickups = self.get_queryset()
        serializer = self.get_serializer(pickups, many=True)
        response_data = {
            'status': 'success',
            'message': 'Pickup Location retrieved successfully.',
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }
        return Response(response_data)
    

#forgot password

class ForgotPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            
            User = get_user_model()  
            
            try:
                user = User.objects.get(username=username)
                
                
                new_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                
               
                user.set_password(new_password)
                user.save()
                
                
                subject = 'Your New Password'
                message = f'Hello {user.username},\n\nYour new password is: {new_password}\nPlease change it after logging in.'
                email_from = settings.DEFAULT_FROM_EMAIL
                recipient_list = [user.email]
                
                send_mail(subject, message, email_from, recipient_list)
                
                return Response({'message': 'A new password has been sent to the email address associated with the username.'}, status=status.HTTP_200_OK)
            
            except User.DoesNotExist:
                return Response({'error': 'Username not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





