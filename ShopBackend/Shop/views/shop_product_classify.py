from ..utils.import_header import *
from Shop.models import ShopProductClassify
from ..utils.filters import BaseProductFilter

class ShopProductClassifyFilter(BaseProductFilter):
    """
    查询条件区间过滤
    """

    # 模糊查询 (不区分大小写的包含)
    name = django_filters.CharFilter(field_name='product_name', lookup_expr='icontains',
                                     label="产品名称", help_text="模糊查询")

    class Meta:
        model = ShopProductClassify
        # 这里列出模型中实际存在的字段，不能包含非模型字段，而且这里的都是精确查询
        fields = ["product_id", "product_classify", "shop_product_classify", "shop"]


class ShopProductClassifySerializer(CustomModelSerializer):
    """
    店铺产品分类序列化器
    """

    class Meta:
        model = ShopProductClassify
        fields = "__all__"
        # exclude = ["create_user_id", "modify_user_id", "is_deleted"]
        read_only_fields = ["shop"]


class ShopProductClassifyViewSet(CustomModelViewSet):
    """
    店铺产品分类接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = ShopProductClassify.objects.exclude().all()
    serializer_class = ShopProductClassifySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ShopProductClassifyFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        if request.user.shop is None or request.user.shop == "":
            return DetailResponse(data=serializer.data, msg="您不是店主，无法新增商品")
        serializer.validated_data["shop"] = request.user.shop
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg="新增成功")
