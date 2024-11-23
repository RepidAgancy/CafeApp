from django.urls import path

from crm import views


urlpatterns = [
    path('translations/<str:lang_code>/', views.get_translations, name='get_translations'),

    path('search/', views.SearchAPIView.as_view(), name='search'),
    path('statistics/', views.StatisticsApiView.as_view(), name='statistics'),
    path('statistics/monthly/', views.MonthlyStatisticsAPIView.as_view(), name='monthly_statistics'),
    path('statistics/chart-activity/', views.ChartActivityIncomeApiView.as_view(), name='chart_activity_income'),
    # employee
    path('employee/list/', views.EmployeesListApiView.as_view(), name='employees-list'),
    path('employee/<int:pk>/delete/', views.EmployeeDeleteApiView.as_view(), name='employee-delete'),
    path('employee/create/', views.EmployeeCreateApiView.as_view(), name='employee-create'),
    path('employee/<int:pk>/update/', views.EmployeeUpdateApiView.as_view(), name='employee-update'),
    # list
    path('food/list/', views.FoodListApiView.as_view(), name='food-list'),
    path('food/<int:pk>/', views.FoodDeleteApiView.as_view(), name='food-delete'),
    path('food/create/', views.FoodCreateApiView.as_view(), name='food-create'),
    path('food/<int:pk>/update/', views.FoodUpdateApiView.as_view(), name='food-update'),
    path('food/category-list/', views.FoodCategoryListView.as_view(), name='food-category-list'),
    # product
    path('product/list/', views.ProductListApiView.as_view(), name='product-list'),
    # payment
    path('payment/employee-salary/add/', views.PaymentEmployeeSalaryCreateApiView.as_view(), name='payment-employee-salary-add'),
    path('payment/add/', views.PaymentCreateApiView.as_view(), name='payment-add'),
    # payment-history
    path('payment/history/list/', views.PaymentHistoryListApiView.as_view(), name='payment-history-list'),
    # payment-type list
    path('paymeny/type/list/', views.PaymentCategoryApiView.as_view(), name='payment-category-list'),
    #validation for access token
    path('validate-accesstoken', views.ValidateAccessTokenView.as_view(), name='access-token-validate'),
]