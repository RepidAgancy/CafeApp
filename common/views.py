from lib2to3.fixes.fix_input import context

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response

from common import models, serializers, permissions, filters


class TableListApiView(generics.ListAPIView):
    serializer_class = serializers.TableListSerializer
    queryset = models.Table.objects.all()
    permission_classes = [permissions.IsWaiter, ]


class TableGetApiView(generics.GenericAPIView):
    serializer_class = serializers.TableGetSerializer
    permission_classes = [permissions.IsWaiter, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodListApiView(generics.ListAPIView):
    serializer_class = serializers.FoodListSerializer
    queryset = models.Food.objects.all()
    permission_classes = [permissions.IsWaiter, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.FoodFilter


class FoodDetailApiView(generics.RetrieveAPIView):
    serializer_class = serializers.FoodDetailSerializer
    permission_classes = [permissions.IsWaiter, ]
    queryset = models.Food.objects.all()
    lookup_field = 'id'


class CartItemCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.CartItemCreateSerializer
    permission_classes = [permissions.IsWaiter, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemEditApiView(generics.GenericAPIView):
    serializer_class = serializers.CartItemUpdateSerializer
    permission_classes = [permissions.IsWaiter, ]
    queryset = models.CartItem.objects.all()

    def patch(self, request, cart_item_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'cart_item_id': cart_item_id, 'request': request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemDeleteApiView(generics.GenericAPIView):
    serializer_class = serializers.CartItemUpdateSerializer
    permission_classes = [permissions.IsWaiter, ]
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
    permission_classes = [permissions.IsWaiter, ]


class OrderCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderCreateSerializer
    permission_classes = [permissions.IsWaiter, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderConfirmedApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderConfirmedSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderListSerializer
    permission_classes = [permissions.IsWaiter, ]

    def get(self, request):
        order = models.Order.objects.all()
        serializer = self.get_serializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)