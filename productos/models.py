from django.db import models

class Envase(models.Model):
    nombre = models.CharField(max_length=255)
    peso = models.FloatField()

    def __str__(self):
        return f"{self.nombre} ({self.peso} g)"

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    envase = models.ForeignKey(Envase, related_name="productos", on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.IntegerField()
    peso_neto = models.FloatField()

    def __str__(self):
        return self.nombre

    def peso_total(self):
        """Calcula el peso total del producto basado en la cantidad"""
        return self.peso_neto * self.cantidad

    class Meta:
        ordering = ['nombre']
