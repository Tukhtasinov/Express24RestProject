from django.db.models import Q
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.views import get_user_model

from accounts.models import Role, UserRole
from accounts.permissions import IsAdminPermission, IsAdminOrDeliverPermission
from accounts.serializers import UserSerializer
from express24.models import Category, Product, ShoppingCard, Address, Order
from express24.serializers import CategorySerializer, ProductSerializer, ProductSerializerForAdmin, \
    ShoppingCartSerializer, OrderSerializer, OrderComment, RoleSerializer, ProductSerializerGet, UserRoleSerializer, \
    OrderSerializerForPatch

User = get_user_model()


class CategoryAPIView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serialized = CategorySerializer(categories, many=True)

        return Response(serialized.data)


class ProductGenericAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductSerializer

    def get(self, request, category_id):
        products = Product.objects.filter(category__id=category_id)
        serialized = self.get_serializer(products, many=True)

        return Response(serialized.data)


class ProductForHomeGenericAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductSerializerGet

    def get(self, request):
        categories = Category.objects.all()[:3]
        data = []
        products = {}
        category_list = {}
        for category in categories:
            product = Product.objects.filter(category__id=category.id)
            serialized = self.get_serializer(product, many=True)
            category_list.update({'category': CategorySerializer(category).data})
            category_list.update({'product': serialized.data})
            data.append(category_list)
            category_list = {}
            products.update({'data': data})

        return Response(products.get('data'))


class ProductAddAdminGenericAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminPermission)
    serializer_class = ProductSerializerForAdmin

    def post(self, request):

        product = self.get_serializer(data=request.data)
        if product.is_valid(raise_exception=True):
            product.save()

            return Response(product.data, status=status.HTTP_201_CREATED)
        else:
            return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryAddAdminGenericAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminPermission, )
    serializer_class = CategorySerializer

    def post(self, request):
        category = self.get_serializer(data=request.data)
        if category.is_valid():
            category.save()
            return Response(category.data, status=status.HTTP_201_CREATED)
        else:
            return Response(category.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductEditAdminGenericAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminPermission)
    serializer_class = ProductSerializerForAdmin

    def get_product(self, pk):
        return Product.objects.get(pk=pk)

    def put(self, request, product_id):
        product = self.get_product(product_id)

        try:
            product_serialized = self.get_serializer(product, data=request.data)
            product_serialized.is_valiq(raise_exception=True)
            product_serialized.save()

        except Exception as e:
            return Response({'success': False, 'error': e}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': True, 'message': 'Product editted successfully'})

    def patch(self, request, product_id):
        product = self.get_product(product_id)

        try:
            product_serialized = ProductSerializerForAdmin(product, data=request.data, partial=True)
            product_serialized.is_valid(raise_exception=True)
            product_serialized.save()

        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': True, 'message': 'Product editted succesfully!'})

    def delete(self, request, product_id):
        product = self.get_product(product_id)
        product.delete()
        return Response({'success': True, 'message': 'Product deleted successfully'})


class ShoppingCartGenericAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShoppingCartSerializer

    def get_shoppingCart(self, id):
        return ShoppingCard.objects.get(pk=id)

    def post(self, request, pk=None):
        data = request.data
        data.update({'user': request.user.id})
        print(data)
        shopping_cart = self.get_serializer(data=data)
        try:
            shopping_cart.is_valid(raise_exception=True)
            shopping_cart.validated_data['user'] = request.user
            shopping_cart.save()

        except Exception as e:
            print('Error ', e)
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': True, 'message': 'Product added successfully'})

    def patch(self, request, pk):
        shopping_cart = self.get_shoppingCart(pk)
        serialized = self.get_serializer(shopping_cart, data=request.data, partial=True)
        try:
            serialized.is_valid(raise_exception=True)
            serialized.save()

        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': True}, status=status.HTTP_205_RESET_CONTENT)

    def delete(self, request, pk):
        shopping_cart = self.get_shoppingCart(pk)
        shopping_cart.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class ShoppingCartForClient(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShoppingCartSerializer

    def get(self, request):
        shopping_cart = ShoppingCard.objects.filter(Q(user__id=request.user.id) & Q(is_ordered=0))
        serialized = self.serializer_class(shopping_cart, many=True)

        return Response({'success': True, 'serialized': serialized.data}, status=status.HTTP_200_OK)


class OrderGenericAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get(self, request):
        ordered_products = ShoppingCard.objects.filter(Q(user__id=request.user.id) & Q(is_ordered=0))

        try:
            for ordered_product in ordered_products:
                address = Address.objects.filter(user__id=request.user.id).first()
                order_data = {
                    'user': request.user.id,
                    'product': ordered_product.product.id,
                    'count': ordered_product.count,
                    'comment': '',
                    'address_id': None,
                    'status': False,
                }
                order_serializer = self.serializer_class(data=order_data)
                order_serializer.is_valid(raise_exception=True)
                order_serializer.save()

            ordered_products.update(is_ordered=1)

            return Response({'success': True, 'message': 'Orders created successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'success': False, 'exception': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderModelGet(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminPermission)
    serializer_class = OrderSerializer

    def get(self, request):
        ordered_products = Order.objects.filter(status=0)
        order_serialized = OrderComment(ordered_products, many=True)

        return Response(order_serialized.data)


class DeliveredProductAPI(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminPermission)

    def get(self, request):
        delivered_products = Order.objects.filter(status=1)
        deli_serializes = OrderSerializer(delivered_products, many=True)

        return Response(deli_serializes.data)


class DeliveredProduct(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrDeliverPermission)
    serializer_class = OrderSerializerForPatch

    def patch(self, request):
        order_id = request.data.get('id')
        order = Order.objects.get(id=order_id)
        serialized = self.get_serializer(order, data=request.data, partial=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Response({'success': True})


class RoleGenericAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminPermission)
    serializer_class = RoleSerializer

    def get(self, request):
        role = Role.objects.all()
        serialized = self.get_serializer(role, many=True)

        return Response(serialized.data)

    def post(self, request):
        role = self.get_serializer(data=request.data)
        role.is_valid(raise_exception=True)
        role.save()

        return Response(role.data)


class GiveRoleForUSerByAdmin(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminPermission)
    serializer_class = UserRoleSerializer

    def post(self, request):
        user_role = self.get_serializer(data=request.data)
        user_role.is_valid(raise_exception=True)
        user_role.save()

        return Response(user_role.data)


class AllUsersForAdmin(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminPermission)
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        user_serialized = self.get_serializer(users, many=True)

        return Response(user_serialized.data)


