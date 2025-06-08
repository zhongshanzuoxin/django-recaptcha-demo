from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm, ApplicationForm, AppSettingsForm, BankAccountForm, SpecifiedCommercialTransactionForm
from django.conf import settings
from common.email_manager import send_email
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from django.urls import reverse
from front.models import Applicant
from urllib.parse import quote, unquote
from uuid import UUID
import logging

logger = logging.getLogger('web')


class TopView(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, 'front/top.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            user_email = form.cleaned_data['email']
            category = form.cleaned_data['category']
            message = form.cleaned_data['message']
            
            # HTMLメールテンプレートをレンダリング
            context = {
                'name': name,
                'email': user_email,
                'category': dict(form.CATEGORY_CHOICES)[category],
                'message': message,
                'service_name': settings.SERVICE_NAME
            }
            email_body = render_to_string('front/email/contact_email.html', context)
            
            # メール送信処理
            send_email(
                to=settings.CONTACT_MAIL_TO,
                subject=f"【{settings.SERVICE_NAME}】{dict(form.CATEGORY_CHOICES)[category]}のお問い合わせを受け付けました",
                body=email_body,
                source=settings.MAIL_FROM,
                html=True
            )
            
            messages.success(request, 'お問い合わせを送信しました。')
            return redirect('front:top')
        
        return render(request, 'front/top.html', {'form': form})



class GoodsShopView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/goods_shop.html')



class DigitalGoodsShopView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/digital_goods_shop.html')



class TwoShotShopView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/2shot_shop.html')



class LiveView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/live.html')



class TwoShotView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/2shot.html')



class HelpView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/help.html')

class PrivacyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/privacy.html')


class TimelineView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/timeline.html')



class CollectionView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/collection.html')



class RoomView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/room.html')



class DmView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/dm.html')



class ModerationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/moderation.html')



class DeliveryManagementView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/delivery_management.html')



class PermissionManagementView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/permission_management.html')



class AccountManagementView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/account_management.html')



class PermissionsOverviewView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/functional_specs/permissions_overview.html')
    


class AboutRevenueView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/about_revenue.html')



class ContactView(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, 'front/contact.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            user_email = form.cleaned_data['email']
            category = form.cleaned_data['category']
            message = form.cleaned_data['message']
            
            # HTMLメールテンプレートをレンダリング
            context = {
                'name': name,
                'email': user_email,
                'category': dict(form.CATEGORY_CHOICES)[category],
                'message': message,
                'service_name': settings.SERVICE_NAME
            }
            email_body = render_to_string('front/email/contact_email.html', context)
            
            # メール送信処理
            send_email(
                to=settings.CONTACT_MAIL_TO,
                subject=f"【{settings.SERVICE_NAME}】お問い合わせを受け付けました",
                body=email_body,
                source=settings.MAIL_FROM,
                html=True
            )
            
            messages.success(request, 'お問い合わせを送信しました。')
            return redirect('front:contact')
        
        return render(request, 'front/contact.html', {'form': form})



class AppRequestView(View):
    def get(self, request, *args, **kwargs):
        form = ApplicationForm()
        return render(request, 'front/app_request.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            # フォームデータの取得
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            website_url = form.cleaned_data.get('website_url', '')
            x_account = form.cleaned_data.get('x_account', '')
            instagram = form.cleaned_data.get('instagram', '')
            youtube = form.cleaned_data.get('youtube', '')
            tiktok = form.cleaned_data.get('tiktok', '')
            followers_count = form.cleaned_data.get('followers_count', '')
            remarks = form.cleaned_data.get('remarks', '')

            # その他のSNSデータの取得
            other_sns = []
            for key, value in request.POST.items():
                if key.startswith('other_sns_name_') and value:
                    index = key.split('_')[-1]
                    url_key = f'other_sns_url_{index}'
                    url = request.POST.get(url_key, '')
                    if url:
                        other_sns.append({'name': value, 'url': url})

            # Applicantモデルへの保存
            applicant = Applicant.objects.create(
                email=email,
                client_name=name,
                website_url=website_url,
                x_account=x_account,
                instagram=instagram,
                youtube=youtube,
                ticktock=tiktok,
                followers_count=followers_count,
                remarks=remarks,
                other_sns=other_sns
            )

            # 2段目の申請URLを生成して保存
            second_step_path = reverse('front:app_settings')
            second_step_url = request.build_absolute_uri(
                f"{second_step_path}?email={quote(applicant.email)}&uuid={applicant.verify_token}"
            )
            applicant.app_settings_url = second_step_url
            applicant.save()

            # メールテンプレート用のコンテキスト
            context = {
                'name': name,
                'email': email,
                'website_url': website_url,
                'x_account': x_account,
                'instagram': instagram,
                'youtube': youtube,
                'tiktok': tiktok,
                'other_sns': other_sns,
                'followers_count': followers_count,
                'remarks': remarks,
                'service_name': settings.SERVICE_NAME
            }

            # 管理者向けメール
            admin_email_body = render_to_string('front/email/app_request_email.html', context)
            
            # 申請者向けメール
            user_email_body = render_to_string('front/email/app_request_user_email.html', context)
            
            # 管理者へのメール送信
            send_email(
                to=settings.CONTACT_MAIL_TO,
                subject=f"【{settings.SERVICE_NAME}】ファンアプリの申請を受け付けました",
                body=admin_email_body,
                source=settings.MAIL_FROM,
                html=True
            )
            
            # 申請者へのメール送信
            send_email(
                to=email,
                subject=f"【{settings.SERVICE_NAME}】ファンアプリの申請ありがとうございます",
                body=user_email_body,
                source=settings.MAIL_FROM,
                html=True
            )
            
            return redirect('front:app_request_complete')
        
        return render(request, 'front/app_request.html', {'form': form})



class AppSettingsView(View):
    def get(self, request, *args, **kwargs):
        email = unquote(request.GET.get('email', ''))
        uuid = request.GET.get('uuid')

        # メールアドレスまたはUUIDのパラメータが存在しない場合
        if not email or not uuid:
            return redirect('front:top')
        
        # UUIDの形式チェック
        try:
            UUID(uuid)
        except (ValueError, AttributeError):
            messages.error(request, '不正なURLです。')
            return redirect('front:top')

        # メールアドレスとUUIDの組み合わせが存在しない場合
        applicant = Applicant.objects.filter(email=email, verify_token=uuid).first()
        if not applicant:
            return redirect('front:top')

        # 申請が完了している場合
        if applicant.is_submitted:
            setup_confirm_path = reverse('front:setup_confirm')
            setup_confirm_url = f"{setup_confirm_path}?email={quote(email)}&uuid={uuid}"
            return redirect(setup_confirm_url)

        # 既存のデータがある場合は初期値として設定
        initial_data = {}
        if applicant.app_name:
            initial_data = {
                'app_name': applicant.app_name,
                'subscription_enabled': 'enabled' if applicant.subscription_enabled else 'disabled',
                'subscription_price': applicant.subscription_price,
                'app_color': f'Color_0{applicant.app_color + 1}',  # 0-4の値を'Color_01'-'Color_05'に変換
                'naming_enabled': 'enabled' if applicant.naming_enabled else 'disabled',
                'home': applicant.home_header,
                'shop': applicant.shop_header,
                'timeline': applicant.timeline_header,
                'chat': applicant.chat_header,
                'more': applicant.more_header,
                'collection': applicant.collection,
                'pickup': applicant.pickup,
                'goods': applicant.goods,
                'products': applicant.products,
                'twoshot': applicant.twoshot,
                'live': applicant.live,
                'room': applicant.room,
                'dm': applicant.dm_long,
                'artist_name': applicant.artist_name,
            }

        form = AppSettingsForm(initial=initial_data, applicant=applicant)
        
        # 画像URLを構築
        app_icon_url = None
        app_logo_url = None
        
        if applicant.app_icon:
            app_icon_url = settings.MEDIA_FQDN + applicant.app_icon.name
        
        if applicant.app_logo:
            app_logo_url = settings.MEDIA_FQDN + applicant.app_logo.name
        
        context = {
            'form': form,
            'current_step': 1,
            'applicant': applicant,
            'app_icon_url': app_icon_url,
            'app_logo_url': app_logo_url
        }
        return render(request, 'front/app_settings.html', context)
    
    def post(self, request, *args, **kwargs):
        # URLパラメータを取得
        email = unquote(request.GET.get('email', ''))
        uuid = request.GET.get('uuid')
        
        applicant = Applicant.objects.filter(email=email, verify_token=uuid).first()
        if not applicant:
            return redirect('front:top')

        # 通常の保存処理
        form = AppSettingsForm(request.POST, request.FILES, applicant=applicant)
        if form.is_valid():
            # フォームデータの取得
            app_name = form.cleaned_data['app_name']
            subscription_enabled = form.cleaned_data['subscription_enabled']
            subscription_price = form.cleaned_data.get('subscription_price')
            app_color = form.cleaned_data['app_color']
            app_icon = request.FILES.get('app_icon')
            app_logo = request.FILES.get('app_logo')
            naming_enabled = form.cleaned_data['naming_enabled']

            # Applicantモデルに保存
            applicant.app_name = app_name
            applicant.subscription_enabled = subscription_enabled == 'enabled'
            applicant.subscription_price = subscription_price if subscription_enabled == 'enabled' else None
            applicant.app_color = app_color
            applicant.naming_enabled = naming_enabled == 'enabled'

            # 画像ファイルの保存
            if app_icon:
                applicant.app_icon = app_icon
            if app_logo:
                applicant.app_logo = app_logo
           
            # コンテンツ呼称の保存
            if naming_enabled == 'enabled':
                # ヘッダーとフッターの両方に同じ値を保存
                applicant.home_header = form.cleaned_data.get('home')
                applicant.home_footer = form.cleaned_data.get('home')
                applicant.shop_header = form.cleaned_data.get('shop')
                applicant.shop_footer = form.cleaned_data.get('shop')
                applicant.timeline_header = form.cleaned_data.get('timeline')
                applicant.timeline_footer = form.cleaned_data.get('timeline')
                applicant.chat_header = form.cleaned_data.get('chat')
                applicant.chat_footer = form.cleaned_data.get('chat')
                applicant.more_header = form.cleaned_data.get('more')
                applicant.more_footer = form.cleaned_data.get('more')

                # その他の呼称変更
                applicant.collection = form.cleaned_data.get('collection')
                applicant.pickup = form.cleaned_data.get('pickup')
                applicant.goods = form.cleaned_data.get('goods')
                applicant.products = form.cleaned_data.get('products')
                applicant.twoshot = form.cleaned_data.get('twoshot')
                applicant.live = form.cleaned_data.get('live')
                applicant.room = form.cleaned_data.get('room')
                applicant.dm_long = form.cleaned_data.get('dm')
                applicant.dm_short = form.cleaned_data.get('dm')
                applicant.artist_name = form.cleaned_data.get('artist_name')

            applicant.save()

            # bank_account_setupへのURLにパラメータを付与
            bank_account_path = reverse('front:bank_account_setup')
            bank_account_url = f"{bank_account_path}?email={quote(email)}&uuid={uuid}"
            return redirect(bank_account_url)

        context = {
            'form': form,
            'current_step': 1,
            'applicant': applicant
        }
        return render(request, 'front/app_settings.html', context)



class BankAccountSetupView(View):
    def get(self, request, *args, **kwargs):
        # URLパラメータを取得
        email = unquote(request.GET.get('email', ''))
        uuid = request.GET.get('uuid')

        # メールアドレスまたはUUIDのパラメータが存在しない場合
        if not email or not uuid:
            return redirect('front:top')
        
        # UUIDの形式チェック
        try:
            UUID(uuid)
        except (ValueError, AttributeError):
            return redirect('front:top')

        # メールアドレスとUUIDの組み合わせが存在しない場合
        applicant = Applicant.objects.filter(
            email=email, 
            verify_token=uuid,
            app_name__isnull=False
        ).first()
        if not applicant:
            return redirect('front:top')

        # 申請が完了している場合
        if applicant.is_submitted:
            setup_confirm_path = reverse('front:setup_confirm')
            setup_confirm_url = f"{setup_confirm_path}?email={quote(email)}&uuid={uuid}"
            return redirect(setup_confirm_url)

        # 既存のデータがある場合は初期値として設定
        initial_data = {}
        if applicant.bank_name:
            initial_data = {
                'bank_name': applicant.bank_name,
                'branch_name': applicant.branch_name,
                'branch_code': applicant.branch_code,
                'bank_account_type': applicant.bank_account_type,
                'bank_account_number': applicant.bank_account_number,
                'bank_account_holder': applicant.bank_account_holder,
            }

        form = BankAccountForm(initial=initial_data)
        context = {
            'form': form,
            'current_step': 2,
            'applicant': applicant
        }
        return render(request, 'front/bank-account-setup.html', context)

    def post(self, request, *args, **kwargs):
        # URLパラメータを取得
        email = unquote(request.GET.get('email', ''))
        uuid = request.GET.get('uuid')

        # メールアドレスまたはUUIDのパラメータが存在しない場合
        if not email or not uuid:
            return redirect('front:top')

        # メールアドレスとUUIDの組み合わせが存在しない場合
        applicant = Applicant.objects.filter(
            email=email, 
            verify_token=uuid,
            app_name__isnull=False
        ).first()
        
        if not applicant:
            return redirect('front:top')
        
        # 通常の保存処理
        form = BankAccountForm(request.POST)
        if form.is_valid():
            # フォームデータの取得
            bank_name = form.cleaned_data['bank_name']
            branch_name = form.cleaned_data['branch_name']
            branch_code = form.cleaned_data['branch_code']
            bank_account_type = form.cleaned_data['bank_account_type']
            bank_account_number = form.cleaned_data['bank_account_number']
            bank_account_holder = form.cleaned_data['bank_account_holder']

            # Applicantモデルに保存
            applicant.bank_name = bank_name
            applicant.branch_name = branch_name
            applicant.branch_code = branch_code
            applicant.bank_account_type = bank_account_type
            applicant.bank_account_number = bank_account_number
            applicant.bank_account_holder = bank_account_holder
        
            applicant.save()

            # 特定商取引法の情報入力へのURLにパラメータを付与
            specified_commercial_transaction_setup_path = reverse('front:specified_commercial_transaction_setup')
            specified_commercial_transaction_setup_url = f"{specified_commercial_transaction_setup_path}?email={quote(email)}&uuid={uuid}"
            return redirect(specified_commercial_transaction_setup_url)

        context = {
            'form': form,
            'current_step': 2,
            'applicant': applicant
        }
        return render(request, 'front/bank-account-setup.html', context)



class SpecifiedCommercialTransactionSetupView(View):
    def get(self, request, *args, **kwargs):
        # URLパラメータを取得
        email = unquote(request.GET.get('email', ''))
        uuid = request.GET.get('uuid')

        # メールアドレスまたはUUIDのパラメータが存在しない場合
        if not email or not uuid:
            return redirect('front:top')
        
        # UUIDの形式チェック
        try:
            UUID(uuid)
        except (ValueError, AttributeError):
            return redirect('front:top')

        # メールアドレスとUUIDの組み合わせが存在しない場合
        applicant = Applicant.objects.filter(
            email=email, 
            verify_token=uuid,
            app_name__isnull=False,
            bank_name__isnull=False
        ).first()
        
        if not applicant:
            return redirect('front:top')

        # 既存のデータがある場合は初期値として設定
        initial_data = {
            'seller_name': applicant.seller_name or '',
            'manager_name': applicant.manager_name or '',
            'seller_address': applicant.seller_address or '',
            'seller_phone_number': applicant.seller_phone_number or '',
            'seller_email': applicant.seller_email or '',
            'product_price': applicant.price_info or '',
            'additional_fees': applicant.additional_fees or '',
            'payment_method': applicant.allowed_payment or '',
            'delivery_method': applicant.delivery_method or '',
            'return_policy': applicant.return_policy or '',
        }

        form = SpecifiedCommercialTransactionForm(initial=initial_data)
        context = {
            'form': form,
            'current_step': 3,
            'applicant': applicant,
            'is_submitted': applicant.is_submitted
        }
        return render(request, 'front/specified_commercial_transaction_setup.html', context)

    def post(self, request, *args, **kwargs):
        # URLパラメータを取得
        email = unquote(request.GET.get('email', ''))
        uuid = request.GET.get('uuid')

        # メールアドレスまたはUUIDのパラメータが存在しない場合
        if not email or not uuid:
            return redirect('front:top')
        
        # UUIDの形式チェック
        try:
            UUID(uuid)
        except (ValueError, AttributeError):
            return redirect('front:top')

        # メールアドレスとUUIDの組み合わせが存在しない場合
        applicant = Applicant.objects.filter(
            email=email, 
            verify_token=uuid,
            app_name__isnull=False,
            bank_name__isnull=False
        ).first()
        
        if not applicant:
            return redirect('front:top')

        form = SpecifiedCommercialTransactionForm(request.POST)
        if form.is_valid():
            # フォームデータの取得
            seller_name = form.cleaned_data['seller_name']
            manager_name = form.cleaned_data['manager_name']
            seller_address = form.cleaned_data['seller_address']
            seller_phone_number = form.cleaned_data['seller_phone_number']
            seller_email = form.cleaned_data['seller_email']
            product_price = form.cleaned_data['product_price']
            additional_fees = form.cleaned_data['additional_fees']
            payment_method = form.cleaned_data['payment_method']
            delivery_method = form.cleaned_data['delivery_method']
            return_policy = form.cleaned_data['return_policy']

            # Applicantモデルに保存
            applicant.seller_name = seller_name
            applicant.manager_name = manager_name
            applicant.seller_address = seller_address
            applicant.seller_phone_number = seller_phone_number
            applicant.seller_email = seller_email
            applicant.price_info = product_price
            applicant.additional_fees = additional_fees
            applicant.allowed_payment = payment_method
            applicant.delivery_method = delivery_method
            applicant.return_policy = return_policy

            applicant.save()

            # setup_confirmへのURLにパラメータを付与
            setup_confirm_path = reverse('front:setup_confirm')
            setup_confirm_url = f"{setup_confirm_path}?email={quote(email)}&uuid={uuid}"
            return redirect(setup_confirm_url)

        context = {
            'form': form,
            'current_step': 3,
            'applicant': applicant
        }
        return render(request, 'front/specified_commercial_transaction_setup.html', context)



class SetupConfirmView(View):
    # 色コードから色名への逆引きマッピング
    REVERSE_COLOR_MAPPING = {
        0: 'サンド',
        1: 'サンセット',
        2: 'オーシャン',
        3: 'フォレスト',
        4: 'ナイト',
    }

    def get(self, request, *args, **kwargs):
        # URLパラメータを取得
        email = unquote(request.GET.get('email', ''))
        uuid = request.GET.get('uuid')

        # メールアドレスまたはUUIDのパラメータが存在しない場合
        if not email or not uuid:
            return redirect('front:top')

        # UUIDの形式チェック
        try:
            UUID(uuid)
        except (ValueError, AttributeError):
            return redirect('front:top')

        # メールアドレスとUUIDの組み合わせが存在しない場合
        # かつ、アプリ設定と口座情報が両方完了している申請者のみアクセス可能
        applicant = Applicant.objects.filter(
            email=email, 
            verify_token=uuid,
            app_name__isnull=False,
            bank_name__isnull=False
        ).first()
        
        if not applicant:
            return redirect('front:top')

        # 画像URLを直接構築
        app_icon_url = None
        app_logo_url = None
        
        if applicant.app_icon:
            app_icon_url = settings.MEDIA_FQDN + applicant.app_icon.name
        
        if applicant.app_logo:
            app_logo_url = settings.MEDIA_FQDN + applicant.app_logo.name
        
        context = {
            'current_step': 4,
            'applicant': applicant,
            'color_name': self.REVERSE_COLOR_MAPPING.get(applicant.app_color, ''),
            'is_submitted': applicant.is_submitted,
            'app_icon_url': app_icon_url,
            'app_logo_url': app_logo_url
        }
        return render(request, 'front/setup_confirm.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        uuid = request.POST.get('uuid')

        # 申請者の検索
        applicant = Applicant.objects.filter(
            email=email,
            verify_token=uuid,
            app_name__isnull=False,
            bank_name__isnull=False,
            is_submitted=False
        ).first()

        if applicant:
            # メールテンプレート用のコンテキスト
            context = {
                'app_name': applicant.app_name,
                'subscription_enabled': 'enabled' if applicant.subscription_enabled else 'disabled',
                'subscription_price': applicant.subscription_price if applicant.subscription_enabled else None,
                'app_color': f'{self.REVERSE_COLOR_MAPPING.get(applicant.app_color, "")}（{applicant.app_color}）',
                'has_app_icon': bool(applicant.app_icon),
                'has_app_logo': bool(applicant.app_logo),
                'naming_enabled': 'enabled' if applicant.naming_enabled else 'disabled',
                'service_name': settings.SERVICE_NAME,
                'naming_fields': {
                    'Home': applicant.home_footer,
                    'Shop': applicant.shop_footer,
                    'Time Line': applicant.timeline_footer,
                    'Chat': applicant.chat_footer,
                    'More': applicant.more_footer,
                    'Collection': applicant.collection,
                    'ピックアップ': applicant.pickup,
                    'グッズ': applicant.goods,
                    '商品': applicant.products,
                    '2shot': applicant.twoshot,
                    'ライブ': applicant.live,
                    'Room': applicant.room,
                    'DM': applicant.dm_short,
                    'アーティストの呼称': applicant.artist_name
                }
            }

            # インライン添付用の画像を準備
            attachments = []
            if applicant.app_icon:
                with applicant.app_icon.open('rb') as f:
                    mime_icon = MIMEImage(f.read())
                    mime_icon.add_header('Content-ID', '<app_icon>')
                    attachments.append({'mime_obj': mime_icon, 'inline': True})

            if applicant.app_logo:
                with applicant.app_logo.open('rb') as f:
                    mime_logo = MIMEImage(f.read())
                    mime_logo.add_header('Content-ID', '<app_logo>')
                    attachments.append({'mime_obj': mime_logo, 'inline': True})

            # 管理者向けメール
            admin_email_body = render_to_string('front/email/app_settings_email.html', context)
            
            # 申請者向けメール
            user_email_body = render_to_string('front/email/app_settings_user_email.html', context)
            
            # 管理者へのメール送信
            send_email(
                to=settings.CONTACT_MAIL_TO,
                subject=f"【{settings.SERVICE_NAME}】アプリの設定情報を受け付けました",
                body=admin_email_body,
                source=settings.MAIL_FROM,
                html=True,
                attachments=attachments if attachments else None
            )
            
            # 申請者へのメール送信
            send_email(
                to=email,
                subject=f"【{settings.SERVICE_NAME}】アプリ設定が完了しました",
                body=user_email_body,
                source=settings.MAIL_FROM,
                html=True
            )

            applicant.is_submitted = True
            applicant.save()
            
            # setup_confirmへのURLにパラメータを付与
            setup_confirm_path = reverse('front:setup_confirm')
            setup_confirm_url = f"{setup_confirm_path}?email={quote(email)}&uuid={uuid}"
            return redirect(setup_confirm_url)
        
        # エラーの場合はトップページにリダイレクト
        return redirect('front:top')



class ContentNamingGuideView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/content_naming_guide.html')



class AppRequestCompleteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/app_request_complete.html')

class CompanyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'front/companye.html')
