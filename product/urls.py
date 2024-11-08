from django.urls import path

from product import views

urlpatterns = [
    path('product/create/', views.ProductCreateApiView.as_view(), name='product-create'),
    path('get-order/', views.GetOrderApiView.as_view(), name='get_order'),
    path('product-category/list/', views.ProductCategoryListApiView.as_view(), name='product-category-list'),
    path('list/', views.ProductCategoryListApiView.as_view(), name='product-category-list'),
    path('cart-item/create/', views.ProductCartItemCreateApiView.as_view(), name='product-cart-item-create'),
    path('cart-item/<int:cart_item_id>/update/', views.ProductCartItemUpdateApiView.as_view(), name='product-cart-item-update'),
    path('cart-item/<int:id>/delete/', views.ProductCartItemDeleteApiView.as_view(), name='product-cart-item-delete'),
    path('order/create/', views.ProductOrderCreateApiView.as_view(), name='product-order-create'),
    path('order/confirm/', views.ProductOrderConfirmApiView.as_view(), name='product-order-confirm'),
    path('order/is-confirm/list/', views.ProductOrderIsConfirmApiView.as_view(), name='product-order-is-confirm'),
    path('order/is-not-confirm/list/', views.ProductOrderIsNotConfirmApiView.as_view(), name='product-order-is-confirm'),
]