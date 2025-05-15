from django.db import models
from django.contrib.auth import get_user_model
from django.core.serializers import serialize


class Container(models.Model):
    name = models.CharField(max_length=255, unique=True)
    weight = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)  # Para saber cuándo fue creado

    def __str__(self):
        return f"{self.name} ({self.weight} g)"

    def to_json(self):
        """
        Método para serializar el container a JSON de forma personalizada.
        """
        return {
            'id': self.id,
            'name': self.name,
            'weight': self.weight,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

    class Meta:
        ordering = ['-created_at']  # Ordena por fecha de creación, más reciente primero

class Product(models.Model):
    name = models.CharField(max_length=255)
    container = models.ForeignKey(Container, related_name="products", on_delete=models.SET_NULL, null=True, blank=True)
    container_weight_at_time = models.FloatField(null=True, blank=True)  # <-- nuevo campo
    quantity = models.IntegerField()
    net_weight = models.FloatField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Si es nuevo o el container ha cambiado, guarda el peso del container en ese momento
        if self.container and (not self.pk or Product.objects.get(pk=self.pk).container_id != self.container_id):
            self.container_weight_at_time = self.container.weight
        super().save(*args, **kwargs)

    def total_weight(self):
        return self.net_weight - (self.container_weight_at_time or 0)

    def to_json(self):
        """
        Método para serializar el producto a JSON de forma personalizada.
        """
        return {
            'id': self.id,
            'name': self.name,
            'container': f"{self.container.name} ({self.container_weight_at_time} g)" if self.container else "Sin envase",
            'quantity': self.quantity,
            'net_weight': self.net_weight,
            'total_weight': self.total_weight(),
        }

    class Meta:
        ordering = ['-id']


class Order(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('pos', 'Card'),
        ('mobile', 'Mobile Payment'),
        ('dollar', 'Dollar'),
        ('none', 'Not Paid Yet'),
    ]

    MODE_OPTIONS = [
        ('takeaway', 'Takeaway'),
        ('dinein', 'Dine-in'),
    ]

    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    table = models.CharField(max_length=10, blank=True, null=True)
    order_number = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='none')

    mode = models.CharField(max_length=10, choices=MODE_OPTIONS)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.order_number} - {self.customer_name}"

    def to_json(self):
        return {
            'order_number': self.order_number,
            'customer_name': self.customer_name,
            'phone_number': self.phone_number,
            'table': self.table,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'paid': self.paid,
            'payment_method': self.get_payment_method_display(),
            'mode': self.get_mode_display(),
            'notes': self.notes,
            'details': [detail.to_json() for detail in self.details.all()],
        }

class OrderDetail(models.Model):
    PRODUCT_OPTIONS = [
        ('promo1', 'Promotion 1'),
        ('promo2', 'Promotion 2'),
        ('promo3', 'Promotion 3'),
        ('promo4', 'Promotion 4'),
        ('promo5', 'Promotion 5'),
        ('individual', 'Individual Pizza'),
        ('other', 'Other'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details')
    product_type = models.CharField(max_length=20, choices=PRODUCT_OPTIONS)
    description = models.CharField(max_length=255)  # Free text for specific product description
    quantity = models.PositiveIntegerField(default=1)
    extra_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_product_type_display()} x{self.quantity}"

    def to_json(self):
        return {
            'id': self.id,
            'product_type': self.get_product_type_display(),
            'description': self.description,
            'quantity': self.quantity,
            'extra_notes': self.extra_notes,
        }
