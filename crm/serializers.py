from datetime import datetime

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from common import models as common_models
from accounts.models import User
from crm import models
from product.models import Product


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'phone_number','profile_image', 'work_experience', 'salary','type'
        ]


class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=False, max_length=255, help_text="Search query string")


class ValidateAccessToken(serializers.Serializer):
    access_token = serializers.CharField()


class StartandEndDateSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField(required=False, input_formats=["%Y-%m-%d"], help_text="year month day")
    end_date = serializers.DateTimeField(required=False,input_formats=["%Y-%m-%d"], help_text="year month day")

    def validate_start_date(self, value):
            if value.date() > datetime.now().date():
                raise serializers.ValidationError("Start date cannot be in the future.")
            return value


    def validate_end_date(self, value):
        if value.date() > datetime.now().date():
            raise serializers.ValidationError("End date cannot be in the future.")
        return value


    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")


        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError("Start date must be before or equal to the end date.")
        return attrs


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'salary', 'work_experience','profile_image', 'type', 'username', 'password',
        ]

    def create(self, validated_data):
        employee = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            type = validated_data['type'],
            phone_number=validated_data['phone_number'],
            profile_image = validated_data.get('profile_image',None),
            salary=validated_data['salary'],
            work_experience=validated_data['work_experience'],
            username=validated_data['username'],
            password=make_password(validated_data['password']),
        )
        return {
            'message': 'Employee successfully added',
        }


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    work_experience = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'salary', 'type', 'work_experience','profile_image', 'username', 'password',
        ]

class FoodCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.CategoryFood
        fields = [
            'id', 'name', 'image'
        ]


class FoodSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField(method_name='get_category_name')
    category = serializers.SerializerMethodField(method_name='get_category_id')

    class Meta:
        model = common_models.Food
        fields = [
            'id', 'name', 'image', 'price', 'category', 'category_name', 'food_info_uz', 'food_info_ru', 'food_info_en'
        ]

    def get_category_name(self, obj):
        return obj.category.name

    def get_category_id(self, obj):
        return obj.category.id
    

class FoodCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.Food
        fields = [
            'id', 'name', 'image', 'price', 'category', 'food_info_uz', 'food_info_ru', 'food_info_en'
        ]

    def create(self, validated_data):
        food = common_models.Food.objects.create(
            name=validated_data['name'],
            image=validated_data['image'],
            price=validated_data['price'],
            category=validated_data['category'],
            food_info_uz=validated_data.get('food_info_uz', None),
            food_info_ru=validated_data.get('food_info_ru', None),
            food_info_en=validated_data.get('food_info_en', None),
        )   
        return {
            'id': food.id, 
            'name': food.name, 
            'image': f"http://api.repid.uz{food.image.url}", 
            'price': food.price, 
            'category_name': food.category.name, 
            'category': food.category_id, 
            'food_info_uz':food.food_info_uz,
            'food_info_ru':food.food_info_ru,
            'food_info_en':food.food_info_en,
        }
    
    def to_representation(self, instance):
        data = super(FoodCreateUpdateSerializer, self).to_representation(instance)
        data['category_name'] = instance.category.name

        return data

    
    
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    class Meta:
        model = Product
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en', 'image', 'price', 'category', 'category_name'
        ]


class PaymentEmployeeSalaryCreateSerializer(serializers.Serializer):
    category = serializers.CharField()
    full_name = serializers.CharField()
    profession = serializers.CharField()
    price = serializers.IntegerField()
    description = serializers.CharField()

    def create(self, validated_data):
        payment = models.Payment.objects.create(
            category=validated_data['category'],
            full_name=validated_data['full_name'],
            profession=validated_data['profession'],
            price=validated_data['price'],
            description=validated_data['description'],
        )
        return payment


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            'price', 'description', 'category'
        ]


class PaymentHistoryListSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField(method_name='get_created_at')
    payment_type = serializers.SerializerMethodField(method_name='get_payment_type')

    class Meta:
        model = models.Payment
        fields = [
            'id', 'full_name', 'payment_type', 'profession', 'price', 'created_at', 'description'
        ]

    def get_created_at(self, obj):
        return obj.created_at.date() if obj.created_at else None

    def get_payment_type(self, obj):
        return obj.category if obj.category else None