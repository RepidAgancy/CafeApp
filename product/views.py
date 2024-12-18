from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, views
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from product import models, serializers, permissions, filters


class ProductCategoryListApiView(views.APIView):
    permission_classes = [permissions.IsStorekeeper, ]

    @method_decorator(cache_page(60*5))
    def get(self, request):
        categories = models.CategoryProduct.objects.all()
        serializer = serializers.ProductCategoryListSerializer(categories, many=True)
        return Response(serializer.data)


class ProductListApiView(generics.ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = models.Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ProductFilter
    permission_classes = [permissions.IsStorekeeper, ]
    pagination_class = None

    @method_decorator(cache_page(60*5))
    def get(self, request):
        return super().get(request)


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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'cart_item_id', openapi.IN_PATH,
                description='cart item id',
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def patch(self, request, cart_item_id):
        serializer = self.get_serializer(data=request.data, context={'request': request, 'cart_item_id': cart_item_id})
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCartItemDeleteApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsStorekeeper, ]

    def delete(self, request, id):
        user = request.user
        try:
            cart_item = models.CartItemProduct.objects.get(id=id)
        except models.CartItemProduct.DoesNotExist:
            return Response({'message': 'Cart item is not found'}, status=status.HTTP_404_NOT_FOUND)
        if cart_item.cart.user != user:
            return Response({'message': 'You are not allowed to delete'})
        total_price = cart_item.cart.total_price - (cart_item.weight * cart_item.price)
        cart_item.cart.total_price = total_price
        cart_item.cart.save()
        cart_item.delete()
        return Response({'message': 'Cart Item successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class ProductCartDetailApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsStorekeeper,]
    serializer_class = serializers.ProductCartSerializer

    def get(self, request, id):
        cart = models.CartProduct.objects.filter(id=id).first()
        if cart:
            serializer = self.get_serializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Cart is not defined'}, status=status.HTTP_400_BAD_REQUEST)


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
    queryset = models.OrderProduct.objects.filter(is_confirm=True)
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

    @method_decorator(cache_page(60*1000))
    def get(self, request):
        data = {
            'status': models.CartItemProduct.get_unit_status()
        }
        return Response(data)


class ProductListByCategoryApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsStorekeeper]
    serializer_class = serializers.ProductListByCategorySerializer
    pagination_class = None

    @method_decorator(cache_page(60*5))
    def get(self, request, category_id):
        try:
            category = models.CategoryProduct.objects.get(id=category_id)
        except models.CategoryProduct.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        products = models.Product.objects.filter(category=category)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ProductDetailApiView(generics.GenericAPIView):
    serializer_class = serializers.ProductDetailSerializer

    def get(self, request, product_id):
        product = models.Product.objects.get(id=product_id)
        serializer = serializers.ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)