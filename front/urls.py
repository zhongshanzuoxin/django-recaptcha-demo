from django.urls import include, path
from front import views


app_name = 'front'

urlpatterns = [
    path('', views.TopView.as_view(), name="top"),
    path('functional_specs/goods_shop/', views.GoodsShopView.as_view(), name="goods_shop"),
    path('functional_specs/digital_goods_shop/', views.DigitalGoodsShopView.as_view(), name="digital_goods_shop"),
    path('functional_specs/2shot_shop/', views.TwoShotShopView.as_view(), name="2shot_shop"),
    path('functional_specs/live/', views.LiveView.as_view(), name="live"),
    path('functional_specs/2shot/', views.TwoShotView.as_view(), name="2shot"),
    path('functional_specs/timeline/', views.TimelineView.as_view(), name="timeline"),
    path('functional_specs/collection/', views.CollectionView.as_view(), name="collection"),
    path('functional_specs/room/', views.RoomView.as_view(), name="room"),
    path('functional_specs/dm/', views.DmView.as_view(), name="dm"),
    path('functional_specs/moderation/', views.ModerationView.as_view(), name="moderation"),
    path('functional_specs/delivery_management/', views.DeliveryManagementView.as_view(), name="delivery_management"),
    path('functional_specs/permission_management/', views.PermissionManagementView.as_view(), name="permission_management"),
    path('functional_specs/account_management/', views.AccountManagementView.as_view(), name="account_management"),
    path('functional_specs/permissions_overview/', views.PermissionsOverviewView.as_view(), name="permissions_overview"),
    path('revenue/', views.AboutRevenueView.as_view(), name='revenue'),
    path('help/', views.HelpView.as_view(), name="help"),
    path('privacy/', views.PrivacyView.as_view(), name="privacy"),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('app_request/', views.AppRequestView.as_view(), name='app_request'),
    path('app_request_complete/', views.AppRequestCompleteView.as_view(), name='app_request_complete'),
    path('app_settings/', views.AppSettingsView.as_view(), name='app_settings'),
    path('bank-account-setup/', views.BankAccountSetupView.as_view(), name='bank_account_setup'),
    path('specified_commercial_transaction_setup/', views.SpecifiedCommercialTransactionSetupView.as_view(), name='specified_commercial_transaction_setup'),
    path('setup_confirm/', views.SetupConfirmView.as_view(), name='setup_confirm'),
    path('content_naming_guide/', views.ContentNamingGuideView.as_view(), name='content_naming_guide'),
    path('company/', views.CompanyView.as_view(), name='company'),
]