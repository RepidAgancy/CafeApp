from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, views
from rest_framework.response import Response


from common import models, serializers, permissions, filters


class TableListApiView(generics.ListAPIView):
    serializer_class = serializers.TableListSerializer
    queryset = models.Table.objects.all()
    permission_classes = [permissions.IsWaiter or permissions.IsCashier]


class TableGetApiView(generics.GenericAPIView):
    serializer_class = serializers.TableGetSerializer
    permission_classes = [permissions.IsWaiter or permissions.IsCashier]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodListApiView(generics.ListAPIView):
    serializer_class = serializers.FoodListSerializer
    queryset = models.Food.objects.all()
    permission_classes = [permissions.IsWaiter or permissions.IsCashier]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.FoodFilter


class FoodDetailApiView(generics.RetrieveAPIView):
    serializer_class = serializers.FoodDetailSerializer
    permission_classes = [permissions.IsWaiter or permissions.IsCashier]
    queryset = models.Food.objects.all()
    lookup_field = 'id'


class CartItemCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.CartItemCreateSerializer
    permission_classes = [permissions.IsWaiter or permissions.IsCashier]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemEditApiView(generics.GenericAPIView):
    serializer_class = serializers.CartItemUpdateSerializer
    permission_classes = [permissions.IsWaiter or permissions.IsCashier]
    queryset = models.CartItem.objects.all()

    def patch(self, request, cart_item_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'cart_item_id': cart_item_id, 'request': request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemDeleteApiView(generics.GenericAPIView):
    serializer_class = serializers.CartItemUpdateSerializer
    permission_classes = [permissions.IsWaiter or permissions.IsCashier]
    queryset = models.CartItem.objects.all()

    def delete(self, request, cart_item_id, *args, **kwargs):
        try:
            cart_item = models.CartItem.objects.get(pk=cart_item_id)
        except models.CartItem.DoesNotExist:
            return Response({'message': 'cart item not found'},status=status.HTTP_404_NOT_FOUND)
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
    permission_classes = [permissions.IsWaiter or permissions.IsCashier]


class OrderCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderCreateSerializer
    permission_classes = [permissions.IsWaiter or permissions.IsCashier]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderConfirmedApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderConfirmedSerializer
    permission_classes = [permissions.IsWaiter or permissions.IsCashier]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListInProcessApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderListSerializer
    permission_classes = [permissions.IsWaiter or permissions.IsCashier]

    def get(self, request):
        order = models.Order.objects.filter(status=models.IN_PROCESS)
        serializer = self.get_serializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderListIsDoneApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderListSerializer
    permission_classes = [permissions.IsWaiter or permissions.IsCashier]

    def get(self, request):
        order = models.Order.objects.filter(status=models.DONE)
        serializer = self.get_serializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FinishDayApiView(views.APIView):
    permission_classes = [permissions.IsWaiter, ]

    def post(self, request):
        user = request.user
        today = timezone.now().date()
        last_day_orders = models.Order.objects.filter(created_at__date=today, status=models.DONE, cart__user=user)
        orders = serializers.OrderListSerializer(last_day_orders, many=True).data
        total_price = 0.000
        for order in orders:
            total_price += float(order['cart']['total_price'])
        ofitsant_kpi = (total_price / 100) * 10
        data = {
            "user": user.id,
            "orders": orders,
            'total_price': f'{total_price:.3f} UZS',
            'ofitsant_kpi': f'{ofitsant_kpi:.3f} UZS',
        }
        return Response(data)


