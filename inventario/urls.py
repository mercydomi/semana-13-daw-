from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductoViewSet
router=DefaultRouter(); router.register('productos',ProductoViewSet,basename='producto'); router.register('categorias',CategoriaViewSet,basename='categoria')
urlpatterns=router.urls
