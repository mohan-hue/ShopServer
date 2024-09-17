"""
自定义序列化器
"""
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer
from django.utils.functional import cached_property
from rest_framework.utils.serializer_helpers import BindingDict

from django_restql.mixins import DynamicFieldsMixin

from ..models import User


class CustomModelSerializer(DynamicFieldsMixin, ModelSerializer):
    """
    增强DRF的ModelSerializer,可自动更新模型的审计字段记录
    (1)self.request能获取到rest_framework.request.Request对象
    """

    # 修改人的审计字段名称, 默认modifier, 继承使用时可自定义覆盖
    modify_user_field_id = "modify_user_id"
    # modify_user_name = serializers.SerializerMethodField(read_only=True)

    # def get_modify_user_name(self, instance):
    #     if not hasattr(instance, "modify_user_id"):
    #         return None
    #     # 如果User中查询该字段在name中，可能出现多个相同名字，但是只返回第一个名字，这个不太好
    #     queryset = (
    #         User.objects.filter(name=instance.modify_user_id)
    #         .values_list("username", flat=True)
    #         .first()
    #     )
    #     if queryset:
    #         return queryset
    #     return None

    # 创建人的审计字段名称, create_user, 继承使用时可自定义覆盖
    create_user_field_id = "create_user_id"
    # create_name = serializers.SlugRelatedField(
    #     slug_field="name", source="create_user_id", read_only=True
    # )
    # 添加默认时间返回格式
    user_create_datetime = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True
    )
    user_modify_datetime = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True
    )

    def __init__(self, instance=None, data=empty, request=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.request: Request = request or self.context.get("request", None)

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        if self.request:
            if str(self.request.user) != "AnonymousUser":
                # 对有创建人ID和修改人ID的表增加该数据
                count = 0
                for field in self.Meta.model._meta.fields:
                    if count == 2:
                        break
                    if self.modify_user_field_id == field.name:
                        count += 1
                        validated_data[self.modify_user_field_id] = self.get_request_user_id()
                    if self.create_user_field_id == field.name:
                        count += 1
                        validated_data[self.create_user_field_id] = self.request.user.user_id

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if self.request:
            if str(self.request.user) != "AnonymousUser":
                # 对有修改人ID的表增加该数据
                for field in self.Meta.model._meta.fields:
                    if self.modify_user_field_id == field.name:
                        validated_data[self.modify_user_field_id] = self.get_request_user_id()
                        break
        return super().update(instance, validated_data)

    def get_request_username(self):
        if getattr(self.request, "user", None):
            return getattr(self.request.user, "username", None)
        return None

    def get_request_name(self):
        if getattr(self.request, "user", None):
            return getattr(self.request.user, "name", None)
        return None

    def get_request_user_id(self):
        if getattr(self.request, "user", None):
            return getattr(self.request.user, "user_id", None)
        return None

    @property
    def errors(self):
        # get errors
        errors = super().errors
        verbose_errors = {}

        # fields = { field.name: field.verbose_name } for each field in model
        fields = {field.name: field.verbose_name for field in
                  self.Meta.model._meta.get_fields() if hasattr(field, 'verbose_name')}

        # iterate over errors and replace error key with verbose name if exists
        for field_name, error in errors.items():
            if field_name in fields:
                verbose_errors[str(fields[field_name])] = error
            else:
                verbose_errors[field_name] = error
        return verbose_errors
