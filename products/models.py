# products/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(_("Nombre"), max_length=100)
    description = models.TextField(_("Descripción"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Categoría")
        verbose_name_plural = _("Categorías")


class Product(models.Model):
    STATUS_CHOICES = [
    ('active', _('Activo')),
    ('inactive', _('Inactivo')),
    ('out_of_stock', _('No tiene stock')),
]


    name = models.CharField(_("Nombre"), max_length=200)
    description = models.TextField(_("Descripción"), blank=True)
    price = models.DecimalField(_("Precio"), max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(_("Stock"), default=0)
    status = models.CharField(_("Estado"), max_length=20, choices=STATUS_CHOICES, default='active')
    image = models.URLField(_("Imagen"), blank=True)
    category = models.ForeignKey(Category, verbose_name=_("Categoría"), on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(_("Creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Actualizado el"), auto_now=True)
    external_id = models.CharField(_("ID externo"), max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.status = 'out_of_stock'
        elif self.stock > 0 and self.status == 'out_of_stock':
            self.status = 'active'
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")
