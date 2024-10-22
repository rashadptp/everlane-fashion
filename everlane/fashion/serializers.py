from rest_framework import serializers
from .models import *
from .variables import * 
import phonenumbers
from django.contrib.auth import authenticate
from .models import Banner
from rest_framework.response import Response
from rest_framework import generics, status


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile','country_code', 'password', 'confirm_password']
        
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'mobile': {'required': True},
            'country_code':{'required':True},
            'password': {'required': True},
            'confirm_password': {'required': True},
        }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        email = data.get('email')

        mobile = data.get('mobile')
        country_code = data.get('country_code')
        full_number = f"+{country_code}{mobile}"

        print(f"Full number for validation: {full_number}")

        # chsnge responses to standard format
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        if len(password) < 8:
            raise serializers.ValidationError("Password does not meet the minimum length of 8 characters")

        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("Password must contain at least one digit")

        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError("Password must contain at least one letter")
        
        # Email uniqueness validation
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")

        
        try:
            parsed_number = phonenumbers.parse(full_number, None)
            print(f"Parsed Number: {parsed_number}")  

            if not phonenumbers.is_valid_number(parsed_number):
                print(f"Validation failed for: {parsed_number}")
                raise serializers.ValidationError("Invalid mobile number.")
        except phonenumbers.NumberParseException as e:
            print(f"Exception: {e}") 

            raise serializers.ValidationError("Invalid mobile number or country code.")

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            mobile=validated_data['mobile'],
            country_code=validated_data['country_code'],
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


class PickupLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickupLocation
        fields = ['id', 'city', 'address']


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
        fields = ['id', 'name', 'description', 'price','brand', 'subcategory', 'image','is_active','created_on','is_deleted','is_trending','skin_colors','heights','genders','usages','winter','summer','rainy','autumn']
        
class RecommendSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Product
        fields = ['id', 'name', 'description', 'price','brand', 'subcategory', 'image','is_active','created_on','is_deleted','is_trending','winter','summer','rainy','autumn','skin_colors', 'heights', 'genders', 'usages']

class SeosonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ['id', 'name', 'description', 'price','brand', 'subcategory', 'image','is_active','created_on','is_deleted','winter','summer','rainy','autumn']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product_item.product.name')
    product_price = serializers.ReadOnlyField(source='product_item.product.price')
    product_image = serializers.ImageField(source='product_item.product.image', read_only=True)
    size = serializers.ReadOnlyField(source='product_item.size')    
    
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product_item','product_name', 'quantity', 'price','return_status','size','product_image',
                'product_price','is_returned','order_item_status','returned_quantity','return_reason','return_requested_on','return_status', 'refund_amount', 'refund_date']
    
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'total_amount', 'created_at', 'pdf']

class OrderSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer(read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    disaster_name = serializers.ReadOnlyField(source='disaster.name')
    pickup_location_address = serializers.ReadOnlyField(source='pickup_location.address')
    class Meta:
        model = Order
        fields = ['id', 'order_code','user','first_name' ,'total_amount','is_active','is_deleted','created_on','is_completed', 'payment_method', 'payment_status','order_status','items',
                  'is_donated', 'disaster', 'disaster_name',
            'pickup_location', 'pickup_location_address', 'is_paid','delivery_address','invoice']


class ReturnSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount','is_active','is_deleted','created_on','is_completed', 
                  'payment_method', 'payment_status','order_status', 'items']
        

class WishlistSerializer(serializers.ModelSerializer):
    

    product_image = serializers.ImageField(source='product.image', read_only=True) 
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    product_description=serializers.ReadOnlyField(source='product.description')

   
    class Meta:
        model = Wishlist
        fields = ['id', 'product','is_active','is_deleted','created_on','product_image','product_name', 'product_price','product_description']



class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product_item.product.name')
    product_price = serializers.ReadOnlyField(source='product_item.product.price')
    product_image = serializers.ImageField(source='product_item.product.image', read_only=True)
    product_id=serializers.ReadOnlyField(source='product_item.product.id', read_only=True)
    size = serializers.ReadOnlyField(source='product_item.size')
    stock = serializers.ReadOnlyField(source='product_item.stock')

    class Meta:
        model = CartItem
        fields = ['id', 'product_item', 'product_id','product_name', 'product_price', 'quantity', 'is_active', 'is_deleted', 'created_on', 'product_image', 'size','stock']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    # total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items','is_active','is_deleted','created_on','total_price']
        read_only_fields = ['id', 'user', 'total_price']

#for banner


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
        

class ProfileSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username','first_name', 'last_name', 'email', 'mobile', 'old_password', 'new_password']

    def update(self, instance, validated_data):
        # Handle password change
        old_password = validated_data.pop('old_password', None)
        new_password = validated_data.pop('new_password', None)
        
        if old_password and new_password:
            if not instance.check_password(old_password):
                raise serializers.ValidationError({"old_password": "Old password is not correct."})
            if len(new_password) < 8:
                raise serializers.ValidationError({"new_password": "New password must be at least 8 characters long."})
            if not any(char.isdigit() for char in new_password):
                raise serializers.ValidationError({"new_password": "New password must contain at least one digit."})
            if not any(char.isalpha() for char in new_password):
                raise serializers.ValidationError({"new_password": "New password must contain at least one letter."})
            instance.set_password(new_password)
        
        # Update other user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()

class ForgotUsernameSerializer(serializers.Serializer):
    email = serializers.EmailField()
        
########################################     DONATION    #########################################################

class DisasterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='created_by.first_name', read_only=True)
    class Meta:
        model = Disaster
        fields = '__all__'

    

        


class ImageUploadModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUploadModel
        fields = ['image']

class DressDonationSerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(source='user.username', read_only=True)
    images = serializers.ListField(
        child=serializers.ImageField(max_length=100, allow_empty_file=False, use_url=True),
        allow_empty=False,
        write_only=True
    )

    class Meta:
        model = DressDonation
        fields = ['disaster', 'men_dresses', 'women_dresses', 'kids_dresses', 'images','pickup_location', 'donated_on', 'donor_name']

    def get_images(self, obj):
        """
        Return URLs of the uploaded images.
        """
        return [image.image.url for image in obj.images.all()]


    # def validate_images(self, value):
    #     """
    #     Ensure at least 5 images are uploaded.
    #     """
    #     if len(value) < 5:
    #         raise serializers.ValidationError("You must upload at least 5 dress images.")
    #     return value

    def create(self, validated_data):
        images_data = validated_data.pop('images')

        donation = DressDonation.objects.create(**validated_data)
        
        image_instances = []
        for image_data in images_data:
            image_instance = ImageUploadModel.objects.create(image=image_data)
            image_instances.append(image_instance)
        
        donation.images.set(image_instances)
        return donation


#Listing ofdress donation
class DressDonationListSerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(source='user.username', read_only=True)
    disaster_name=serializers.CharField(source='disaster.name',read_only=True)
    images = serializers.SerializerMethodField()
    pickup_location_city=serializers.CharField(source='pickup_location.city',read_only=True)
    pickup_location_address=serializers.CharField(source='pickup_location.address',read_only=True)

    class Meta:
        model = DressDonation
        fields = ['disaster','disaster_name', 'men_dresses', 'women_dresses', 'kids_dresses', 'images','pickup_location', 'donated_on',
                   'donor_name','pickup_location_address','pickup_location_city']

    def get_images(self, obj):
        """
        Return URLs of the uploaded images.
        """
        return [image.image.url for image in obj.images.all()]


#NOTIFICATION SERIALIZER

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'verb', 'description','formatted_timestamp']

    def get_formatted_timestamp(self, obj):
        return obj.formatted_timestamp()

# 'timestamp'
    



