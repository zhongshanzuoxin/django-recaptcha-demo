from django.contrib.sitemaps import Sitemap
from django.urls import reverse
import re

from app.models import Article, ArticleCategory, ArticleTag

class StaticViewSitemap(Sitemap):
    priority   = 1.0
    changefreq = "weekly"

    def items(self):
        return [
            "front:top",
            "front:goods_shop",
            "front:digital_goods_shop",
            "front:2shot_shop",
            "front:live",
            "front:2shot",
            "front:timeline",
            "front:collection",
            "front:room",
            "front:dm",
            "front:moderation",
            "front:delivery_management",
            "front:permission_management",
            "front:account_management",
            "front:permissions_overview",
            "front:revenue",
            "front:help",
            "front:privacy",
            "front:contact",
            "front:app_request",
            "front:app_request_complete",
            "front:app_settings",
            "front:bank_account_setup",
            "front:specified_commercial_transaction_setup",
            "front:setup_confirm",
            "front:content_naming_guide",
            "front:company",
        ]

    def location(self, name):
        return reverse(name)


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority   = 0.8

    def items(self):
        return Article.objects.filter(is_published=True)

    # ★ get_absolute_url が無いので明示的に location() をオーバーライド
    def location(self, obj):
        return reverse("front:column_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority   = 0.6

    def items(self):
        return ArticleCategory.objects.all()

    def location(self, obj):
        return reverse("front:column_category", kwargs={"slug": obj.slug})


class TagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        # [-a-zA-Z0-9_] に完全一致する slug のみ対象とする
        return ArticleTag.objects.filter(slug__regex=r'^[-a-zA-Z0-9_]+$')

    def location(self, obj):
        return reverse("front:column_tag", kwargs={"slug": obj.slug})