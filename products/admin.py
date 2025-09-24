from django.contrib import admin
from .models import Product
import cloudinary.uploader
from django import forms

# ─── Formulario personalizado para el admin ─────────────
class ProductAdminForm(forms.ModelForm):
    # Campo temporal para subir archivos
    image_file = forms.FileField(required=False, label="Imagen")

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image_file']

# ─── Registro en el admin ───────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("name", "price", "created_at")

    def save_model(self, request, obj, form, change):
        uploaded_file = form.cleaned_data.get('image_file')
        if uploaded_file:
            # Subimos la imagen a Cloudinary
            result = cloudinary.uploader.upload(uploaded_file)
            # Guardamos la URL en el campo URLField
            obj.image = result['secure_url']
        super().save_model(request, obj, form, change)
