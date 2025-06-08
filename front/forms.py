from django import forms
import re
from django.core.exceptions import ValidationError
from front.models import Applicant
from PIL import Image
from io import BytesIO

class ContactForm(forms.Form):
    CATEGORY_CHOICES = [
        ('', '選択してください'),
        ('general', '一般的なお問い合わせ'),
        ('business', 'ビジネスに関するお問い合わせ'),
        ('technical', '技術的なお問い合わせ'),
        ('other', 'その他')
    ]

    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        }),
        error_messages={
            'invalid': '正しいメールアドレスの形式で入力してください。'
        }
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        error_messages={
            'required': 'お問い合わせカテゴリを選択してください。'
        }
    )
    message = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5
        })
    )



class ApplicationForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        }),
        error_messages={
            'invalid': '正しいメールアドレスの形式で入力してください。'
        }
    )
    website_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
        }),
        error_messages={
            'invalid': '正しいURLの形式で入力してください。'
        }
    )
    x_account = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://x.com/',
            'class': 'form-control',
        })
    )
    instagram = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.instagram.com/',
            'class': 'form-control',
        })
    )
    youtube = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.youtube.com/',
            'class': 'form-control',
        })
    )
    tiktok = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.tiktok.com/@',
            'class': 'form-control',
        })
    )
    followers_count = forms.IntegerField(
        required=True,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
        error_messages={
            'required': '総フォロワー数を入力してください。'
        }
    )
    remarks = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Applicant.objects.filter(email=email).exists():
            raise ValidationError(
                'このメールアドレスでは既に申請が完了しています。',
                code='duplicate_email'
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        
        # メインSNSフィールドのチェック
        main_sns_fields = [
            cleaned_data.get('x_account'),
            cleaned_data.get('instagram'),
            cleaned_data.get('youtube'),
            cleaned_data.get('tiktok')
        ]
        has_main_sns = any(main_sns_fields)
        
        # その他のSNSのチェック
        other_sns_entries = []
        for key, value in self.data.items():
            if key.startswith('other_sns_name_'):
                index = key.split('_')[-1]
                url_key = f'other_sns_url_{index}'
                
                name_val = value.strip()
                url_val = self.data.get(url_key, '').strip()
                
                if name_val or url_val:
                    other_sns_entries.append((name_val, url_val))
        
        # その他のSNSの完全性チェック
        for name, url in other_sns_entries:
            if bool(name) != bool(url):
                raise forms.ValidationError(
                    'その他のSNSは名前とURLの両方を入力してください。',
                    code='incomplete_other_sns'
                )
        
        has_valid_other_sns = any(name and url for name, url in other_sns_entries)
        
        # SNS全体の必須チェック
        if not (has_main_sns or has_valid_other_sns):
            raise forms.ValidationError(
                'SNSアカウント情報は少なくとも1つ入力してください。',
                code='required_sns'
            )

        return cleaned_data




class AppSettingsForm(forms.Form):
    app_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    SUBSCRIPTION_CHOICES = [
        ('enabled', '有効にする'),
        ('disabled', '有効にしない')
    ]
    subscription_enabled = forms.ChoiceField(
        choices=SUBSCRIPTION_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'subscription-radio'
        }),
        initial='disabled'
    )
    
    subscription_price = forms.IntegerField(
        required=False,
        min_value=100,
        max_value=100000,
        initial=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': 10
        })
    )
    
    COLOR_MAPPING = {
        'Color_01': (0, 'サンド'),
        'Color_02': (1, 'サンセット'),
        'Color_03': (2, 'オーシャン'),
        'Color_04': (3, 'フォレスト'),
        'Color_05': (4, 'ナイト'),
    }

    app_color = forms.ChoiceField(
        choices=[(k, v[1]) for k, v in COLOR_MAPPING.items()],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_app_color(self):
        color_code = self.cleaned_data['app_color']
        return self.COLOR_MAPPING[color_code][0]
    
    app_icon = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/jpg'
        })
    )
    
    app_logo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/png'
        })
    )


    NAMING_CHOICES = [
        ('enabled', '有効にする'),
        ('disabled', '有効にしない')
    ]
    naming_enabled = forms.ChoiceField(
        choices=NAMING_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'naming-radio'
        }),
        initial='disabled'
    )

    home = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    shop = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    timeline = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    chat = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    more = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    collection = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    pickup = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    goods = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    products = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    twoshot = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    live = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    room = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    dm = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    artist_name = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    def __init__(self, *args, applicant=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.applicant = applicant

    def clean(self):
        cleaned_data = super().clean()
        app_icon = cleaned_data.get('app_icon')
        app_logo = cleaned_data.get('app_logo')

        # 新規アップロードがない場合は既存の画像があるかチェック
        if not app_icon and (not self.applicant or not self.applicant.app_icon):
            self.add_error('app_icon', 'アプリアイコン画像は必須です。')
        if not app_logo and (not self.applicant or not self.applicant.app_logo):
            self.add_error('app_logo', 'ロゴ画像は必須です。')

        return cleaned_data

    def clean_subscription_price(self):
        price = self.cleaned_data.get('subscription_price')
        if price is not None:
            if price % 10 != 0:
                raise forms.ValidationError('月額料金は10円単位で入力してください')
        return price

    def clean_app_icon(self):
        icon = self.cleaned_data.get('app_icon')
        if icon:
            # ファイル形式のチェック
            if not icon.content_type in ['image/jpeg', 'image/jpg']:
                raise forms.ValidationError('JPGまたはJPEG形式の画像を選択してください')
            
            # 画像サイズのチェック
            img = Image.open(icon)
            if img.width != 512 or img.height != 512:
                raise forms.ValidationError('アプリアイコンは512×512ピクセルのサイズが必要です')
            # ファイルポインタを先頭に戻す
            icon.seek(0)
        return icon

    def clean_app_logo(self):
        logo = self.cleaned_data.get('app_logo')
        if logo:
            # ファイル形式のチェック
            if not logo.content_type == 'image/png':
                raise forms.ValidationError('PNG形式の画像を選択してください')
            
            # 画像サイズのチェック
            img = Image.open(logo)
            if img.width != 500 or img.height != 1024:
                raise forms.ValidationError('ロゴ画像は500×1024ピクセルのサイズが必要です')
            # ファイルポインタを先頭に戻す
            logo.seek(0)
        return logo




class BankAccountForm(forms.Form):
    bank_name = forms.CharField(
        max_length=255,
        required=True,
        label='金融機関名',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    branch_name = forms.CharField(
        max_length=255,
        required=True,
        label='支店名',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    branch_code = forms.CharField(
        max_length=3,
        required=True,
        label='支店コード',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    bank_account_type = forms.ChoiceField(
        choices=[(1, "普通"), (2, "当座")],
        required=True,
        label='口座種別',
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    bank_account_number = forms.CharField(
        max_length=7,
        required=True,
        label='口座番号',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    bank_account_holder = forms.CharField(
        max_length=255,
        required=True,
        label='口座名義',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    # 支店コードのバリデーション
    def clean_branch_code(self):
        branch_code = self.cleaned_data.get('branch_code')
        if branch_code:
            # 3桁の半角数字かチェック
            if not re.match(r'^\d{3}$', branch_code):
                raise ValidationError('3桁の半角数字で入力してください')
        return branch_code
    
    # 口座番号のバリデーション
    def clean_bank_account_number(self):
        bank_account_number = self.cleaned_data.get('bank_account_number')
        if bank_account_number:
            # 7桁の半角数字かチェック
            if not re.match(r'^\d{7}$', bank_account_number):
                raise ValidationError('7桁の半角数字で入力してください')
        return bank_account_number
    
    # 口座名義のバリデーション
    def clean_bank_account_holder(self):
        bank_account_holder = self.cleaned_data.get('bank_account_holder')
        if bank_account_holder:
            # カタカナかチェック
            if not re.match(r'^[ァ-ヶー\s]+$', bank_account_holder):
                raise ValidationError('口座名義はカタカナで入力してください')
        return bank_account_holder



class SpecifiedCommercialTransactionForm(forms.Form):
    seller_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '株式会社〇〇'
        })
    )
    
    manager_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '山田 太郎'
        })
    )
    
    seller_address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '〒100-0001 東京都千代田区千代田1-1'
        })
    )
    
    seller_phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': '[0-9-]+',
            'placeholder': '03-1234-5678'
        })
    )
    
    seller_email = forms.EmailField(
        max_length=255,
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'info@example.com'
        })
    )
    
    product_price = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': '価格は各商品ページに税込みで表示しています。'
        })
    )
    
    additional_fees = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': '送料：本州〇〇円　四国・九州・北海道〇〇円　沖縄〇〇円離島料金はかかりません。'
        })
    )
    
    payment_method = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'クレジットカード決済'
        })
    )
    
    delivery_method = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': '当方にて手配後、運送会社による発送'
        })
    )
    
    return_policy = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 12,
            'placeholder': '「不良品・当社の商品の間違い」の場合は当社が負担いたします。\n'
                         '配送途中の破損などの事故がございましたら、弊社までご連絡下さい。\n'
                         '送料・手数料ともに弊社負担で早急に新品をご送付致します。\n'
                         '【返品対象】\n'
                         '「不良品・当社の商品の間違い」の場合\n'
                         '【返品時期】\n'
                         'ご購入後〇〇日以内にご連絡があった場合に返金可能となります。\n'
                         '【返品方法】\n'
                         'メールにて返金要請してください。\n'
                         '〇〇日以内にご購入代金を指定の口座へお振込みいたします。'
        })
    )
    
    # 電話番号のバリデーション
    def clean_seller_phone_number(self):
        phone_number = self.cleaned_data.get('seller_phone_number')
        if phone_number:
            # ハイフンが2つ以上含まれているかチェック
            hyphens = phone_number.count('-')
            if hyphens < 2:
                raise forms.ValidationError('正しい電話番号を入力してください')
            
            # 数字とハイフンのみを許可する正規表現パターン
            pattern = re.compile(r'^[0-9-]+$')
            if not pattern.match(phone_number):
                raise forms.ValidationError('電話番号は数字とハイフンのみで入力してください。')
        return phone_number
    
    # メールアドレスのバリデーション
    def clean_seller_email(self):
        email = self.cleaned_data.get('seller_email')
        if email:
            # メールアドレスの形式チェック
            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                raise ValidationError('有効なメールアドレスを入力してください')
        return email