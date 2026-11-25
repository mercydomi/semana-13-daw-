from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from inventario.models import Categoria, Producto
class Command(BaseCommand):
    help = 'Crea datos reproducibles de demostración.'
    def handle(self,*args,**kwargs):
        categorias=[]
        for n,d in [('Electrónica','Dispositivos y accesorios'),('Oficina','Suministros de oficina'),('Hogar','Artículos para el hogar'),('Deportes','Equipamiento deportivo'),('Libros','Material de lectura')]: categorias.append(Categoria.objects.get_or_create(nombre=n,defaults={'descripcion':d})[0])
        for i in range(30):
            Producto.objects.update_or_create(codigo=f'DEMO-{i+1:03}',defaults={'nombre':f'Producto demostración {i+1}','descripcion':'Datos de ejemplo reproducibles','categoria':categorias[i%5],'precio':Decimal('9.90')+i*Decimal('3.25'),'stock':[0,2,5,12,30,50][i%6],'activo':i%7!=0})
        for username,staff in [('admin_demo',True),('usuario_demo',False)]:
            u,created=User.objects.get_or_create(username=username,defaults={'is_staff':staff,'is_superuser':staff})
            u.is_staff=staff; u.is_superuser=staff; u.set_password('Demo12345!'); u.save(); Token.objects.get_or_create(user=u)
        self.stdout.write(self.style.SUCCESS('Datos listos: admin_demo y usuario_demo; contraseña Demo12345!'))
