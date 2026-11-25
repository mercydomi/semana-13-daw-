from django.db import models
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, db_index=True)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta: ordering = ['nombre']
    def __str__(self): return self.nombre
class Producto(models.Model):
    codigo = models.CharField(max_length=30, unique=True, db_index=True)
    nombre = models.CharField(max_length=150, db_index=True)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.PROTECT, db_index=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    stock = models.PositiveIntegerField(default=0, db_index=True)
    activo = models.BooleanField(default=True, db_index=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_index=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    class Meta: ordering = ['-fecha_creacion']
    def __str__(self): return f'{self.codigo} - {self.nombre}'
