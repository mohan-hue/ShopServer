
from ..utils.import_header import *
from Shop.models import BrowsingHistory


class BrowsingHistorySerializer(CustomModelSerializer):
    """
    浏览历史序列化器
    """

    class Meta:
        model = BrowsingHistory
        fields = "__all__"
        # exclude = ["create_user_id", "modify_user_id", "is_deleted"]
        # read_only_fields = ["shop_id"]


class BrowsingHistoryViewSet(CustomModelViewSet):
    """
    浏览历史接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = BrowsingHistory.objects.exclude().all()
    serializer_class = BrowsingHistorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
