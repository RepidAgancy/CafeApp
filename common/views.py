from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, views
from rest_framework.response import Response

from common import models, serializers, permissions, filters
from accounts.models import CASHIER, WAITER


class TableListApiView(generics.ListAPIView):
    serializer_class = serializers.TableListSerializer
    permission_classes = [permissions.IsCashierOrWaiter]
    pagination_class = None

    def get_queryset(self):
        if self.request.user.type == WAITER:
            return models.Table.objects.exclude(number=0).order_by('number')
        else:
            return models.Table.objects.filter(number=0)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class TableGetApiView(generics.GenericAPIView):
    serializer_class = serializers.TableGetSerializer
    permission_classes = [permissions.IsCashierOrWaiter]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodListApiView(generics.ListAPIView):
    serializer_class = serializers.FoodListSerializer
    queryset = models.Food.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.FoodFilter
    pagination_class = None
    permission_classes = [permissions.IsCashierOrWaiter]


class FoodDetailApiView(generics.RetrieveAPIView):
    serializer_class = serializers.FoodDetailSerializer
    permission_classes = [permissions.IsCashierOrWaiter]
    queryset = models.Food.objects.all()
    lookup_field = 'id'


class FoodCategoryListApiView(generics.ListAPIView):
    queryset = models.CategoryFood.objects.all()
    serializer_class = serializers.FoodCategorySerializer
    permission_classes = [permissions.IsCashierOrWaiter]
    pagination_class = None


class FoodListByCategoryApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsCashierOrWaiter]
    serializer_class = serializers.FoodListByCategorySerializer
    pagination_class = None

    def get(self, request, category_id):
        try:
            category = models.CategoryFood.objects.get(id=category_id)
        except models.CategoryFood.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        foods = models.Food.objects.filter(category=category)

        page = self.paginate_queryset(foods)  # Apply pagination to the queryset
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)  # Return paginated response

        serializer = self.get_serializer(foods, many=True)
        return Response(serializer.data)


class CartItemCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.CartItemCreateSerializer
    permission_classes = [permissions.IsCashierOrWaiter]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemEditApiView(generics.GenericAPIView):
    serializer_class = serializers.CartItemUpdateSerializer
    permission_classes = [permissions.IsCashierOrWaiter]
    queryset = models.CartItem.objects.all()

    def patch(self, request, cart_item_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'cart_item_id': cart_item_id, 'request': request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemDeleteApiView(generics.GenericAPIView):
    # serializer_class = serializers.CartItemUpdateSerializer
    permission_classes = [permissions.IsCashierOrWaiter]
    queryset = models.CartItem.objects.all()

    def delete(self, request, cart_item_id, *args, **kwargs):
        try:
            cart_item = models.CartItem.objects.get(pk=cart_item_id)
        except models.CartItem.DoesNotExist:
            return Response({'message': 'cart item not found'},status=status.HTTP_404_NOT_FOUND)
        if cart_item.cart.is_confirm:
            return Response({'message': 'You can not delete this cart item'})
        else:
            if cart_item.cart.user == request.user:
                food_price = cart_item.food.price
                food_quantity = cart_item.quantity
                cart_total_price = cart_item.cart.total_price
                total_price = cart_total_price - (food_price * food_quantity)
                cart_item.cart.total_price = total_price
                cart_item.cart.save()
                cart_item.delete()
        return Response({'message': 'Cart item successfully deleted'}, status=status.HTTP_200_OK)


class CartDetailApiView(generics.RetrieveAPIView):
    serializer_class = serializers.CartSerializer
    queryset = models.Cart.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsCashierOrWaiter]


class OrderCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderCreateSerializer
    permission_classes = [permissions.IsCashierOrWaiter]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderConfirmedApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderChangeStatusSerializer
    permission_classes = [permissions.IsCashierOrWaiter]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListInProcessApiView(generics.ListAPIView):
    serializer_class = serializers.OrderListSerializer
    permission_classes = [permissions.IsCashierOrWaiter]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.OrderListInProcessFilter

    def get_queryset(self):
        return models.Order.objects.filter(
            status=models.IN_PROCESS,
            cart__user=self.request.user
        )


class OrderListIsDoneApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderListSerializer
    permission_classes = [permissions.IsCashierOrWaiter]
    pagination_class = None

    def get(self, request):
        order = models.Order.objects.filter(status=models.DONE, cart__user=request.user, is_confirm=False)
        serializer = self.get_serializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FinishDayApiView(views.APIView):
    permission_classes = [permissions.IsWaiter, ]

    def post(self, request):
        user = request.user
        today = timezone.now().date()
        orders = models.Order.objects.filter(cart__user=user, status=models.IN_PROCESS)
        if not orders.exists():
            last_day_orders = models.Order.objects.filter(created_at__date=today, status=models.DONE, cart__user=user)
            orders = serializers.OrderListSerializer(last_day_orders, many=True).data
            total_price = 0
            for order in orders:
                total_price += float(order['cart']['total_price'])
            ofitsant_kpi = (total_price / 100) * 10
            data = {
                'sana': today,
                "orders": last_day_orders.count(),
                'percentage_for': 10,
                'total_price': total_price,
                'ofitsant_kpi': ofitsant_kpi,
            }
            return Response(data)
        else:
            return Response({'message': 'Waiter orders in process'}, status=status.HTTP_400_BAD_REQUEST)


class OrderConfirmApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderFoodConfirmSerializer
    permission_classes = [permissions.IsCashier]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderIsConfirmListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsCashier]
    serializer_class = serializers.OrderListSerializer
    pagination_class = None

    def get_queryset(self):
        return models.Order.objects.filter(cart__user=self.request.user, is_confirm=True)


class OrderIsNotConfirmListApiView(views.APIView):
    permission_classes = [permissions.IsCashier]

    def get(self, request):
        orders = models.Order.objects.filter(cart__user=request.user, is_confirm=False, status=models.DONE)
        print(request.user)
        serializer = serializers.OrderListSerializer(orders, many=True)
        return Response(serializer.data)


class CashierFinishDayApiView(views.APIView):
    permission_classes = [permissions.IsCashier]

    def post(self, request):
        today = timezone.now().date()
        if models.Order.objects.filter(is_confirm=False):
            return Response({'message': 'Siz kunni yakunlay olmaysiz qachonki buyurtmalar toliq tugatilmaguncha'})
        orders = models.Order.objects.filter(created_at__date=today)
        delivery_orders = models.Order.objects.filter(cart__user=request.user, created_at__date=today).count()
        total_price = 0
        for order in orders:
            total_price += order.cart.total_price

        data = {
            'sana': today,
            'orders_count': orders.count(),
            'delivery': delivery_orders,
            'total_price': total_price,
            'cashier': f'{request.user.first_name} {request.user.last_name}',
        }
        return Response(data, status=status.HTTP_200_OK)