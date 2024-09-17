
from Shop.utils.import_header import *
from Shop.models import MaternalAndChild
from Shop.utils.filters import BaseProductFilter

class MaternalAndChildFilter(BaseProductFilter):
    """
    查询条件区间过滤
    """
    class Meta:
        model = MaternalAndChild
        # 这里列出模型中实际存在的字段，不能包含非模型字段，而且这里的都是精确查询
        fields = ["product_id", "product_classify_name", "product_classify_id"]

class MaternalAndChildSerializer(CustomModelSerializer):
    """
    母婴序列化器
    """

    class Meta:
        model = MaternalAndChild
        fields = "__all__"
        # exclude = ["create_user_id", "modify_user_id", "is_deleted"]
        # read_only_fields = ["shop_id"]


class MaternalAndChildViewSet(CustomModelViewSet):
    """
    母婴接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = MaternalAndChild.objects.exclude().all()
    serializer_class = MaternalAndChildSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = MaternalAndChildFilter
