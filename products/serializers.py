from rest_framework import serializers
from .models import Product
import cloudinary.uploader

class ProductSerializer(serializers.ModelSerializer):
    # Campo solo para subir la imagen
    image_file = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Product
        # Incluimos el campo image_file para subir, pero image sigue siendo read-only
        fields = ['id', 'name', 'description', 'price', 'image', 'image_file', 'created_at']
        read_only_fields = ['image', 'created_at']

    def create(self, validated_data):
        # Si envían un archivo, lo subimos a Cloudinary
        uploaded_file = validated_data.pop('image_file', None)
        if uploaded_file:
            result = cloudinary.uploader.upload(uploaded_file)
            validated_data['image'] = result['secure_url']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Mismo proceso para actualización
        uploaded_file = validated_data.pop('image_file', None)
        if uploaded_file:
            result = cloudinary.uploader.upload(uploaded_file)
            validated_data['image'] = result['secure_url']
        return super().update(instance, validated_data)
