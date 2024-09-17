
from ..utils.import_header import *
from Shop.models import ReceivingAddress
from Shop.models import User


class ReceivingAddressSerializer(CustomModelSerializer):
    """
    收货地址序列化器
    """

    class Meta:
        model = ReceivingAddress
        fields = "__all__"
        read_only_fields = ["user"]


class ReceivingAddressViewSet(CustomModelViewSet):
    """
    收货地址接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = ReceivingAddress.objects.exclude().all()
    serializer_class = ReceivingAddressSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['user']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = User.objects.get(pk=request.user.user_id)
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg="新增成功")
