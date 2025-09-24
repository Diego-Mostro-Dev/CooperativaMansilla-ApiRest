from django.contrib import admin
from .models import Category, Product
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)
    verbose_name = _("Categoría")
    verbose_name_plural = _("Categorías")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "status", "category", "created_at", "updated_at", "image_tag")
    list_filter = ("status", "category")
    search_fields = ("name", "description", "external_id")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "image_preview")

    fieldsets = (
        (_("Información del producto"), {
            "fields": ("name", "description", "category", "status")
        }),
        (_("Stock y precio"), {
            "fields": ("price", "stock")
        }),
        (_("Imagen"), {
            "fields": ("image", "image_preview")
        }),
        (_("Integración"), {
            "fields": ("external_id",)
        }),
        (_("Fechas"), {
            "fields": ("created_at", "updated_at")
        }),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px; border-radius: 5px;" />', obj.image)
        return _("Sin imagen")
    image_tag.short_description = _("Vista previa")

    def image_preview(self, obj):
        """Muestra la imagen más grande en la edición"""
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 10px;" />', obj.image)
        return _("Sin imagen")
    image_preview.short_description = _("Vista previa")


