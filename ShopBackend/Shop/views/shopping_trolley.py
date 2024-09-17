from ..utils.import_header import *
from Shop.models import ShoppingTrolley, User, UserToShoppingTrolley
from ..utils.filters import BaseProductFilter

class ShoppingTrolleyFilter(BaseProductFilter):
    """
    查询条件区间过滤
    """

    # 模糊查询 (不区分大小写的包含)
    name = django_filters.CharFilter(field_name='product_name', lookup_expr='icontains',
                                     label="产品名称", help_text="模糊查询")

    class Meta:
        model = ShoppingTrolley
        # 这里列出模型中实际存在的字段，不能包含非模型字段，而且这里的都是精确查询
        fields = ["product_id", "shop_id"]

class ShoppingTrolleySerializer(CustomModelSerializer):
    """
    购物车序列化器
    """

    class Meta:
        model = ShoppingTrolley
        fields = "__all__"
        # exclude = ["create_user_id", "modify_user_id", "is_deleted"]
        read_only_fields = ["shopping_trolley_id"]


class ShoppingTrolleyViewSet(CustomModelViewSet):
    """
    购物车接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = ShoppingTrolley.objects.exclude().all()
    serializer_class = ShoppingTrolleySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ShoppingTrolleyFilter

    def perform_create(self, serializer):
        """
        重写perform_create执行创建方法，用于更新user表中的shop外键
        :param serializer: 序列化器提交的验证后的数据
        :return:
        """
        instance = serializer.save()
        user_instance = User.objects.get(pk=self.request.user.user_id)
        user2shopping_trolley = UserToShoppingTrolley.objects.create(user=user_instance,
                                                               shopping_trolley=instance)
        user2shopping_trolley.save()
