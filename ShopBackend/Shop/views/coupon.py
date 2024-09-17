
from ..utils.import_header import *
from Shop.models import Coupon, User, UserToCoupon


class CouponSerializer(CustomModelSerializer):
    """
    优惠券序列化器
    """

    class Meta:
        model = Coupon
        # fields = "__all__"
        exclude = ["create_user_id", "modify_user_id"]
        read_only_fields = ["coupon_id", "is_use", "is_valid"]


class CouponViewSet(CustomModelViewSet):
    """
    优惠券接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = Coupon.objects.exclude().all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["coupon_id", "coupon_name", "coupon_shop_id", "coupon_product_id",
                        "is_use", "is_valid", "product_classify_id", "is_superposition"]


    def perform_create(self, serializer):
        """
        重写perform_create执行创建方法，用于更新user表中的shop外键
        :param serializer: 序列化器提交的验证后的数据
        :return:
        """
        instance = serializer.save()
        user_instance = User.objects.get(pk=self.request.user.user_id)
        user2pcoupon = UserToCoupon.objects.create(user=user_instance,
                                                               coupon=instance)
        user2pcoupon.save()
