from rest_framework import serializers
from .models import Product, Category
import cloudinary.uploader

class ProductSerializer(serializers.ModelSerializer):
    image_file = serializers.ImageField(write_only=True, required=False)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price',
            'stock', 'status', 'status_display',
            'image', 'image_file', 'created_at'
        ]
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

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']