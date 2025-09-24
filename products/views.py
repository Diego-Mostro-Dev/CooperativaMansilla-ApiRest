# products/views.py
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product
from .serializers import ProductSerializer
from .models import Category
from .serializers import CategorySerializer

# products/views.py
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]  # Ajustar
    parser_classes = [MultiPartParser, FormParser]  # Permite subir archivos desde la API

    def get_queryset(self):
        # Solo productos con estado 'active' y stock mayor a 0
        return Product.objects.filter(status='active', stock__gt=0)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]  # Restringir luego
