from django.db import models
import uuid
from datetime import datetime, date, timedelta
import os
import secured_fields
from stdimage.models import StdImageField


def path_and_rename(instance, filename):
    upload_to = instance.prefix + "/" + datetime.now().strftime('%Y%m%d')
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)

    return os.path.join(upload_to, filename)


class Applicant(models.Model):
    prefix = "applicant"

    BANK_ACCOUNT_TYPE = (
        (1, "普通"),
        (2, "当座"),
    )

    email                 = models.CharField(verbose_name='メールアドレス', max_length=255, db_index=True, unique=True)
    verify_token          = models.UUIDField(verbose_name='UUID', db_index=True, default=uuid.uuid4)
    app_settings_url      = models.URLField(verbose_name='アプリ申請URL', max_length=1000, blank=True, null=True)
    
    is_submitted          = models.BooleanField(verbose_name='2段階目申請送信済み', default=0)

    client_name           = models.CharField(verbose_name='お名前・法人名', max_length=255, blank=True, null=True)
    website_url           = models.URLField(verbose_name='公式サイト URL', max_length=1000, blank=True, null=True)
    x_account             = models.CharField(verbose_name='X（旧Twitter）', max_length=255, blank=True, null=True)
    instagram             = models.CharField(verbose_name='Instagram', max_length=255, blank=True, null=True)
    youtube               = models.CharField(verbose_name='YouTube', max_length=255, blank=True, null=True)
    ticktock              = models.CharField(verbose_name='ticktock', max_length=255, blank=True, null=True)
    followers_count       = models.IntegerField(verbose_name='総フォロワー数', blank=True, null=True)
    remarks               = models.TextField(verbose_name='備考欄', max_length=1000, blank=True, null=True)
    other_sns             = models.JSONField(verbose_name='その他のSNS', blank=True, null=True, default=list)

    app_name              = models.CharField(verbose_name='希望するアプリ名（仮）', max_length=255, blank=True, null=True)
    subscription_enabled  = models.BooleanField(verbose_name='月額有料会員プランの追加', default=0)
    subscription_price    = models.IntegerField(verbose_name='月額有料会員の金額', blank=True, null=True)
    app_color             = models.IntegerField(verbose_name='初期のアプリカラー', default=0)
    app_icon              = models.ImageField(verbose_name='アプリアイコン画像', upload_to=path_and_rename, blank=True, null=True)
    app_logo              = models.ImageField(verbose_name='ロゴ画像', upload_to=path_and_rename, blank=True, null=True)
    naming_enabled        = models.BooleanField(verbose_name='コンテンツの呼称変更の希望', default=0)

    home_header           = models.CharField(verbose_name='ホーム（ヘッダー）', max_length=255, blank=True, null=True)
    home_footer           = models.CharField(verbose_name='Home（フッター）', max_length=255, blank=True, null=True)
    shop_header           = models.CharField(verbose_name='ショップ（ヘッダー）', max_length=255, blank=True, null=True)
    shop_footer           = models.CharField(verbose_name='Shop（フッター）', max_length=255, blank=True, null=True)
    timeline_header       = models.CharField(verbose_name='タイムライン（ヘッダー）', max_length=255, blank=True, null=True)
    timeline_footer       = models.CharField(verbose_name='TL（フッター）', max_length=255, blank=True, null=True)
    chat_header           = models.CharField(verbose_name='チャット（ヘッダー）', max_length=255, blank=True, null=True)
    chat_footer           = models.CharField(verbose_name='Chat（フッター）', max_length=255, blank=True, null=True)
    more_header           = models.CharField(verbose_name='More', max_length=255, blank=True, null=True)
    more_footer           = models.CharField(verbose_name='More（フッター）', max_length=255, blank=True, null=True)
    collection            = models.CharField(verbose_name='コレクション', max_length=255, blank=True, null=True)
    pickup                = models.CharField(verbose_name='ピックアップ', max_length=255, blank=True, null=True)
    goods                 = models.CharField(verbose_name='グッズ', max_length=255, blank=True, null=True)
    products              = models.CharField(verbose_name='商品', max_length=255, blank=True, null=True)
    twoshot               = models.CharField(verbose_name='2shot', max_length=255, blank=True, null=True)
    live                  = models.CharField(verbose_name='ライブ', max_length=255, blank=True, null=True)
    room                  = models.CharField(verbose_name='ルーム', max_length=255, blank=True, null=True)
    dm_long               = models.CharField(verbose_name='ダイレクトメッセージ', max_length=255, blank=True, null=True)
    dm_short              = models.CharField(verbose_name='DM', max_length=255, blank=True, null=True)
    artist_name           = models.CharField(verbose_name='アーティストの呼称', max_length=255, blank=True, null=True)

    store_description_short  = models.CharField(verbose_name='ストア掲載用アプリ概要（短文）', max_length=30, blank=True, null=True)
    store_description_long   = models.TextField(verbose_name='ストア掲載用アプリ概要（詳細）',  max_length=4000, blank=True, null=True)
    screenshot_text_enabled  = models.BooleanField(verbose_name='スクリーンショット文言変更の希望', default=0)

    screenshot_text_a        = models.CharField(verbose_name='スクリーンショット文言A', max_length=50, blank=True, null=True)
    screenshot_text_b        = models.CharField(verbose_name='スクリーンショット文言B', max_length=50, blank=True, null=True)
    screenshot_text_c        = models.CharField(verbose_name='スクリーンショット文言C', max_length=50, blank=True, null=True)
    screenshot_text_d        = models.CharField(verbose_name='スクリーンショット文言D', max_length=50, blank=True, null=True)
    screenshot_text_e        = models.CharField(verbose_name='スクリーンショット文言E', max_length=50, blank=True, null=True)
    screenshot_text_f        = models.CharField(verbose_name='スクリーンショット文言F', max_length=50, blank=True, null=True)
    screenshot_text_g        = models.CharField(verbose_name='スクリーンショット文言G', max_length=50, blank=True, null=True)
    store_copyright          = models.CharField(verbose_name='ストア著作権表記', max_length=50, blank=True, null=True)

    bank_name             = models.CharField(verbose_name='銀行名', max_length=255, blank=True, null=True)
    branch_name           = models.CharField(verbose_name='銀行支店名', max_length=255, blank=True, null=True)
    branch_code           = models.CharField(verbose_name='銀行支店コード', max_length=10, blank=True, null=True)
    bank_account_number   = secured_fields.EncryptedCharField(verbose_name='口座番号', max_length=30, blank=True, null=True)
    bank_account_holder   = secured_fields.EncryptedCharField(verbose_name='口座名義', max_length=255, blank=True, null=True)
    bank_account_type     = models.SmallIntegerField(verbose_name='口座の種類', choices=BANK_ACCOUNT_TYPE, blank=True, null=True)
    
    seller_name	          = models.CharField(verbose_name="販売業者名", max_length=255, blank=True, null=True)
    manager_name	      = models.CharField(verbose_name="運営統括責任者名", max_length=255, blank=True, null=True)
    seller_address	      = models.CharField(verbose_name="販売業者所在地", max_length=255, blank=True, null=True)
    seller_phone_number   = models.CharField(verbose_name="販売業者電話番号", max_length=20, blank=True, null=True)
    seller_email	      = models.CharField(verbose_name="販売業者メールアドレス", max_length=255, blank=True, null=True)
    price_info            = models.TextField(verbose_name="商品の販売価格", max_length=1000, blank=True, null=True)
    additional_fees	      = models.TextField(verbose_name="商品代金以外の必要料金", max_length=1000, blank=True, null=True)
    allowed_payment	      = models.TextField(verbose_name="支払い方法", max_length=1000, blank=True, null=True)
    delivery_method	      = models.TextField(verbose_name="商品の引渡方法", max_length=1000, blank=True, null=True)
    return_policy         = models.TextField(verbose_name="返品・不良品対応", max_length=1000, blank=True, null=True)

    created_at            = models.DateTimeField(verbose_name='データ作成日時', auto_now_add=True)
    updated_at            = models.DateTimeField(verbose_name='データ更新日時', auto_now=True)

    class Meta():
        verbose_name_plural = '01-01. 申し込み者'
        db_table = 'applicant'



class ArticleCategory(models.Model):
    prefix = "article_category"
    name            = models.CharField('カテゴリ名', max_length=100)
    slug            = models.SlugField('スラッグ', unique=True)

    description     = models.TextField('カテゴリ概要', blank=True, null=True)
    seo_keywords    = models.TextField('SEOキーワード群（カンマ区切り）', blank=True, null=True)
    is_published    = models.BooleanField(verbose_name='公開', default=False)
    created_at      = models.DateTimeField(verbose_name='データ作成日時', auto_now_add=True)
    updated_at      = models.DateTimeField(verbose_name='データ更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = '02-01. 記事カテゴリ'
        db_table = 'article_category'

    def __str__(self):
        return f"{self.id}: {self.name}"

class ArticleTag(models.Model):
    name            = models.CharField('タグ名', max_length=50)
    slug            = models.SlugField('スラッグ', unique=True)

    created_at      = models.DateTimeField(verbose_name='データ作成日時', auto_now_add=True)
    updated_at      = models.DateTimeField(verbose_name='データ更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = '02-02. タグ'
        db_table = 'article_tag'

    def __str__(self):
        return f"{self.id}: {self.name}"


class Article(models.Model):
    prefix       = "article"

    title           = models.CharField(verbose_name='タイトル', max_length=200)
    category        = models.ForeignKey(ArticleCategory, verbose_name='カテゴリ', on_delete=models.SET_NULL, null=True, blank=True)
    eyecatch_title  = models.CharField(verbose_name='アイキャッチタイトル',max_length=20,blank=True,null=True)
    thumbnail_image = models.ImageField(verbose_name='アイキャッチ画像', upload_to=path_and_rename, blank=True, null=True)
    is_published    = models.BooleanField(verbose_name='公開', default=False)
    publish_date    = models.DateTimeField(verbose_name='公開日時', blank=True, null=True,)
    slug            = models.SlugField(verbose_name='スラッグ', unique=True)
    content         = models.TextField(verbose_name='本文')
    summary         = models.TextField(verbose_name='記事要約', max_length=500, blank=True, null=True)
    tags            = models.ManyToManyField(ArticleTag, verbose_name='タグ', blank=True)
    table_of_contents  = models.TextField(verbose_name='目次', blank=True, null=True)
    lead_text       = models.TextField(verbose_name='リード文', blank=True, null=True)
    meta            = models.JSONField(verbose_name="メタデータ", blank=True, null=True, default=dict)
    view_count      = models.PositiveIntegerField(verbose_name='閲覧数', default=0)

    is_seed_generated = models.BooleanField(verbose_name='タイトル・要約のみ生成済', default=False, help_text='記事生成がレディになった時は外す。')
    embedding       = models.JSONField(verbose_name='埋め込みベクトル', blank=True, null=True, help_text='タイトル＋要約のベクトル表現（text-embedding-3-small）')

    created_at      = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at      = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = '02-03. 記事'
        db_table = 'article'
