from dataclasses import field

from django.contrib import admin
from django.contrib.admin import display

from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Shop)
admin.site.register(BankCardID)
admin.site.register(ReceivingAddress)
admin.site.register(Classify)
admin.site.register(MobilePhone)
admin.site.register(ShopProductClassify)
admin.site.register(ProductOrder)
admin.site.register(Coupon)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(ProductCollect)
admin.site.register(ShoppingTrolley)


