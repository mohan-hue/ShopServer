
from ..utils.import_header import *
from Shop.models import Reply


class ReplySerializer(CustomModelSerializer):
    """
    回复序列化器
    """

    class Meta:
        model = Reply
        fields = "__all__"
        # exclude = ["create_user_id", "modify_user_id", "is_deleted"]
        # read_only_fields = ["user_id"]


class ReplyViewSet(CustomModelViewSet):
    """
    回复接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = Reply.objects.exclude().all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["comment"]
