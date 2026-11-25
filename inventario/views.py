from django.db.models import Count, F, Sum, DecimalField, ExpressionWrapper
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.prefetch_related('productos').all()
    serializer_class = CategoriaSerializer
    search_fields = ['nombre','descripcion']; ordering_fields = ['nombre','fecha_creacion']
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related('categoria').all()
    serializer_class = ProductoSerializer
    filterset_fields = {'categoria':['exact'],'activo':['exact'],'precio':['gte','lte']}
    search_fields = ['nombre','codigo','descripcion']; ordering_fields = ['precio','stock','fecha_creacion']
    @action(detail=False, methods=['get'])
    def stock_bajo(self, request):
        queryset = self.get_queryset().filter(stock__lte=5)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(queryset, many=True).data)
    @action(detail=False, methods=['get'])
    def resumen(self, request):
        qs=self.get_queryset(); valor=qs.aggregate(v=Sum(ExpressionWrapper(F('precio')*F('stock'),output_field=DecimalField(max_digits=15,decimal_places=2))))['v'] or 0
        return Response({'total_productos':qs.count(),'productos_activos':qs.filter(activo=True).count(),'stock_bajo':qs.filter(stock__lte=5).count(),'valor_total':valor,'por_categoria':list(qs.values('categoria__nombre').annotate(total=Count('id')).order_by('categoria__nombre'))})
@method_decorator(ensure_csrf_cookie, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'inventario/dashboard.html'
