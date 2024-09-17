
from ..utils.import_header import *
from Shop.models import Classify


class ClassifySerializer(CustomModelSerializer):
    """
    分类序列化器
    """

    class Meta:
        model = Classify
        # fields = "__all__"
        exclude = ["create_user_id", "modify_user_id", "product_table"]
        read_only_fields = ["product_classify_id"]


class ClassifyViewSet(CustomModelViewSet):
    """
    分类接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = Classify.objects.exclude().all()
    serializer_class = ClassifySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["product_classify_id", "classify_name"]
