from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.throttling import AnonRateThrottle
from django.core.cache import cache
from .models import Categoria, Producto
class ApiTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user('tester',password='Clave123!'); self.client=APIClient(); self.cat=Categoria.objects.create(nombre='Prueba')
        self.p=Producto.objects.create(codigo='P-001',nombre='Teclado',categoria=self.cat,precio=Decimal('20'),stock=4)
    def auth(self): self.client.force_authenticate(self.user)
    def test_list_and_filters(self):
        r=self.client.get('/api/productos/',{'search':'Teclado','precio__gte':10,'ordering':'precio'}); self.assertEqual(r.status_code,200); self.assertEqual(r.data['count'],1)
    def test_create_validation_and_duplicate(self):
        self.auth(); data={'codigo':'P-002','nombre':'Mouse','categoria':self.cat.pk,'precio':'15.50','stock':3}; self.assertEqual(self.client.post('/api/productos/',data,format='json').status_code,201)
        data['precio']='0'; self.assertEqual(self.client.post('/api/productos/',data,format='json').status_code,400)
        data['precio']='2'; data['codigo']='P-001'; self.assertEqual(self.client.post('/api/productos/',data,format='json').status_code,400)
    def test_update_delete_permissions_and_custom(self):
        self.assertEqual(self.client.patch(f'/api/productos/{self.p.pk}/',{'stock':2},format='json').status_code,403)
        self.auth(); self.assertEqual(self.client.patch(f'/api/productos/{self.p.pk}/',{'stock':2},format='json').status_code,200); self.assertEqual(self.client.get('/api/productos/stock_bajo/').status_code,200); self.assertEqual(self.client.get('/api/productos/resumen/').status_code,200); self.assertEqual(self.client.delete(f'/api/productos/{self.p.pk}/').status_code,204)
    def test_schema_cors_and_not_found(self):
        self.assertEqual(self.client.get('/api/schema/').status_code,200); self.assertEqual(self.client.options('/api/productos/',HTTP_ORIGIN='http://localhost:8000').status_code,200); self.assertEqual(self.client.get('/api/productos/999/').status_code,404)

    def test_anonymous_throttle_returns_429(self):
        previous = AnonRateThrottle.THROTTLE_RATES.copy()
        AnonRateThrottle.THROTTLE_RATES = {**previous, 'anon': '1/minute'}
        cache.clear()
        try:
            self.client.logout()
            self.assertEqual(self.client.get('/api/categorias/').status_code, 200)
            self.assertEqual(self.client.get('/api/categorias/').status_code, 429)
        finally:
            AnonRateThrottle.THROTTLE_RATES = previous
            cache.clear()
