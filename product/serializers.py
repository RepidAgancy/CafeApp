from django.utils import timezone
from rest_framework import serializers

from core.settings import BASE_URL
from product import models


class ProductCategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CategoryProduct
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'image',]


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'image']


class ProductCartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItemProduct
        fields = ['product', 'weight', 'unit_status', 'cart', 'date', 'time', 'price']
        extra_kwargs = {
            'data': {'required': True}, 'time': {'required': True},
        }

    def create(self, validated_data):
        cart = models.CartProduct.objects.get(pk=self.data['cart'])
        product = models.Product.objects.get(pk=self.data['product'])
        cart_item = models.CartItemProduct.objects.create(
            product=product,
            cart=cart,
            weight=validated_data['weight'],
            unit_status=validated_data['unit_status'],
            date=validated_data['date'] if validated_data['date'] else timezone.now().date,
            time=validated_data['time'],
            price=validated_data['price'],
        )
        price = product.price * validated_data['weight']
        cart.total_price += price
        cart.save()
        return {
            'product': ProductListSerializer(cart_item.product).data,
            'cart': {
                'id': cart_item.id,
                'user': cart_item.cart.user.id,
                'total_price': cart_item.cart.total_price,
            },
            'weight': cart_item.weight,
            'unit_status': cart_item.unit_status,
            'date': cart_item.date,
            'time': cart_item.time,
            'price': cart_item.price
        }


class ProductItemEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItemProduct
        fields = ['weight',]

    def validate(self, data):
        user = self.context['request'].user
        try:
            cart_item = models.CartItemProduct.objects.get(pk=data['cart_item_id'])
        except models.CartItemProduct.DoesNotExist:
            raise serializers.ValidationError({"message": "CartItem does not exist"})
        if cart_item.cart.user != user:
            raise serializers.ValidationError({"message": 'You are not allowed to update'})

        return data

    def save(self):
        cart_item = models.CartItemProduct.objects.get(pk=self.data['cart_item_id'])

        old_weight = cart_item.weight
        product_price = cart_item.product.price
        total_price = cart_item.cart.total_price
        total_price -= (old_weight * product_price)

        weight = self.data['weight']
        total_price += (weight * product_price)
        cart_item.weight = weight
        cart_item.cart.total_price = total_price
        cart_item.cart.save()
        cart_item.save()
        return {
            'message': 'Cart Item is successfully updated',
        }


class ProductCartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')

    class Meta:
        model = models.CartItemProduct
        fields = ['id', 'product_name', 'product_image', 'weight', 'unit_status', 'price']


class ProductCartSerializer(serializers.ModelSerializer):
    cart_item = serializers.SerializerMethodField(method_name='get_cart_item')

    class Meta:
        model = models.CartProduct
        fields = ['id', 'total_price', 'cart_item',]

    def get_cart_item(self, obj):
        cart = models.CartProduct.objects.get(pk=obj.id)
        cart_item = models.CartItemProduct.objects.filter(cart=cart)
        return ProductCartItemSerializer(cart_item, many=True).data


class ProductOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderProduct
        fields = ['cart',]

    def create(self, validated_data):
        try:
            order = models.OrderProduct.objects.get(
                cart=validated_data['cart'], status=models.NOT_APPROVED, type=models.EXPENSE
            )
        except models.OrderProduct.DoesNotExist:
            order = models.OrderProduct.objects.create(
                cart=validated_data['cart'],
                status=models.NOT_APPROVED,
                type=models.EXPENSE
            )
        cart = order.cart
        if not models.CartItemProduct.objects.filter(cart=cart).exists():
            return {
                'message': 'You cannot create an order',
            }
        cart.is_confirm = True
        cart.save()
        return {
            'id': order.id,
            'cart': ProductCartSerializer(cart).data,
            'date': order.created_at.date().isoformat(),
            'time': order.created_at.time().isoformat(),
            'storekeeper': order.cart.user.username,
            'total_price': order.cart.total_price,
        }


class OrderConfirmSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

    def validate(self, data):
        user = self.context['request'].user
        try:
            order = models.OrderProduct.objects.get(pk=data['order_id'])
        except models.OrderProduct.DoesNotExist:
            raise serializers.ValidationError({"message": "Order does not exist"})
        if order.cart.user != user:
            raise serializers.ValidationError({"message": "You are not allowed to confirm order"})
        return data

    def save(self):
        order = models.OrderProduct.objects.get(pk=self.data['order_id'])
        order.is_confirm = True
        order.save()
        return {
            'message': 'Order is successfully confirmed',
        }


class ProductOrderListSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField(method_name='get_cart')
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = models.OrderProduct
        fields = ['id', 'cart', 'status', 'total_price']

    def get_cart(self, obj):
        return ProductCartSerializer(obj.cart).data

    def get_total_price(self, obj):
        return obj.cart.total_price


class ProductCreateSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    image = serializers.ImageField()
    category = serializers.IntegerField()

    def validate(self, data):
        try:
            category = models.CategoryProduct.objects.get(pk=data['category'])
        except models.CategoryProduct.DoesNotExist:
            raise serializers.ValidationError({"message": "Category does not exist"})
        return data

    def create(self, validated_data):
        category = models.CategoryProduct.objects.get(id=validated_data['category'])
        product = models.Product.objects.create(
            name=validated_data['product_name'],
            image=validated_data['image'],
            category=category,
        )
        return {
            'message': 'Product is successfully created',
        }


class ProductListByCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en', 'image',
        ]
