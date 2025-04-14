from django.db import models

class Container(models.Model):
    name = models.CharField(max_length=255, unique=True)
    weight = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.weight} g)"


from django.db import models
from django.core.serializers import serialize

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
        ordering = ['name']



