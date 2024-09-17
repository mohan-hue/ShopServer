from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, UserManager

from Shop.utils.models import BaseModel, ProductClassBaseModel, SoftDeleteModel

GENDER_CHOICES = (
        (0, "未知"),
        (1, "男"),
        (2, "女"),
    )

NON_PAYMENT_CHOICES = (
        (0, "其他状态"),
        (1, "未付款"),
        (2, "已付款"),
    )

WAIT_FOR_RECEIVING_CHOICES = (
        (0, "其他状态"),
        (1, "待收货"),
        (2, "已收货"),
    )

class Shop(BaseModel, SoftDeleteModel):
    """
    店铺表
    """
    shop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name='店铺ID',
                                      help_text='店铺ID')
    shop_name = models.CharField(max_length=64, null=False, blank=True, verbose_name='店铺名称',
                                    help_text='店铺名称')
    shop_info = models.TextField(default='', null=False, blank=True, verbose_name='店铺信息',
                                 help_text='店铺信息')
    shopkeeper_phone = models.CharField(max_length=11, null=False, blank=True, verbose_name='店主电话号码',
                                 help_text='店主电话号码')
    shopkeeper_name = models.CharField(max_length=64, null=False, blank=True, verbose_name='店主名字',
                                        help_text='店主名字')

    def __str__(self):
        return self.shop_name

    class Meta:
        db_table = "shop"
        verbose_name = "店铺表"
        verbose_name_plural = verbose_name


class User(BaseModel, SoftDeleteModel, AbstractUser):
    """
    用户表
    """
    # 保留对 UserManager 的引用以使用 create_superuser
    objects = UserManager()

    user_id = models.BigAutoField(primary_key=True, verbose_name="用户ID", help_text="用户ID")
    # user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name='用户ID',
    #                            help_text='用户ID')
    name = models.CharField(max_length=64, null=False, blank=True, verbose_name='姓名', help_text='姓名')
    username = models.CharField(max_length=150, null=False, blank=True, unique=True, db_index=True, verbose_name='账号',
                                help_text='账号')
    password = models.CharField(max_length=255, null=False, blank=True, verbose_name='密码', help_text='密码')
    icon = models.ImageField(upload_to='static/icon/', null=True, blank=True, verbose_name='头像', help_text='头像')
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0, null=True, blank=True, verbose_name='性别',
                                 help_text='性别')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='生日', help_text='生日')
    phone_number = models.CharField(max_length=11, null=False, blank=True, unique=True, db_index=True,
                                    verbose_name='电话号码', help_text='电话号码')
    shop = models.ForeignKey(to=Shop, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='店铺ID', help_text='店铺ID')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "user"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        ordering = ("user_create_datetime",)


class UserToShopCollect(models.Model):
    """
    用户-店铺收藏表
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=True,
                                             verbose_name='用户ID', help_text='用户ID')
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE, null=False,
                                           verbose_name='店铺ID', help_text='店铺ID')

    def __str__(self):
        return str(self.user.user_id)

    class Meta:
        db_table = "user_to_shop_collect"
        verbose_name = "用户2店铺收藏表"
        verbose_name_plural = verbose_name


class ReceivingAddress(models.Model):
    """
    收货地址表
    """
    address = models.CharField(max_length=255, null=False, blank=True, verbose_name='地址', help_text='地址')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=True,
                                verbose_name='用户ID', help_text='用户ID')

    def __str__(self):
        return self.address

    class Meta:
        db_table = "receiving_address"
        verbose_name = "收获地址表"
        verbose_name_plural = verbose_name


class ProductOrder(BaseModel):
    """
    产品订单表
    """
    product_order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name='产品订单ID',
                                        help_text='产品订单ID')
    product_id = models.CharField(max_length=255, null=False, blank=True, verbose_name='产品ID', help_text='产品ID')
    product_name = models.CharField(max_length=255, null=False, blank=True, verbose_name='产品名称',
                                    help_text='产品名称')
    shop_id = models.CharField(max_length=255, null=False, blank=True, verbose_name='商店ID', help_text='商店ID')
    price = models.FloatField(default=0.0, null=False, blank=True, verbose_name='价格', help_text='价格')
    product_classify_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='产品分类ID',
                                           help_text='产品分类ID')
    product_classify_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='产品分类名称',
                                             help_text='产品名称')
    product_describe = models.TextField(null=True, blank=True, verbose_name='产品描述', help_text='产品描述')

    non_payment = models.IntegerField(choices=NON_PAYMENT_CHOICES, default=0, null=True, blank=True,
                                      verbose_name='待付款', help_text='待付款')

    wait_for_receiving = models.IntegerField(choices=WAIT_FOR_RECEIVING_CHOICES, default=0, null=True, blank=True,
                                             verbose_name='待收货', help_text='待收货')
    after_sale = models.BooleanField(default=False, null=True, blank=True, verbose_name='售后', help_text='售后')
    is_finish = models.BooleanField(default=False, null=True, blank=True, verbose_name='是否完成', help_text='是否完成')
    is_cancel = models.BooleanField(default=False, null=True, blank=True, verbose_name='是否取消', help_text='是否取消')

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = "product_order"
        verbose_name = "产品订单表"
        verbose_name_plural = verbose_name


class UserToProductOrder(models.Model):
    """
    用户-产品订单表
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=True,
                                           verbose_name='用户ID', help_text='用户ID')
    product_order = models.ForeignKey(to=ProductOrder, on_delete=models.CASCADE, null=False,
                                         blank=True, verbose_name='产品订单ID', help_text='产品订单ID')

    def __str__(self):
        return str(self.user.user_id)

    class Meta:
        db_table = "user_to_product_order"
        verbose_name = "用户2产品订单表"
        verbose_name_plural = verbose_name


class Coupon(BaseModel):
    """
    优惠券表
    """
    coupon_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name='优惠券ID',
                                 help_text='优惠券ID')
    coupon_name = models.CharField(max_length=255, null=False, blank=True, verbose_name='优惠券名称',
                                   help_text='优惠券名称')
    coupon_discount = models.FloatField(default=0.0, null=False, blank=True, verbose_name='优惠券折扣',
                                          help_text='优惠券折扣')
    coupon_product_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='折扣产品ID',
                                         help_text='折扣产品ID')
    product_classify_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='产品分类ID',
                                           help_text='产品分类ID')
    coupon_shop_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='折扣商店ID',
                                      help_text='折扣商店ID')
    valid_time = models.DateTimeField(null=False, blank=True, verbose_name='有效时间', help_text='有效时间')
    is_superposition = models.BooleanField(default=False, null=True, blank=True, verbose_name='是否能叠加',
                                           help_text='是否能叠加')
    is_use = models.BooleanField(default=False, null=True, blank=True, verbose_name='是否使用', help_text='是否使用')
    is_valid = models.BooleanField(default=False, null=True, blank=True, verbose_name='是否有效', help_text='是否有效')

    def __str__(self):
        return self.coupon_name

    class Meta:
        db_table = "coupon"
        verbose_name = "优惠券表"
        verbose_name_plural = verbose_name


class UserToCoupon(models.Model):
    """
    用户-优惠券表
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=True,
                                    verbose_name='用户ID', help_text='用户ID')
    coupon = models.ForeignKey(to=Coupon, on_delete=models.CASCADE, null=False, blank=True,
                                  verbose_name='优惠券ID', help_text='优惠券ID')

    def __str__(self):
        return str(self.user.user_id)

    class Meta:
        db_table = "user_to_coupon"
        verbose_name = "用户2优惠券表"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """
    评论表
    """
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name='评论ID',
                                  help_text='评论ID')
    upvote = models.BigIntegerField(default=0, null=False, blank=True, verbose_name='点赞', help_text='点赞')
    trample = models.BigIntegerField(default=0, null=False, blank=True, verbose_name='踩', help_text='踩')
    reply_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='回复ID', help_text='回复ID')
    product_classify_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='产品分类ID',
                                           help_text='产品分类ID')
    content = models.TextField(null=True, blank=True, verbose_name='内容', help_text='内容')
    shop_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='店铺ID',
                               help_text='店铺ID')
    product_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='产品ID',
                               help_text='产品ID')

    def __str__(self):
        return self.content

    class Meta:
        db_table = "comment"
        verbose_name = "评论表"
        verbose_name_plural = verbose_name


class UserToComment(models.Model):
    """
    用户-评论表
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=True,
                                     verbose_name='用户ID', help_text='用户ID')
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, null=False, blank=True,
                                   verbose_name='评论ID', help_text='评论ID')

    def __str__(self):
        return str(self.user.user_id)

    class Meta:
        db_table = "user_to_comment"
        verbose_name = "用户2评论表"
        verbose_name_plural = verbose_name


class Reply(models.Model):
    """
    回复表
    """
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, null=False, blank=True,
                                   verbose_name='评论ID', help_text='评论ID')
    nickname = models.CharField(max_length=64, null=False, blank=True, verbose_name='用户昵称', help_text='用户昵称')
    user_id = models.CharField(max_length=255, null=False, blank=True, verbose_name='用户ID',
                                    help_text='用户ID')
    reply_content = models.TextField(null=True, blank=True, verbose_name='内容', help_text='内容')
    replied_nickname = models.CharField(max_length=64, null=False, blank=True, verbose_name='被回复用户昵称',
                                        help_text='被回复用户昵称')

    def __str__(self):
        return self.reply_content

    class Meta:
        db_table = "reply"
        verbose_name = "回复表"
        verbose_name_plural = verbose_name


class ProductCollect(models.Model):
    """
    产品收藏表
    """
    product_collect_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name='产品收藏ID',
                                          help_text='产品收藏ID')
    shop_id = models.CharField(max_length=255, null=False, blank=True, verbose_name='店铺ID', help_text='店铺ID')
    product_id = models.CharField(max_length=255, null=False, blank=True, verbose_name='产品ID', help_text='产品ID')
    product_classify_id = models.CharField(max_length=255, null=False, blank=True, verbose_name='产品分类ID',
                                             help_text='产品分类ID')
    price = models.FloatField(default=0.0, null=False, blank=True, verbose_name='价格', help_text='价格')
    product_name = models.CharField(max_length=255, null=False, blank=True, verbose_name='产品名称', help_text='产品名称')

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = "product_collect"
        verbose_name = "产品收藏表"
        verbose_name_plural = verbose_name


class UserToProductCollect(models.Model):
    """
    用户-产品收藏表
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=True,
                                     verbose_name='用户ID', help_text='用户ID')
    product_collect = models.ForeignKey(to=ProductCollect, on_delete=models.CASCADE, null=False, blank=True,
                                   verbose_name='产品收藏ID', help_text='产品收藏ID')

    def __str__(self):
        return str(self.user.user_id)

    class Meta:
        db_table = "user_to_product_collect"
        verbose_name = "用户2产品收藏表"
        verbose_name_plural = verbose_name


class Classify(BaseModel):
    """
    分类表
    """
    product_classify_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name='产品分类ID',
                                          help_text='产品分类ID')
    product_table = models.CharField(max_length=255, null=False, blank=True, verbose_name='产品表名', help_text='产品表名')
    classify_name = models.CharField(max_length=255, null=False, blank=True, verbose_name='分类名称', help_text='分类名称')

    def __str__(self):
        return self.classify_name

    class Meta:
        db_table = "classify"
        verbose_name = "分类表"
        verbose_name_plural = verbose_name



class BankCardID(BaseModel, SoftDeleteModel):
    """
    银行卡表
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=True,
                                verbose_name='用户ID', help_text='用户ID')
    bank_card_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name='银行卡ID',
                                     help_text='银行卡ID')
    bank_card = models.CharField(max_length=32, null=False, blank=True, verbose_name='银行卡号',
                                     help_text='银行卡号')
    bank_name = models.CharField(max_length=64, null=False, blank=True, verbose_name='银行卡名',
                                 help_text='银行卡名')

    def __str__(self):
        return self.bank_name

    class Meta:
        db_table = "bank_card_id"
        verbose_name = "银行卡表"
        verbose_name_plural = verbose_name


class ShoppingTrolley(models.Model):
    """
    购物车表
    """
    shopping_trolley_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name='购物车ID',
                               help_text='购物车ID')
    product_id = models.CharField(max_length=255, null=False, blank=True, verbose_name='产品ID',
                               help_text='产品ID')
    shop_id = models.CharField(max_length=255, null=False, blank=True, verbose_name='店铺ID',
                               help_text='店铺ID')
    product_name = models.CharField(max_length=64, null=False, blank=True, verbose_name='产品名称',
                                       help_text='产品名称')
    price = models.FloatField(default=0.0, null=False, blank=True, verbose_name='价格',
                                       help_text='价格')

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = "shopping_trolley"
        verbose_name = "购物车表"
        verbose_name_plural = verbose_name


class UserToShoppingTrolley(models.Model):
    """
    用户-购物车表
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=True,
                                          verbose_name='用户ID', help_text='用户ID')
    shopping_trolley = models.ForeignKey(to=ShoppingTrolley, on_delete=models.CASCADE, null=False,
                                blank=True,  verbose_name='购物车ID', help_text='购物车ID')

    def __str__(self):
        return str(self.user.user_id)

    class Meta:
        db_table = "user_to_shopping_trolley"
        verbose_name = "用户2购物车表"
        verbose_name_plural = verbose_name


class ShopProductClassify(models.Model):
    """
    店铺产品分类表
    """
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE, null=False, blank=True,
                                verbose_name='店铺ID', help_text='店铺ID')
    product_id = models.CharField(max_length=255, null=False, blank=True, verbose_name='产品ID',
                                  help_text='产品ID')
    product_name = models.CharField(max_length=64, null=False, blank=True, verbose_name='产品名称',
                                    help_text='产品名称')
    price = models.FloatField(default=0.0, null=False, blank=True, verbose_name='价格',
                                   help_text='价格')
    product_classify = models.CharField(max_length=255, null=False, blank=True, verbose_name='产品分类',
                                    help_text='产品分类')
    shop_product_classify = models.CharField(max_length=255, null=False, blank=True, verbose_name='店铺产品分类',
                                        help_text='店铺产品分类')
    product_describe = models.TextField(null=True, blank=True, verbose_name='产品描述',
                                           help_text='产品描述')

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = "shop_product_classify"
        verbose_name = "店铺产品分类表"
        verbose_name_plural = verbose_name


class BrowsingHistory(models.Model):
    """
    浏览记录表
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=True,
                                verbose_name='用户ID', help_text='用户ID')
    browsing_history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name='浏览记录ID',
                                  help_text='浏览记录ID')
    product_id = models.CharField(max_length=255, null=False, blank=True, verbose_name='产品ID',
                                  help_text='产品ID')
    shop_id = models.CharField(max_length=255, null=False, blank=True, verbose_name='店铺ID',
                                  help_text='店铺ID')
    price = models.FloatField(default=0.0, null=False, blank=True, verbose_name='价格',
                                   help_text='价格')
    product_name = models.CharField(max_length=64, null=False, blank=True, verbose_name='产品名称',
                                        help_text='产品名称')

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = "browsing_history"
        verbose_name = "浏览记录表"
        verbose_name_plural = verbose_name

# 各类产品表，例如手机、鞋子等，写在下方 BaseModel, SoftDeleteModel, ProductClassBaseModel
class HouseholdAppliances(ProductClassBaseModel):
    """
    家用电器表
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "household_appliances"
        verbose_name = "家用电器表"
        verbose_name_plural = verbose_name


class MobilePhone(ProductClassBaseModel):
    """
    手机表
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "mobile_phone"
        verbose_name = "手机表"
        verbose_name_plural = verbose_name


class Computer(ProductClassBaseModel):
    """
    电脑表
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "computer"
        verbose_name = "电脑表"
        verbose_name_plural = verbose_name


class Home(ProductClassBaseModel):
    """
    家居表
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "home"
        verbose_name = "家居表"
        verbose_name_plural = verbose_name


class MensWear(ProductClassBaseModel):
    """
    男装表
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "mens_wear"
        verbose_name = "男装表"
        verbose_name_plural = verbose_name


class BeautyPersonalCare(ProductClassBaseModel):
    """
    美妆个护表
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "beauty_personal_care"
        verbose_name = "美妆个护表"
        verbose_name_plural = verbose_name


class WomenShoes(ProductClassBaseModel):
    """
    女鞋表
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "women_shoes"
        verbose_name = "女鞋表"
        verbose_name_plural = verbose_name


class MenShoes(ProductClassBaseModel):
    """
    男鞋表
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "men_shoes"
        verbose_name = "男鞋表"
        verbose_name_plural = verbose_name


class Car(ProductClassBaseModel):
    """
    汽车表
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "car"
        verbose_name = "汽车表"
        verbose_name_plural = verbose_name


class MaternalAndChild(ProductClassBaseModel):
    """
    母婴表
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "maternal_and_child"
        verbose_name = "母婴表"
        verbose_name_plural = verbose_name

class Foodstuff(ProductClassBaseModel):
    """
    食品表
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "foodstuff"
        verbose_name = "食品表"
        verbose_name_plural = verbose_name


class GiftFlowers(ProductClassBaseModel):
    """
    礼品鲜花表
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "gift_flowers"
        verbose_name = "礼品鲜花表"
        verbose_name_plural = verbose_name


class HealthCare(ProductClassBaseModel):
    """
    医疗保健
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "health_care"
        verbose_name = "医疗保健"
        verbose_name_plural = verbose_name


class Books(ProductClassBaseModel):
    """
    图书表
    """
    def __str__(self):
        return self.name

    class Meta:
        db_table = "books"
        verbose_name = "图书表"
        verbose_name_plural = verbose_name

ClassifyTableObject = {
    "HouseholdAppliances": HouseholdAppliances,
    "MobilePhone": MobilePhone,
    "Computer": Computer,
    "Home": Home,
    "MensWear": MensWear,
    "BeautyPersonalCare": BeautyPersonalCare,
    "WomenShoes": WomenShoes,
    "MenShoes": MenShoes,
    "Car": Car,
    "MaternalAndChild": MaternalAndChild,
    "Foodstuff": Foodstuff,
    "GiftFlowers": GiftFlowers,
    "HealthCare": HealthCare,
    "Books": Books,
}