from rest_framework import serializers
from .models import *

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile', 'password', 'confirm_password']
        
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'mobile': {'required': True},
            'password': {'required': True},
            'confirm_password': {'required': True},
        }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})

        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError({"password": "Password must contain at least one digit."})

        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError({"password": "Password must contain at least one letter."})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            mobile=validated_data['mobile']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class AdminRegistrationSerializer(UserRegistrationSerializer):
    class Meta(UserRegistrationSerializer.Meta):
        fields = UserRegistrationSerializer.Meta.fields + ['is_admin',]
    
    def create(self, validated_data):
        validated_data['is_admin'] = True
        return super().create(validated_data)

#login

from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        data['user'] = user
        return data


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name','is_admin']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','image','is_active','is_deleted','created_on']

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category','image','is_active','is_deleted','created_on']





class ProductItemSerializer(serializers.ModelSerializer):
    is_out_of_stock = serializers.SerializerMethodField()
    class Meta:
        model = ProductItem
        fields = ['id', 'product', 'size', 'stock','is_out_of_stock']

    def get_is_out_of_stock(self, obj):
        return obj.stock == 0    

class ProductRetrieveSerializer(serializers.ModelSerializer):
    items = ProductItemSerializer(many=True, read_only=True) 

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price','brand', 'subcategory', 'image','is_active','created_on','is_deleted','is_trending','items']


class ProductSerializer(serializers.ModelSerializer):
    # items = ProductItemSerializer(many=True, read_only=True) 

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price','brand', 'subcategory', 'image','is_active','created_on','is_deleted','is_trending']
class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ['id', 'name', 'description', 'price','brand', 'subcategory', 'image','is_active','created_on','is_deleted','is_trending','winter','summer','rainy','autumn','skin_colors', 'heights', 'genders', 'usages']

class SeosonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ['id', 'name', 'description', 'price','brand', 'subcategory', 'image','is_active','created_on','is_deleted','winter','summer','rainy','autumn']

class OrderItemSerializer(serializers.ModelSerializer):
    return_status = serializers.CharField(source='get_return_status_display', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price','return_status','is_returned','return_reason','return_requested_on']
    return_status = serializers.CharField(source='get_return_status_display', read_only=True)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount','is_active','is_deleted','created_on','is_completed', 'payment_method', 'payment_status','status','items','return_status']


class ReturnSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount','is_active','is_deleted','created_on','is_completed', 
                  'payment_method', 'payment_status','status',
                 'return_status', 'refund_amount', 'refund_date', 'items']
        

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'product','is_active','is_deleted','created_on']


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = CartItem
        fields = ['id', 'product','product_name', 'product_price', 'quantity','is_active','is_deleted','created_on']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items','is_active','is_deleted','created_on','total_price']
        read_only_fields = ['id', 'user', 'total_price']

#for banner
from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['image','category','is_active','is_deleted','created_on','which']  



class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','gender', 'skin_color','height','preferred_season','usage_of_dress']
    
    def update(self, instance, validated_data):
        instance.gender = validated_data.get('gender', instance.gender)
        instance.skin_color = validated_data.get('skin_color', instance.skin_color)
        instance.height = validated_data.get('height', instance.height)
        instance.preferred_season = validated_data.get('preferred_season', instance.preferred_season)
        instance.usage_of_dress = validated_data.get('usage_of_dress', instance.usage_of_dress)
        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','mobile','pincode','locality','address','city','state','landmark','is_default','is_active','is_deleted','created_on']











