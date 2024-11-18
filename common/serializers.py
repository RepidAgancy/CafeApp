from rest_framework import serializers

from common import models


class TableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Table
        fields = [
            'id', 'number', 'is_busy',
        ]


class TableGetSerializer(serializers.Serializer):
    table_id = serializers.IntegerField()

    def validate(self, data):
        try:
            table = models.Table.objects.get(id=data['table_id'])
        except models.Table.DoesNotExist:
            raise serializers.ValidationError({'message': 'Table not found'})
        if table.is_busy == True:
            raise serializers.ValidationError({'message': 'Table is busy'})
        return data

    def save(self):
        table = models.Table.objects.get(id=self.validated_data['table_id'])
        table.is_busy = True
        table.save()
        cart = models.Cart.objects.create(
            table=table,
            user=self.context['request'].user,
        )
        return {
            'message': 'Table created',
            'cart_id': cart.id,
        }


class FoodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food
        fields = [
            'id', 'name', 'image', 'price'
        ]


class FoodDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food
        fields = [
            'id', 'name', 'image', 'price',
            'food_info_uz','food_info_ru', 'food_info_en',
        ]


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategoryFood
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en', 'image'
        ]


class FoodListByCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food
        fields = [
            'id', 'name', 'image', 'price',
        ]


class CartItemCreateSerializer(serializers.Serializer):
    food_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    cart_id = serializers.IntegerField()

    def validate(self, data):
        try:
            food = models.Food.objects.get(id=data['food_id'])
            cart = models.Cart.objects.get(id=data['cart_id'])
        except models.Food.DoesNotExist:
            raise serializers.ValidationError({'message': 'Food not found'})
        except models.Cart.DoesNotExist:
            raise serializers.ValidationError({'message': 'Cart not found'})
        return data

    def create(self, validated_data):
        food = models.Food.objects.get(id=validated_data['food_id'])
        cart = models.Cart.objects.get(id=validated_data['cart_id'])
        cart_item = models.CartItem.objects.create(
            food=food,
            cart=cart,
            quantity=validated_data['quantity'],
        )
        total_price = cart_item.food.price * cart_item.quantity
        cart_item.cart.total_price += total_price
        cart_item.cart.save()
        return {
            'food': cart_item.food.name,
            'cart': {
                'id': cart_item.cart.id,
                'user': cart_item.cart.user.username,
                'table': cart_item.cart.table.number,
                'total_price': f'{cart_item.cart.total_price} UZS',
            },
            'quantity': cart_item.quantity,
        }

class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['quantity']

    def save(self):
        try:
            cart_item = models.CartItem.objects.get(id=self.context['cart_item_id'])
        except models.CartItem.DoesNotExist:
            raise serializers.ValidationError({'message': 'CartItem not found'})
        if cart_item.cart.user == self.context['request'].user:
            old_quantity = cart_item.quantity
            food_price = cart_item.food.price
            total_price = cart_item.cart.total_price
            total_price -= (old_quantity * food_price)

            quantity = self.validated_data['quantity']
            total_price += (quantity * food_price)
            cart_item.quantity = self.validated_data['quantity']

            cart_item.cart.total_price = total_price
            cart_item.cart.save()
            cart_item.save()
        else:
            raise serializers.ValidationError({'message': 'You are not allowed to update'})

        return {
            'message': 'CartItem updated',
        }


class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(method_name='get_price')
    food_name = serializers.SerializerMethodField(method_name='get_food_name')
    food_image = serializers.SerializerMethodField(method_name='get_food_image')

    class Meta:
        model = models.CartItem
        fields = [
            'id', 'food', 'quantity', 'price', 'food_name', 'food_image'
        ]

    def get_price(self, obj):
        return f'{obj.food.price} UZS'

    def get_food_name(self, obj):
        return obj.food.name

    def get_food_image(self, obj):
        return obj.food.image


class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField(method_name='get_cart_items')

    class Meta:
        model = models.Cart
        fields = [
            'id', 'user', 'table', 'total_price', 'cart_items',
        ]

    def get_cart_items(self, obj):
        cart = models.Cart.objects.get(id=obj.id)
        cart_items = models.CartItem.objects.filter(cart=cart)
        return CartItemSerializer(cart_items, many=True).data


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            'id', 'cart',
        ]
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        order = models.Order.objects.create(
            cart=validated_data['cart'], status=models.IN_PROCESS
        )
        cart = order.cart
        return {
            'order_id': order.id,
            'status': order.status,
            'created_at': order.created_at,
            'cart': CartSerializer(order.cart).data,
            'total_price': cart.total_price,
            'table_number': cart.table.number,
        }


class OrderChangeStatusSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

    def validate(self, data):
        try:
            order = models.Order.objects.get(id=data['order_id'])
        except models.Order.DoesNotExist:
            raise serializers.ValidationError({'message': 'Order not found'})
        if order.is_confirm:
            raise serializers.ValidationError({'message': 'Order is confirmed'})
        return data

    def save(self, *args, **kwargs):
        order = models.Order.objects.get(id=self.validated_data['order_id'])
        order.status = models.DONE
        order.cart.table.type = models.DONE
        order.cart.table.save()
        order.save()

        return {
            'message': 'Order status successfully changed'
        }


class OrderListSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField(method_name='get_cart')
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = models.Order
        fields = [
            'id', 'cart', 'status', 'created_at', 'total_price'
        ]

    def get_cart(self, obj):
        cart = obj.cart
        return CartSerializer(cart).data

    def get_total_price(self, obj):
        total_price = obj.cart.total_price
        return f"{total_price} UZS"


class OrderFoodConfirmSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

    def validate(self, data):
        try:
            order = models.Order.objects.get(id=data['order_id'])
        except models.Order.DoesNotExist:
            raise serializers.ValidationError({'message': 'Order not found'})
        if order.is_confirm:
            raise serializers.ValidationError({'message': 'Order is confirmed'})
        return data

    def save(self, *args, **kwargs):
        order = models.Order.objects.get(id=self.validated_data['order_id'])
        order.is_confirm = True
        order.save()

        return {
            'message': 'Order is successfully confirmed'
        }