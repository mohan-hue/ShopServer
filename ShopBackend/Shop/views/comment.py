
from ..utils.import_header import *
from Shop.models import Comment, User, UserToComment


class CommentSerializer(CustomModelSerializer):
    """
    评论序列化器
    """

    class Meta:
        model = Comment
        fields = "__all__"
        # exclude = ["create_user_id", "modify_user_id", "is_deleted"]
        read_only_fields = ["comment_id"]


class CommentViewSet(CustomModelViewSet):
    """
    评论接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = Comment.objects.exclude().all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['comment_id']

    def perform_create(self, serializer):
        """
        重写perform_create执行创建方法，用于更新user表中的shop外键
        :param serializer: 序列化器提交的验证后的数据
        :return:
        """
        instance = serializer.save()
        user_instance = User.objects.get(pk=self.request.user.user_id)
        user2comment = UserToComment.objects.create(user=user_instance,
                                                               comment=instance)
        user2comment.save()
