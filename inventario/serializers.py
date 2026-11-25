from rest_framework import serializers
from .models import Categoria, Producto
class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    productos_count = serializers.SerializerMethodField()
    class Meta:
        model = Categoria
        fields = ['url','id','nombre','descripcion','fecha_creacion','productos_count']
        read_only_fields = ['id','fecha_creacion','productos_count']
        extra_kwargs = {'url': {'view_name':'categoria-detail'}}
    def get_productos_count(self,obj) -> int: return obj.productos.count()
    def validate(self, attrs):
        if 'nombre' in attrs and not attrs['nombre'].strip(): raise serializers.ValidationError({'nombre':'No puede estar vacío.'})
        return attrs
class ProductoSerializer(serializers.HyperlinkedModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    valor_inventario = serializers.SerializerMethodField()
    disponibilidad = serializers.SerializerMethodField()
    class Meta:
        model = Producto
        fields = ['url','id','codigo','nombre','descripcion','categoria','categoria_nombre','precio','stock','activo','fecha_creacion','fecha_actualizacion','valor_inventario','disponibilidad']
        read_only_fields = ['id','fecha_creacion','fecha_actualizacion','categoria_nombre','valor_inventario','disponibilidad']
        extra_kwargs = {'url': {'view_name':'producto-detail'}}
    def get_valor_inventario(self,obj) -> str: return str(obj.precio * obj.stock)
    def get_disponibilidad(self,obj) -> str: return 'Sin stock' if obj.stock == 0 else ('Stock bajo' if obj.stock <= 5 else 'Disponible')
    def validate(self, attrs):
        for field in ('codigo','nombre'):
            if field in attrs and not attrs[field].strip(): raise serializers.ValidationError({field:'No puede estar vacío.'})
        if attrs.get('precio') is not None and attrs['precio'] <= 0: raise serializers.ValidationError({'precio':'Debe ser mayor que cero.'})
        if attrs.get('stock') is not None and attrs['stock'] < 0: raise serializers.ValidationError({'stock':'No puede ser negativo.'})
        return attrs
