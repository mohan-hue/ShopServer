from django_filters.rest_framework import DjangoFilterBackend

from ..utils.import_header import *
from Shop.models import Shop, User, ClassifyTableObject, Classify
from ..utils.filters import BaseProductFilter


class ProductFilter(DjangoFilterBackend):
    """
    动态获取产品的过滤条件
    """

    def get_filterset_class(self, view, queryset=None):
        request = view.request
        product_classify_id = request.query_params.get('product_classify_id')

        if product_classify_id:
            instance = Classify.objects.filter(pk=product_classify_id).first()
            if instance:
                product_model = ClassifyTableObject.get(instance.product_table)

                class DynamicProductFilter(BaseProductFilter):

                    class Meta:
                        model = product_model
                        fields = ['product_id', 'product_classify_name', 'product_classify_id']

                return DynamicProductFilter

        class DefaultProductFilter(django_filters.FilterSet):

            # 模糊查询 (不区分大小写的包含)
            name = django_filters.CharFilter(field_name='classify_name', lookup_expr='icontains',
                                             label="分类名称", help_text="模糊查询")

            class Meta:
                model = Classify
                fields = ['product_classify_id']

        return DefaultProductFilter


class ProductViewSet(CustomModelViewSet):
    """
    通用产品接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Classify.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ProductFilter]

    def get_queryset(self):
        # 这里可以访问 self.request 对象
        product_classify_id = self.request.query_params.get('product_classify_id')
        product_id = self.request.query_params.get('product_id')
        if product_classify_id:
            # 查询 Classify 表，获取 product_table 字段
            instance = Classify.objects.filter(pk=product_classify_id).first()

            # 确保 instance 存在，并且获取对应的模型
            if instance:
                product_model = ClassifyTableObject.get(instance.product_table)

                # 返回动态模型的数据集，如果带product_id来访问，则查询指定的product_id的数据，否则返回
                # 该类型的所有数据
                if product_id:
                    # return product_model.objects.filter(product_id=product_id)
                    pass
                # 暂时没有需要排除的字段
                return product_model.objects.exclude().all()

        # 如果没有传递 product_classify_id，默认返回 Classify 表的数据
        return Classify.objects.exclude().all()

    def get_serializer_class(self):
        product_classify_id_1 = self.request.query_params.get('product_classify_id')
        product_classify_id_2 = self.request.data.get('product_classify_id')
        if product_classify_id_1 or product_classify_id_2:
            instance = None
            if product_classify_id_1:
                instance = Classify.objects.filter(pk=product_classify_id_1).first()
            else:
                instance = Classify.objects.filter(pk=product_classify_id_2).first()
            if instance:
                product_model = ClassifyTableObject.get(instance.product_table)

                class DynamicProductSerializer(CustomModelSerializer):
                    class Meta:
                        model = product_model
                        fields = '__all__'
                        read_only_fields = ["product_id"]


                return DynamicProductSerializer

        class DefaultProductSerializer(CustomModelSerializer):
            class Meta:
                model = Classify
                exclude = ['create_user_id', 'modify_user_id']
                read_only_fields = ["product_classify_id"]

        return DefaultProductSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg="新增成功")

