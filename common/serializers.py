from rest_framework import serializers

from common import models
from accounts.models import WAITER, CASHIER, User


class TableListSerializer(serializers.ModelSerializer):
    cart_id = serializers.SerializerMethodField(method_name='get_cart_id')

    class Meta:
        model = models.Table
        fields = [
            'id', 'number', 'is_busy', 'cart_id'
        ]

    def get_cart_id(self, obj):
        user = self.context['request'].user
        if obj.is_busy:
            cart = models.Cart.objects.filter(table_id=obj.id).last()
            return cart.id
        else:
            if user.type == CASHIER:
                cart = models.Cart.objects.filter(user=user).last()
                try:
                    order = models.Order.objects.get(cart=cart)
                except:
                    return cart.id
                if order.is_confirm == True:
                    return None
                return cart.id
            else:
                return None


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
        user = self.context['request'].user
        table = models.Table.objects.get(id=self.validated_data['table_id'])
        if user.type == WAITER:
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
            'id', 'name_uz', 'name_ru', 'name_en', 'image', 'price',
        ]


class FoodDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en',  'image', 'price',
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
            'id', 'name_uz', 'name_ru', 'name_en', 'image', 'price',
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
        if cart_item.cart.is_confirm:
            raise serializers.ValidationError({'message': 'CartItem is already confirmed'})
        else:
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
        return obj.food.image.url


class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField(method_name='get_cart_items')
    table = serializers.IntegerField(source='table.number')

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
        user = self.context['user']
        try:
            order = models.Order.objects.get(
                cart=validated_data['cart']
            )
        except models.Order.DoesNotExist:
            if user.type == WAITER:
                order = models.Order.objects.create(
                    cart=validated_data['cart'],
                    status=models.IN_PROCESS,
                )
            elif user.type == CASHIER:
                order = models.Order.objects.create(
                    cart=validated_data['cart'],
                    status=models.DONE,
                )
        cart = order.cart
        if not models.CartItem.objects.filter(cart=cart).exists():
            return {
                'message': 'You cannot create an order',
            }
        cart.is_confirm = True
        cart.save()
        return {
            'order_id': order.id,
            'status': order.status,
            'created_at': order.created_at,
            'cart': CartSerializer(order.cart).data,
            'cart_is_confirm': cart.is_confirm,
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
        order.save()

        return {
            'message': 'Order status successfully changed'
        }


class OrderUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(method_name='get_full_name')

    class Meta:
        model = User
        fields = ['full_name', 'type']

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


class OrderCartItemListSerializer(serializers.ModelSerializer):
    food = serializers.CharField(source='food.name')

    class Meta:
        model = models.CartItem
        fields = ['id', 'food', 'quantity']


class OrderCartListSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField(method_name='get_cart_items')
    table_number = serializers.IntegerField(source='table.number')

    class Meta:
        model = models.Cart
        fields = [
            'id', 'table_number', 'cart_items'
        ]

    def get_cart_items(self, obj):
        cart_items = models.CartItem.objects.filter(cart=obj)
        return OrderCartItemListSerializer(cart_items, many=True).data


class OrderListSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField(method_name='get_cart')
    total_price = serializers.IntegerField(source='cart.total_price')
    user = OrderUserSerializer(source='cart.user')
    date = serializers.SerializerMethodField(method_name='get_date')
    time = serializers.SerializerMethodField(method_name='get_time')

    class Meta:
        model = models.Order
        fields = [
            'id', 'cart', 'date', 'time', 'total_price', 'user'
        ]

    def get_cart(self, obj):
        cart = obj.cart
        return OrderCartListSerializer(cart).data

    def get_date(self, obj):
        return obj.created_at.date()

    def get_time(self, obj):
        return obj.created_at.time()


class OrderSerializer(serializers.ModelSerializer):
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
        return f'{total_price} UZS'


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
        order.cart.table.is_busy = False
        order.cart.table.save()
        order.save()

        return {
            'message': 'Order is successfully confirmed'
        }