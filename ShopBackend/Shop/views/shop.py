from ..utils.import_header import *
from Shop.models import Shop, User, UserToShopCollect


class ShopSerializer(CustomModelSerializer):
    """
    店铺序列化器
    """

    class Meta:
        model = Shop
        # fields = "__all__"
        exclude = ["create_user_id", "modify_user_id", "is_deleted"]
        read_only_fields = ["shop_id"]


class UserToShopCollectSerializer(CustomModelSerializer):
    """
    用户店铺收藏序列化器
    """

    class Meta:
        model = UserToShopCollect
        fields = "__all__"
        # exclude = ["create_user_id", "modify_user_id", "is_deleted"]
        # read_only_fields = ["user"]


class ShopViewSet(CustomModelViewSet):
    """
    店铺接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = Shop.objects.exclude().all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["shop_id"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg="新增成功")

    def perform_create(self, serializer):
        """
        重写perform_create执行创建方法，用于更新user表中的shop外键
        :param serializer: 序列化器提交的验证后的数据
        :return:
        """
        # 这里serializer.save()已经存入数据库，并返回一个实例
        instance = serializer.save()
        shop_id = instance.shop_id
        user = User.objects.get(user_id=self.request.user.user_id)
        user.shop_id = shop_id
        user.save()

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated],
            serializer_class=UserToShopCollectSerializer)
    def shop_collect(self, request, *args, **kwargs):
        user_instance = User.objects.get(pk=self.request.user.user_id)
        shop_instance = Shop.objects.get(pk=self.request.data['shop'])
        user2shop_collect = UserToShopCollect.objects.create(user=user_instance,
                                                             shop=shop_instance)
        user2shop_collect.save()
        return DetailResponse(data=request.data, msg="收藏成功")

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated],
            serializer_class=UserToShopCollectSerializer)
    def get_collect(self, request, *args, **kwargs):
        # 获取 UserToShopCollect 表的数据
        instance = UserToShopCollect.objects.exclude().all()
        # 应用过滤逻辑
        queryset = self.filter_queryset(instance)
        # 进行分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")
