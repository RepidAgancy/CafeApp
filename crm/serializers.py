from django.contrib.auth.hashers import make_password
from django.db.models.base import method_set_order
from rest_framework import serializers

from common import models as common_models
from accounts.models import User, Profession
from crm import models
from product.models import Product


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number', 'salary', 'profession',
        ]


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'salary', 'profession', 'work_experience', 'username', 'password',
        ]

    def create(self, validated_data):
        employee = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            salary=validated_data['salary'],
            profession=validated_data['profession'],
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
            'first_name', 'last_name', 'email', 'phone_number', 'salary', 'profession', 'work_experience', 'username', 'password',
        ]


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.Food
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en', 'image', 'price', 'category'
        ]


class FoodCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.Food
        fields = [
            'id', 'name', 'image', 'price', 'category', 'food_info', 'food_composition'
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
        return obj.category.name if obj.category else None