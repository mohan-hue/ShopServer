
from ..utils.import_header import *
from Shop.models import ProductCollect, User, UserToProductCollect
from Shop.utils.filters import BaseProductFilter

class ProductCollectFilter(BaseProductFilter):
    """
    查询条件区间过滤
    """
    # 模糊查询 (不区分大小写的包含)
    name = django_filters.CharFilter(field_name='product_name', lookup_expr='icontains',
                                     label="产品名称", help_text="模糊查询")

    class Meta:
        model = ProductCollect
        # 这里列出模型中实际存在的字段，不能包含非模型字段，而且这里的都是精确查询
        fields = ["product_collect_id", "product_classify_id",
                  "product_id"]


class ProductCollectSerializer(CustomModelSerializer):
    """
    产品收藏序列化器
    """

    class Meta:
        model = ProductCollect
        fields = "__all__"
        # exclude = ["create_user_id", "modify_user_id", "is_deleted"]
        read_only_fields = ["product_collect_id"]


class ProductCollectViewSet(CustomModelViewSet):
    """
    产品收藏接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = ProductCollect.objects.exclude().all()
    serializer_class = ProductCollectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ProductCollectFilter

    def perform_create(self, serializer):
        """
        重写perform_create执行创建方法，用于更新user表中的shop外键
        :param serializer: 序列化器提交的验证后的数据
        :return:
        """
        instance = serializer.save()
        user_instance = User.objects.get(pk=self.request.user.user_id)
        user2product_collect = UserToProductCollect.objects.create(user=user_instance,
                                                               product_collect=instance)
        user2product_collect.save()

