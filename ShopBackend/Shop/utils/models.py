"""
公共基础model类
"""

from django.apps import apps
from django.db import models
from django.conf import settings
import uuid


class BaseModel(models.Model):
    """
    基础模型类，包含数据库的基础信息
    """
    # id = models.BigAutoField(help_text="Id", verbose_name="Id")
    create_user_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='创建人ID', help_text="创建人ID")
    user_create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                                verbose_name="创建时间")
    modify_user_id = models.CharField(max_length=255, null=True, blank=True, help_text="修改人ID", verbose_name="修改人ID")
    user_modify_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间",
                                                verbose_name="修改时间")

    class Meta:
        abstract = True
        verbose_name = '基础模型'
        verbose_name_plural = verbose_name


class SoftDeleteQuerySet(models.QuerySet):
    pass


class SoftDeleteManager(models.Manager):
    """支持软删除"""

    def __init__(self, *args, **kwargs):
        self.__add_is_del_filter = False
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        # 考虑是否主动传入is_deleted
        if not kwargs.get('is_deleted') is None:
            self.__add_is_del_filter = True
        return super(SoftDeleteManager, self).filter(*args, **kwargs)

    def get_queryset(self):
        if self.__add_is_del_filter:
            return SoftDeleteQuerySet(self.model, using=self._db).exclude(is_deleted=False)
        return SoftDeleteQuerySet(self.model).exclude(is_deleted=True)

    def get_by_natural_key(self, name):
        return SoftDeleteQuerySet(self.model).get(username=name)


class SoftDeleteModel(models.Model):
    """
    软删除模型
    一旦继承,就将开启软删除
    """
    is_deleted = models.BooleanField(verbose_name="是否软删除", help_text='是否软删除', default=False, db_index=True)
    objects = SoftDeleteManager()

    class Meta:
        abstract = True
        verbose_name = '软删除模型'
        verbose_name_plural = verbose_name


class ProductClassBaseModel(models.Model):
    """
    产品类基础模型，包含了所有产品的基础信息
    """
    # id = models.BigAutoField(help_text="Id", verbose_name="Id")
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='产品名称', help_text='产品名称')
    price = models.IntegerField(default=0.0, null=False, blank=False, verbose_name='产品价格', help_text='产品价格')
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name='产品ID',
                                  help_text='产品ID')
    describe = models.TextField(null=True, blank=True, verbose_name='产品描述', help_text='产品描述')
    product_classify_id = models.CharField(max_length=255, null=True, blank=False, verbose_name='产品分类ID',
                                           help_text='产品分类ID')
    product_classify_name = models.CharField(max_length=64, null=True, blank=False, verbose_name='产品分类名称',
                                           help_text='产品分类名称')

    class Meta:
        abstract = True
        verbose_name = '产品类基础模型'
        verbose_name_plural = verbose_name
