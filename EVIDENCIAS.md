# Evidencias para el informe

1. Dashboard `/`: tarjetas alimentadas por `/api/productos/resumen/`, gráfico y tabla paginada.
2. Swagger `/api/docs/`: esquema y ejecución de GET de productos.
3. POST autenticado en Swagger/Postman: respuesta 201 y cálculo de disponibilidad.
4. Filtros `/api/productos/?activo=true&precio__gte=10`: resultado filtrado.
5. Búsqueda y ordenamiento: URL con `search` y `ordering`.
6. `/api/productos/stock_bajo/`: stock 0–5.
7. Admin `/admin/`: productos/categorías y usuarios de demostración.
8. Consola: `test`, `spectacular --validate` y `check --deploy`; capture su salida real.
9. Petición sin autenticar POST: 401/403, demostrando permisos y CSRF cuando use sesión.
10. Peticiones repetidas (ajustando temporalmente límites de prueba): respuesta 429.

No sustituya estas capturas por datos inventados: tómeselas en su instalación después de ejecutar `seed_demo`.
