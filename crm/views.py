from datetime import timedelta, datetime
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import get_language

from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from crm import serializers, models, permissions
from crm.utils import calculate_percentage_change
from crm.pagination import CustomPagination
from product.models import OrderProduct, APPROVED, Product
from common.models import Order, PROFIT, EXPENSE, DONE, Food, CategoryFood
from accounts.models import User, WAITER, CASHIER, ADMIN


class StatisticsApiView(generics.GenericAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = serializers.StartandEndDateSerializer

    def get(self, request):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        income_orders_today = OrderProduct.objects.filter(type=PROFIT, is_confirm=True, status=APPROVED,
                                                    created_at__date=today)
        expense_orders_today = Order.objects.filter(type=EXPENSE, is_confirm=True, status=DONE, created_at__date=today)
        total_income_today = sum(order.cart.total_price for order in income_orders_today)
        total_expense_today = sum(order.cart.total_price for order in expense_orders_today)
        income_orders_yesterday = OrderProduct.objects.filter(type=PROFIT, is_confirm=True, status=APPROVED,
                                                    created_at__date=yesterday)
        expense_orders_yesterday = Order.objects.filter(type=EXPENSE, is_confirm=True, status=DONE,
                                                        created_at__date=yesterday)
        total_income_yesterday = sum(order.cart.total_price for order in income_orders_yesterday)
        total_expense_yesterday = sum(order.cart.total_price for order in expense_orders_yesterday)
        income_change_percentage = calculate_percentage_change(total_income_today, total_income_yesterday)
        expense_change_percentage = calculate_percentage_change(total_expense_today, total_expense_yesterday)
        employees = User.objects.count()
        customers_today = Order.objects.filter(is_confirm=True, status=APPROVED, created_at__date=today).count()
        data = {
            'total_income': {
                'value': total_income_today,
                'percentage': income_change_percentage,
            },
            'total_expense': {
                'value': total_expense_today,
                'percentage': expense_change_percentage,
            },
            'employees': employees,
            'customers_today': customers_today,
        }

        return Response(data)
    
    def post(self, request,*args,**kwargs):
        # Deserialize and validate input data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated data
        start_date = serializer.validated_data.get('start_date',datetime.now().strftime("%Y-%m-%d"))
        end_date = serializer.validated_data.get('end_date', datetime.now().strftime("%Y-%m-%d"))

        # Query data based on the provided date range
        income_orders = OrderProduct.objects.filter(
            type=PROFIT, is_confirm=True, status=APPROVED,
            created_at__date__range=(start_date, end_date)
        )
        expense_orders = Order.objects.filter(
            type=EXPENSE, is_confirm=True, status=DONE,
            created_at__date__range=(start_date, end_date)
        )

        total_income = sum(order.cart.total_price for order in income_orders)
        total_expense = sum(order.cart.total_price for order in expense_orders)

        # Additional data
        employees = User.objects.count()
        customers = Order.objects.filter(
            is_confirm=True, status=APPROVED,
            created_at__date__range=(start_date, end_date)
        ).count()

        # Prepare response data
        data = {
            'total_income': {
                'value': total_income,
            },
            'total_expense': {
                'value': total_expense,
            },
            'employees': employees,
            'customers': customers,
        }

        return Response(data)


class MonthlyStatisticsAPIView(views.APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        monthly_income = (
            OrderProduct.objects
            .filter(type=PROFIT, is_confirm=True, status=APPROVED)
            .annotate(month=ExtractMonth('created_at'))
            .values('month')
            .annotate(total_income=Sum('cart__total_price'))
            .order_by('month')
        )

        monthly_expense = (
            Order.objects
            .filter(type=EXPENSE, is_confirm=True, status=DONE)
            .annotate(month=ExtractMonth('created_at'))
            .values('month')
            .annotate(total_expense=Sum('cart__total_price'))
            .order_by('month')
        )

        income_data = {item['month']: item['total_income'] for item in monthly_income}
        expense_data = {item['month']: item['total_expense'] for item in monthly_expense}

        data = {
            "months": list(range(1, 13)),
            "series": [
                {"name": "Income", "data": [income_data.get(month, 0) for month in range(1, 13)]},
                {"name": "Expense", "data": [expense_data.get(month, 0) for month in range(1, 13)]}
            ]
        }

        return Response(data)


class ChartActivityIncomeApiView(views.APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        today = timezone.now().date()
        orders = Order.objects.filter(type=PROFIT, is_confirm=True, status=DONE, created_at__date=today)
        waiter_orders = orders.filter(cart__user__type=WAITER)
        cashier_orders = orders.filter(cart__user__type=CASHIER)
        total_price = 0
        from_within = 0
        delivery = 0
        for order in orders:
            total_price += order.cart.total_price
        for waiter_order in waiter_orders:
            from_within += waiter_order.cart.total_price
        for cashier_order in cashier_orders:
            delivery += cashier_order.cart.total_price
        delivery_percentage = (delivery / total_price) * 100 if delivery else 0
        from_within_percentage = (from_within / total_price) * 100 if from_within else 0

        data = {
            'total_price': total_price,
            'from_within':{
                'value': from_within,
                'percentage': from_within_percentage,
            },
            'delivery': {
                'value': delivery,
                'percentage': delivery_percentage,
            },
        }
        return Response(data)


class SearchAPIView(generics.GenericAPIView):
    serializer_class = serializers.SearchSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)  
        
        query = serializer.validated_data.get('query', '')
        

        employees = User.objects.filter(Q(username__icontains=query) | 
                                        Q(first_name__icontains=query)|
                                        Q(last_name__icontains=query))
        
        current_language = get_language()
        foods = Food.objects.filter(
            Q(name__icontains = query) |
            Q(**{f'food_info_{current_language}__icontains': query})
        )
        products = Product.objects.filter(
            Q(**{f'name_{current_language}__icontains': query})
        )
        

        employee_serializer = serializers.UserListSerializer(employees, many=True)
        food_serializer = serializers.FoodSerializer(foods, many=True)
        product_serializer = serializers.ProductSerializer(products, many=True)
        
        return Response({
            'employees': employee_serializer.data,
            'foods': food_serializer.data,
            'products': product_serializer.data,
        }, status=status.HTTP_200_OK)
    

class ValidateAccessTokenView(generics.GenericAPIView):
    serializer_class = serializers.ValidateAccessToken
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['access_token']
        if not token:
            return Response({"valid": False, "message": "Token not provided"}, status=400)
        
        try:
            AccessToken(token)
            return Response({"valid": True}, status=200)
        except Exception as e:
            return Response({"valid": False, "message": str(e)}, status=401)
    

class EmployeesListApiView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.filter().exclude(type=ADMIN)
    serializer_class = serializers.UserListSerializer
    pagination_class = CustomPagination


class EmployeeDeleteApiView(views.APIView):
    permission_classes = (permissions.IsAdminUser,)

    def delete(self, request, pk):
        try:
            employee = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.EmployeeCreateSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.EmployeeUpdateSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()


class FoodListApiView(generics.ListAPIView):
    serializer_class = serializers.FoodSerializer
    queryset = Food.objects.all()
    permission_classes = (permissions.IsAdminUser,)


class FoodCategoryListView(generics.ListAPIView):
    serializer_class = serializers.FoodCategoryListSerializer
    queryset = CategoryFood.objects.all()
    permission_classes = (permissions.IsAdminUser, )


class FoodCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.FoodCreateUpdateSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.FoodCreateUpdateSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = Food.objects.all()
    lookup_field = 'pk'


class FoodDeleteApiView(views.APIView):
    permission_classes = (permissions.IsAdminUser,)

    def delete(self, request, pk):
        try:
            food = Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            return Response({'message': 'Food not found'}, status=status.HTTP_404_NOT_FOUND)
        food.delete()
        return Response({'message': 'Food successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAdminUser,)


class PaymentEmployeeSalaryCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.PaymentEmployeeSalaryCreateSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({'message': 'Payment successfull added'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.PaymentCreateSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = models.Payment.objects.all()


class PaymentHistoryListApiView(generics.ListAPIView):
    serializer_class = serializers.PaymentHistoryListSerializer
    queryset = models.Payment.objects.all().order_by('-created_at')
    permission_classes = (permissions.IsAdminUser,)


class PaymentCategoryApiView(views.APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        payment_type = models.Payment.category_list()
        data = {
            'payment_type': payment_type,
        }
        return Response(data)