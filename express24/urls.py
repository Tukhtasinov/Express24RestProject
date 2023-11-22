from django.urls import path

from express24.views import (CategoryAPIView, ProductGenericAPIView, ProductAddAdminGenericAPIView,
                             ProductEditAdminGenericAPIView, CategoryAddAdminGenericAPIView, ShoppingCartGenericAPIView,
                             ShoppingCartForClient, OrderGenericAPIView, OrderModelGet,
                             DeliveredProduct, GiveRoleForUSerByAdmin, ProductForHomeGenericAPIView,
                             DeliveredProductAPI, RoleGenericAPIView, AllUsersForAdmin)

urlpatterns = [
    path('express24/categories/', CategoryAPIView.as_view(), name='categories'),
    path('express24/products/', ProductForHomeGenericAPIView.as_view(), name='products'),
    path('express24/all_users/', AllUsersForAdmin.as_view(), name='all_users'),
    path('express24/products/category/<int:category_id>', ProductGenericAPIView.as_view(), name='productWithCategoryId'),
    path('express24/product/add', ProductAddAdminGenericAPIView.as_view(), name='productAddAdmin'),
    path('express24/product/delivered', DeliveredProductAPI.as_view(), name='delivered'),
    path('express24/category/add', CategoryAddAdminGenericAPIView.as_view(), name='categoryAddAdmin'),
    path('express24/product/<int:product_id>/edit', ProductEditAdminGenericAPIView.as_view(), name='productEditAdmin'),
    path('express24/shopping_cart/<int:pk>', ShoppingCartGenericAPIView.as_view(), name='shopping-cart'),
    path('express24/shopping_cart/of-user/', ShoppingCartForClient.as_view(), name='shopping-cart-of-user'),
    path('express24/shopping_cart_to_order/', OrderGenericAPIView.as_view(), name='shopping-card_to_order'),
    path('express24/order-info-for-admin', OrderModelGet.as_view(), name='order-info-for-admin'),
    path('express24/product/delivered/post', DeliveredProduct.as_view(), name='delivered-product'),
    path('express24/roles/', RoleGenericAPIView.as_view(), name='roles'),
    path('express24/give-role-for-user/', GiveRoleForUSerByAdmin.as_view(), name='give-role')
]