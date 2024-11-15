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
            'id', 'first_name', 'last_name', 'email', 'phone_number','profile_image', 'work_experience', 'salary','type'
        ]


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'salary', 'work_experience','profile_image', 'type', 'username', 'password',
        ]

    def create(self, validated_data):
        employee = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
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
            'first_name', 'last_name', 'email', 'phone_number', 'salary', 'type', 'work_experience','profile_image', 'username', 'password',
        ]

class FoodCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.CategoryFood
        fields = [
            'id', 'name', 'image'
        ]


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.Food
        fields = [
            'id', 'name', 'image', 'price', 'category', 'food_info_uz', 'food_info_ru', 'food_info_en'
        ]


class FoodCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.Food
        fields = [
            'id', 'name', 'image', 'price', 'category', 'food_info_uz', 'food_info_ru', 'food_info_en' 
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en', 'image', 'price', 'category'
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