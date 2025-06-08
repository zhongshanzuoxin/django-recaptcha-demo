
from django.contrib import admin
from .models import Applicant

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['email', 'client_name', 'is_submitted', 'created_at']
    list_filter = ['is_submitted', 'created_at', 'subscription_enabled']
    search_fields = ['email', 'client_name', 'app_name']
    readonly_fields = ['verify_token', 'created_at', 'updated_at']
    
    fieldsets = (
        ('基本情報', {
            'fields': ('email', 'verify_token', 'app_settings_url', 'is_submitted')
        }),
        ('クライアント情報', {
            'fields': ('client_name', 'website_url', 'x_account', 'instagram', 
                      'youtube', 'ticktock', 'followers_count', 'other_sns', 'remarks')
        }),
        ('アプリ設定', {
            'fields': ('app_name', 'subscription_enabled', 'subscription_price', 
                      'app_color', 'app_icon', 'app_logo', 'naming_enabled')
        }),
        ('カスタマイズ名称', {
            'fields': ('home_header', 'home_footer', 'shop_header', 'shop_footer',
                      'timeline_header', 'timeline_footer', 'chat_header', 'chat_footer',
                      'more_header', 'more_footer', 'collection', 'pickup', 'goods',
                      'products', 'twoshot', 'live', 'room', 'dm_long', 'dm_short',
                      'artist_name'),
            'classes': ('collapse',)
        }),
        ('銀行情報', {
            'fields': ('bank_name', 'branch_name', 'branch_code', 'bank_account_number',
                      'bank_account_holder', 'bank_account_type'),
            'classes': ('collapse',)
        }),
        ('特定商取引法情報', {
            'fields': ('seller_name', 'manager_name', 'seller_address', 
                      'seller_phone_number', 'seller_email', 'price_info',
                      'additional_fees', 'allowed_payment', 'delivery_method',
                      'return_policy'),
            'classes': ('collapse',)
        }),
        ('システム情報', {
            'fields': ('created_at', 'updated_at')
        }),
    )