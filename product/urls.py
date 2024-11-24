from django.urls import path

from product import views

urlpatterns = [
    # product category
    path('product-category/list/', views.ProductCategoryListApiView.as_view(), name='product-category-list'),
    path('product-category/<category_id>/', views.ProductListByCategoryApiView.as_view(), name='product-category-list'),
    # product
    path('product/create/', views.ProductCreateApiView.as_view(), name='product-create'),
    path('product/list/', views.ProductListApiView.as_view(), name='product-category-list'),
    # cart-item
    path('cart-item/create/', views.ProductCartItemCreateApiView.as_view(), name='product-cart-item-create'),
    path('cart-item/<int:cart_item_id>/update/', views.ProductCartItemUpdateApiView.as_view(), name='product-cart-item-update'),
    path('cart-item/<int:id>/delete/', views.ProductCartItemDeleteApiView.as_view(), name='product-cart-item-delete'),
    # cart
    path('cart/create/', views.GetOrderApiView.as_view(), name='get_order'),
    # order
    path('order/create/', views.ProductOrderCreateApiView.as_view(), name='product-order-create'),
    path('order/confirm/', views.ProductOrderConfirmApiView.as_view(), name='product-order-confirm'),
    path('order/list/is-confirm/', views.ProductOrderIsConfirmApiView.as_view(), name='product-order-is-confirm'),
    path('order/list/is-not-confirm/', views.ProductOrderIsNotConfirmApiView.as_view(), name='product-order-is-confirm'),

    path('get-unit-status/', views.GetUnitStatusApiView.as_view(), name='get-unit-status'),
]