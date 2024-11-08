from itertools import product

from rest_framework import serializers

from product import models

class ProductCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategoryProduct
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'image',]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'image', 'price']


class ProductCartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItemProduct
        fields = ['product', 'weight', 'unit_status', 'cart', 'date', 'time']
        extra_kwargs = {
            'data': {'required': True}, 'time': {'required': True}
        }
    def validate(self, data):
        user = self.context['request'].user
        try:
            product = models.Product.objects.get(pk=data['product'])
            cart = models.CartProduct.objects.get(pk=data['cart'])
        except models.Product.DoesNotExist:
            raise serializers.ValidationError({"message": "Product does not exist"})
        except models.CartProduct.DoesNotExist:
            raise serializers.ValidationError({"message": "CartProduct does not exist"})
        if cart.user != user:
            raise serializers.ValidationError({'message': 'Cart user is not the requested user'})
        return data

    def create(self, validated_data):
        cart_item = models.CartItemProduct.objects.create(
            product=models.Product.objects.get(pk=self.data['product']),
            cart=models.CartProduct.objects.get(pk=self.data['cart']),
            weight=validated_data['weight'],
            unit_status=validated_data['unit_status'],
            date=validated_data['date'],
            time=validated_data['time'],
        )
        return {
            'product': cart_item.product,
            'cart': {
                'id': cart_item.id,
                'user': cart_item.cart.user.id,
                'total_price': cart_item.cart.total_price,
            },
            'weight': cart_item.weight,
            'unit_status': cart_item.unit_status,
            'date': cart_item.date,
            'time': cart_item.time,
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
    price = serializers.SerializerMethodField(method_name='get_price')

    class Meta:
        model = models.CartItemProduct
        fields = ['product', 'weight', 'unit_status', 'date', 'time', 'price']

    def get_price(self, obj):
        return f'{obj.product.price:.3f} uzs'


class ProductCartSerializer(serializers.ModelSerializer):
    cart_item = serializers.SerializerMethodField(method_name='get_cart_item')

    class Meta:
        model = models.CartProduct
        fields = ['id', 'cart_item',]

    def get_cart_item(self, obj):
        cart = models.CartProduct.objects.get(pk=obj.id)
        cart_item = models.CartProduct.objects.get(cart=cart)
        return ProductCartItemSerializer(cart_item, many=True).data


class ProductOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderProduct
        fields = ['cart', 'status']

    def validate(self, data):
        user = self.context['request'].user
        try:
            cart = models.CartProduct.objects.get(pk=data['cart'])
        except models.CartProduct.DoesNotExist:
            raise serializers.ValidationError({"message": "CartProduct does not exist"})
        if cart.user != user:
            raise serializers.ValidationError({"message": "You are not allowed to create order"})
        return data

    def create(self, validated_data):
        cart = models.CartProduct.objects.get(pk=validated_data['cart'])
        order = models.OrderProduct.objects.create(cart=cart, status=models.NOT_APPROVED)
        cart.is_confirm = True
        cart.save()
        return {
            'id': f'#{order.id}',
            'cart': ProductCartSerializer(order.cart).data,
            # 'date': order.
            'storekeeper': order.cart.user,
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
        return f'{obj.cart.total_price:.3f} uzs'


class ProductCreateSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    image = serializers.ImageField()
    price = serializers.DecimalField(max_digits=10, decimal_places=3)
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
            price=validated_data['price'],
            category=category,
        )
        return {
            'message': 'Product is successfully created',
        }