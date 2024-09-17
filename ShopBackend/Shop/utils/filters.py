import django_filters

class BaseProductFilter(django_filters.FilterSet):
    """
    查询条件区间过滤
    """
    # 大于等于查询
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte',
                                            label="产品价格", help_text="大于等于")
    # 小于等于查询
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte',
                                            label="产品价格", help_text="小于等于")

    # 模糊查询 (不区分大小写的包含)
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains',
                                     label="产品名称", help_text="模糊查询")

    class Meta:
        abstract = True



