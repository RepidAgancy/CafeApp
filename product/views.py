from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, views
from rest_framework.response import Response

from product import models, serializers, permissions, filters


class ProductCategoryListApiView(generics.ListAPIView):
    serializer_class = serializers.ProductCategoryListSerializer
    queryset = models.CategoryProduct.objects.all()
    permission_classes = [permissions.IsStorekeeper, ]
    pagination_class = None


class ProductListApiView(generics.ListAPIView):
    serializer_class = serializers.ProductCartItemSerializer
    queryset = models.Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ProductFilter
    permission_classes = [permissions.IsStorekeeper, ]
    pagination_class = None


class GetOrderApiView(views.APIView):
    permission_classes = [permissions.IsStorekeeper, ]

    def post(self, request):

        cart = models.CartProduct.objects.create(
            user=request.user,
        )
        return Response({'cart_id': cart.id}, status.HTTP_201_CREATED)


class ProductCartItemCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.ProductCartItemCreateSerializer
    permission_classes = [permissions.IsStorekeeper, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCartItemUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.ProductItemEditSerializer
    permission_classes = [permissions.IsStorekeeper, ]

    def patch(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCartItemDeleteApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsStorekeeper, ]

    def delete(self, request):
        user = request.user
        try:
            cart_item = models.CartItemProduct.objects.get(id=id)
        except models.CartItemProduct.DoesNotExist:
            return Response({'message': 'Cart item is not found'}, status=status.HTTP_404_NOT_FOUND)
        if cart_item.cart.user != user:
            return Response({'message': 'You are not allowed to delete'})
        total_price = cart_item.cart.total_price - (cart_item.weight * cart_item.product.price)
        cart_item.cart.total_price = total_price
        cart_item.cart.save()
        cart_item.delete()
        return Response({'message': 'Cart Item successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class ProductOrderCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.ProductOrderCreateSerializer
    permission_classes = [permissions.IsStorekeeper, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductOrderConfirmApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderConfirmSerializer
    permission_classes = [permissions.IsStorekeeper, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductOrderIsConfirmApiView(generics.ListAPIView):
    serializer_class = serializers.ProductOrderListSerializer
    permission_classes = [permissions.IsStorekeeper, ]
    queryset = models.OrderProduct.objects.filter(is_confirm=True)
    pagination_class = None


class ProductOrderIsNotConfirmApiView(generics.ListAPIView):
    serializer_class = serializers.ProductOrderListSerializer
    permission_classes = [permissions.IsStorekeeper, ]
    queryset = models.OrderProduct.objects.filter(is_confirm=False)
    pagination_class = None


class ProductCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.ProductCreateSerializer
    permission_classes = [permissions.IsStorekeeper, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUnitStatusApiView(views.APIView):
    permission_classes = [permissions.IsStorekeeper, ]

    def get(self, request):
        data = {
            'status': models.CartItemProduct.get_unit_status()
        }
        return Response(data)