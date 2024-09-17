from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Shop.views.user import UserViewSet
from Shop.views.shop import ShopViewSet
from Shop.views.shop_product_classify import ShopProductClassifyViewSet
from Shop.views.browsing_history import BrowsingHistoryViewSet
from Shop.views.bank_card_id import BankCardIDViewSet
from Shop.views.receiving_address import ReceivingAddressViewSet
from Shop.views.coupon import CouponViewSet
from Shop.views.comment import CommentViewSet
from Shop.views.reply import ReplyViewSet
from Shop.views.classify import ClassifyViewSet
from Shop.views.product_collect import ProductCollectViewSet
from Shop.views.shopping_trolley import ShoppingTrolleyViewSet
from Shop.views.product_order import ProductOrderViewSet
from Shop.views.product import ProductViewSet
from Shop.views.ProductClassify.household_appliances import HouseholdAppliancesViewSet
from Shop.views.ProductClassify.mobile_phone import MobilePhoneViewSet
from Shop.views.ProductClassify.computer import ComputerViewSet
from Shop.views.ProductClassify.home import HomeViewSet
from Shop.views.ProductClassify.mens_wear import MensWearViewSet
from Shop.views.ProductClassify.beauty_personal_care import BeautyPersonalCareViewSet
from Shop.views.ProductClassify.women_shoes import WomenShoesViewSet
from Shop.views.ProductClassify.men_shoes import MenShoesViewSet
from Shop.views.ProductClassify.car import CarViewSet
from Shop.views.ProductClassify.maternal_and_child import MaternalAndChildViewSet
from Shop.views.ProductClassify.foodstuff import FoodstuffViewSet
from Shop.views.ProductClassify.gift_flowers import GiftFlowersViewSet
from Shop.views.ProductClassify.health_care import HealthCareViewSet
from Shop.views.ProductClassify.books import BooksViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'shop', ShopViewSet)
router.register(r'shop_pro_cls', ShopProductClassifyViewSet)
router.register(r'bro_his', BrowsingHistoryViewSet)
router.register(r'bank_card', BankCardIDViewSet)
router.register(r'recv_address', ReceivingAddressViewSet)
router.register(r'coupon', CouponViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'reply', ReplyViewSet)
router.register(r'classify', ClassifyViewSet)
router.register(r'pro_collect', ProductCollectViewSet)
router.register(r'pro_order', ProductOrderViewSet)
router.register(r'product', ProductViewSet)
router.register(r'shop_trolley', ShoppingTrolleyViewSet)
router.register(r'house_appliances', HouseholdAppliancesViewSet)
router.register(r'mobile_phone', MobilePhoneViewSet)
router.register(r'computer', ComputerViewSet)
router.register(r'home', HomeViewSet)
router.register(r'mens_wear', MensWearViewSet)
router.register(r'beauty_person_care', BeautyPersonalCareViewSet)
router.register(r'women_shoes', WomenShoesViewSet)
router.register(r'men_shoes', MenShoesViewSet)
router.register(r'car', CarViewSet)
router.register(r'maternal_child', MaternalAndChildViewSet)
router.register(r'foodstuff', FoodstuffViewSet)
router.register(r'gift_flower', GiftFlowersViewSet)
router.register(r'health_care', HealthCareViewSet)
router.register(r'books', BooksViewSet)
router.register(r'books', BooksViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('login/', LoginViewSet.as_view(template_name='rest_framework/login.html'), name='login'),
    # path('logout/', LogoutViewSet.as_view(), name='logout'),
]

# urlpatterns += router.urls
