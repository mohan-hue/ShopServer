
from ..utils.import_header import *
from Shop.models import ProductOrder
from Shop.models import UserToProductOrder
from Shop.models import User


class ProductOrderSerializer(CustomModelSerializer):
    """
    产品订单序列化器
    """

    class Meta:
        model = ProductOrder
        # fields = "__all__"
        exclude = ["create_user_id", "modify_user_id", "is_cancel", "is_finish", "after_sale",
                   "non_payment", "wait_for_receiving"]
        read_only_fields = ["product_order_id"]


class ProductOrderViewSet(CustomModelViewSet):
    """
    产品订单接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    """
    冗余的字段在更新时需要保证数据的一致性
    """
    queryset = ProductOrder.objects.exclude().all()
    serializer_class = ProductOrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["product_order_id", "product_name", "shop_id", "non_payment",
                        "wait_for_receiving", "after_sale", "is_finish", "is_cancel",
                        "product_classify_name", "product_classify_id", "product_id"]

    def perform_create(self, serializer):
        """
        重写perform_create执行创建方法，用于更新user表中的shop外键
        :param serializer: 序列化器提交的验证后的数据
        :return:
        """
        instance = serializer.save()
        user_instance = User.objects.get(pk=self.request.user.user_id)
        user2product_order = UserToProductOrder.objects.create(user=user_instance,
                                                               product_order=instance)
        user2product_order.save()

