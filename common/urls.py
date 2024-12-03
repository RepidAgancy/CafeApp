
from django.urls import path

from common import views

urlpatterns = [
    # food category list
    path('category/list/', views.FoodCategoryListApiView.as_view(), name='food_category_list'),
    path('category/<int:category_id>/foods/', views.FoodListByCategoryApiView.as_view(), name='food_category_list'),
    # table
    path('table/list/', views.TableListApiView.as_view(), name='tables'),
    path('table/choose/', views.TableGetApiView.as_view(), name='table-get'),
    # food
    path('food/list/', views.FoodListApiView.as_view(), name='foods'),
    path('food/<int:id>/', views.FoodDetailApiView.as_view(), name='food-detail'),
    # cart-item
    path('cart-item/create/', views.CartItemCreateApiView.as_view(), name='cart-item-create'),
    path('cart-item/<int:cart_item_id>/update/', views.CartItemEditApiView.as_view(), name='cart-item-edit'),
    path('cart-item/<int:cart_item_id>/delete/', views.CartItemDeleteApiView.as_view(),name='cart-item-delete'),
    # cart
    path('cart/<int:id>/', views.CartDetailApiView.as_view(), name='cart-detail'),
    # order
    path('order/create/', views.OrderCreateApiView.as_view(), name='order-create'),
    path('order/change/status/', views.OrderConfirmedApiView.as_view(), name='order-change-status'),
    path('order/list/in-process/', views.OrderListInProcessApiView.as_view(), name='order-list-in-process'),
    path('order/list/is-done/', views.OrderListIsDoneApiView.as_view(), name='order-list-is-done'),
    path('order/confirm/', views.OrderConfirmApiView.as_view(), name='order-confirm'),
    path('order/list/is-confirm/', views.OrderIsConfirmListApiView.as_view(), name='order-list-is-confirm'),
    path('order/list/is-not-confirm/', views.OrderIsNotConfirmListApiView.as_view(), name='order-list-is-not-confirm'),
    # finish day
    path('finish-day/', views.FinishDayApiView.as_view(), name='finish-day'),
]