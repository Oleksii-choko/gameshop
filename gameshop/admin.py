from django.contrib import admin
from django.utils.html import format_html
from .models import *

# Допоміжні таблички
admin.site.register(Tag)
admin.site.register(Language)
admin.site.register(Platform)
admin.site.register(Genre)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', "image_thumb", 'get_games_count')
    readonly_fields = ("image_preview",)
    prepopulated_fields = {'slug': ('title',)}

    def get_games_count(self, obj):  # вывести з бд количество предметов по категории
        if obj.games:
            return str(len(obj.games.all()))
        else:
            return '0'

    get_games_count.short_description = 'Количество товаров'

    @admin.display(description="Мініатюра", empty_value="—")
    def image_thumb(self, obj):
        if obj.image and getattr(obj.image, "url", None):
            return format_html(
                '<img src="{}" width="75" height="75" style="object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )

    @admin.display(description="Прев’ю")
    def image_preview(self, obj):
        if obj.pk and obj.image and getattr(obj.image, "url", None):
            return format_html('<img src="{}" style="max-height:180px;" />', obj.image.url)
        return "—"


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'price', 'discount_percent', 'stock', 'is_published', 'image_thumb')
    list_editable = ('price', 'discount_percent', 'stock', 'is_published')
    list_filter = ('is_published', 'price', 'discount_percent', 'platforms')
    list_display_links = ('title', 'pk')
    readonly_fields = ('watched', "image_preview",)
    prepopulated_fields = {'slug': ('title',)}

    @admin.display(description="Мініатюра", empty_value="—")
    def image_thumb(self, obj):
        if obj.image and getattr(obj.image, "url", None):
            return format_html(
                '<img src="{}" width="75" height="75" style="object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )

    @admin.display(description="Прев’ю")
    def image_preview(self, obj):
        if obj.pk and obj.image and getattr(obj.image, "url", None):
            return format_html('<img src="{}" style="max-height:180px;" />', obj.image.url)
        return "—"


@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name','email', 'subject', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name','last_name','email','phone')
    list_filter = ('first_name', 'email')
    search_fields = ('first_name', 'last_name', 'email', 'subject', 'message')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'text', 'created_at','game')
    list_filter = ('user', 'game')
    readonly_fields = ('created_at',)
