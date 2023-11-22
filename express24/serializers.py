from rest_framework.serializers import ModelSerializer

from accounts.models import Role, UserRole
from express24.models import Category, Product, ShoppingCard, Order


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializerGet(ModelSerializer):

    class Meta:
        model = Product
        exclude = ('category',)


class ProductSerializerForAdmin(ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('image',)


class ProductSerializerOnlyAdmin(ModelSerializer):

    class Meta:
        model = Product
        fields = ('count',)


class RoleSerializer(ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


class UserRoleSerializer(ModelSerializer):

    class Meta:
        model = UserRole
        fields = '__all__'


class ShoppingCartSerializer(ModelSerializer):
    # product = ProductSerializer()

    class Meta:
        model = ShoppingCard
        fields = '__all__'
        read_only_fields = ('user', 'is_ordered')


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('address_id', 'amount', '')


class OrderSerializerForPatch(ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'status')


class OrderComment(ModelSerializer):

    class Meta:
        model = Order
        exclude = ('address_id', 'ordered_at', 'status')





