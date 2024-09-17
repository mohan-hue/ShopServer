
from ..utils.import_header import *
from Shop.models import BankCardID
from Shop.models import User


class BankCardIDSerializer(CustomModelSerializer):
    """
    银行卡序列化器
    """

    class Meta:
        model = BankCardID
        # fields = "__all__"
        exclude = ["create_user_id", "modify_user_id", "is_deleted"]
        read_only_fields = ["user", "bank_card_id"]


class BankCardIDViewSet(CustomModelViewSet):
    """
    银行卡接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = BankCardID.objects.exclude().all()
    serializer_class = BankCardIDSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['user', 'bank_card_id']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["user"] = User.objects.get(pk=self.request.user.user_id)
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg="新增成功")
