# InventarioAPI

Práctica 13 de Desarrollo de Aplicaciones Web (UNCP): una API REST de inventario en Django 5 y una interfaz web responsive que consume esa API.

## Tecnologías y arquitectura

Django, Django REST Framework, SQLite, django-filter, CORS Headers y drf-spectacular. La aplicación `inventario` contiene modelos, serializadores, ViewSets, rutas, pruebas y comando de datos; `InventarioAPI` centraliza la configuración. La interfaz está en `templates/` y `static/`.

## Instalación y ejecución

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Credenciales de desarrollo: `admin_demo` / `Demo12345!` y `usuario_demo` / `Demo12345!`. Son datos locales de demostración; cámbielos antes de desplegar. El comando crea también un token por usuario, consultable desde Admin.

## URLs

| Ruta | Uso |
|---|---|
| `/` | Dashboard web |
| `/api/productos/` | CRUD de productos, filtros, búsqueda y paginación |
| `/api/categorias/` | CRUD de categorías |
| `/api/productos/stock_bajo/` | Productos con stock ≤ 5 |
| `/api/productos/resumen/` | Indicadores del dashboard |
| `/api/schema/`, `/api/docs/`, `/api/redoc/` | OpenAPI, Swagger y ReDoc |
| `/admin/` | Administración Django |

Ejemplo: `GET /api/productos/?categoria=1&activo=true&precio__gte=10&precio__lte=50&search=mouse&ordering=-precio&page=1`.

## Cinco fases y REST

1. Configuración DRF centralizada: autenticación de sesión/token, permisos `IsAuthenticatedOrReadOnly`, paginación de 5 y throttling (100/h anónimo, 1000/h usuario).
2. Serializadores explícitos y hipervinculados; validan precio, stock, textos y unicidad. Exponen `url`, valor de inventario y disponibilidad, aplicando HATEOAS básico.
3. `ModelViewSet` y `DefaultRouter` dan CRUD HTTP (GET, POST, PUT, PATCH, DELETE); las acciones `stock_bajo` y `resumen` concentran las consultas adicionales.
4. Filtros SQL, búsqueda, ordenamiento e índices evitan filtrado en memoria.
5. CORS restringido por `.env`, CSRF activo para sesiones (AJAX debe enviar `X-CSRFToken`) y documentación OpenAPI.

## Verificación

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py check
python manage.py test
python manage.py spectacular --file schema.yml --validate
python manage.py check --deploy
```

`check --deploy` puede advertir sobre `DEBUG=True`, una clave de desarrollo y ausencia de HTTPS: son esperables en entorno local y deben cambiarse en producción. Los resultados reales de esta ejecución se registran tras ejecutar los comandos en la entrega.

## GitHub

```powershell
git init
git add .
git commit -m "Implementa InventarioAPI"
git branch -M main
git remote add origin URL_DEL_REPOSITORIO
git push -u origin main
```

La asistencia de IA se utilizó para implementar y documentar el proyecto; los resultados de pruebas indicados proceden de los comandos ejecutados, no de evidencias inventadas.
