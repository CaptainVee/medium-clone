from django.contrib import admin
from .models import Article, ArticleView, Clap


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["pkid", "author", "title", "slug", "view_count"]
    list_display_links = ["pkid", "author"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["title", "body", "tags"]
    ordering = ["-created_at"]


class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ["pkid", "article", "user", "viewer_ip"]
    list_display_links = ["pkid", "article"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["article", "user", "viewer_ip"]


class ClapAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "article", "user"]
    list_display_links = ["id", "user"]
    list_filter = ["created_at", "updated_at"]


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleView, ArticleViewAdmin)
admin.site.register(Clap, ClapAdmin)
