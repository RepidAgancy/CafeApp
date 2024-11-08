from tkinter.font import names

from django.urls import path

from common import views

urlpatterns = [
    path('tables/', views.TableListApiView.as_view(), name='tables'),
    path('table/get/', views.TableGetApiView.as_view(), name='table-get'),
    path('foods/', views.FoodListApiView.as_view(), name='foods'),
    path('food/<int:id>/', views.FoodDetailApiView.as_view(), name='food-detail'),
    path('cart-item/create/', views.CartItemCreateApiView.as_view(), name='cart-item-create'),
    path('cart-item/<int:cart_item_id>/', views.CartItemEditApiView.as_view(), name='cart-item-edit'),
    path('cart-item/<int:cart_item_id>/delete/', views.CartItemDeleteApiView.as_view(),name='cart-item-delete'),
    path('cart/<int:id>/', views.CartDetailApiView.as_view(), name='cart-detail'),
    path('order/create/', views.OrderCreateApiView.as_view(), name='order-create'),
    path('order/confirm/', views.OrderConfirmedApiView.as_view(), name='order-confirmed'),
    path('orders/in-process/', views.OrderListInProcessApiView.as_view(), name='orders'),
    path('orders/is-done/', views.OrderListIsDoneApiView.as_view(), name='orders'),
    path('finish-day/', views.FinishDayApiView.as_view(), name='finish-day'),
    # path('order-receipt/is-confimed/list/', views.OrderReceiptListIsConfirmedApiView.as_view(), name='order-reciept'),
    # path('order-receipt/is-not-confimed/list/', views.OrderReceiptListIsNotConfirmedApiView.as_view(), name='order-reciept'),
    # path('order-receipt/confim/', views.OrderReceiptConfirmApiView.as_view(), name='order-receipt'),
]