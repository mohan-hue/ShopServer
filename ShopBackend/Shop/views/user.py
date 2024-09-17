from ..utils.import_header import *
from Shop.models import User, GENDER_CHOICES


class UserSerializer(CustomModelSerializer):
    """
    序列化器
    """
    password = serializers.CharField(write_only=True, max_length=255)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.modify_user_id = user.user_id
        user.create_user_id = user.user_id
        user.save()

        return user

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ["is_superuser", "is_staff", "is_active", "date_joined", "last_login",
                   "groups", "user_permissions", "last_name", "first_name", "is_deleted"]
        read_only_fields = ["user_id", "create_user_id", "modify_user_id", "user_create_datetime"]


class UserViewSet(CustomModelViewSet):
    """
    用户接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    # 过滤数据，并优化查询
    # books = Book.objects.exclude(published=False).select_related('publisher').prefetch_related('authors').all()
    queryset = User.objects.exclude(is_superuser=1).all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # create_serializer_class = UserCreateSerializer
    # update_serializer_class = UserUpdateSerializer
    filter_fields = ["name", "username", "gender", "phone_number"]
    search_fields = ["name", "username", "phone_number", "shop_id"]

    # 导出
    # export_field_label = None
    # import_field_dict = None

    @action(methods=["POST"], detail=False, permission_classes=[])
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg="注册成功")

    def create(self, request, *args, **kwargs):
        return DetailResponse(data=[], msg="不是新用户注册", status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def user_info(self, request):
        """
        获取当前用户信息
        """
        user = request.user
        result = {
            "user_id": user.user_id,
            "nickname": user.username,
            "name": user.name,
            "gender": dict(GENDER_CHOICES).get(user.gender),
            "phone_number": user.phone_number,
        }
        return DetailResponse(data=result, msg="获取成功")

    @action(methods=["PUT"], detail=False, permission_classes=[IsAuthenticated])
    def change_password(self, request, *args, **kwargs):
        """密码修改"""
        data = request.data
        old_pwd = data.get("oldPassword")
        print(old_pwd)
        new_pwd = data.get("newPassword")
        new_pwd2 = data.get("newPassword2")
        if old_pwd is None or new_pwd is None or new_pwd2 is None:
            return ErrorResponse(msg="参数不能为空")
        if new_pwd != new_pwd2:
            return ErrorResponse(msg="两次密码不匹配")
        verify_password = check_password(old_pwd, request.user.password)
        if not verify_password:
            old_pwd_md5 = hashlib.md5(old_pwd.encode(encoding='UTF-8')).hexdigest()
            verify_password = check_password(str(old_pwd_md5), request.user.password)
        if verify_password:
            request.user.password = make_password(hashlib.md5(new_pwd.encode(encoding='UTF-8')).hexdigest())
            request.user.save()
            return DetailResponse(data=None, msg="修改成功")
        return ErrorResponse(msg="旧密码不正确")


