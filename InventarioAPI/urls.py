from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from inventario.views import DashboardView
from django.contrib.auth import views as auth_views
urlpatterns = [path('admin/',admin.site.urls),path('',DashboardView.as_view(),name='dashboard'),path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),path('api/',include('inventario.urls')),path('api/schema/',SpectacularAPIView.as_view(),name='schema'),path('api/docs/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),path('api/redoc/',SpectacularRedocView.as_view(url_name='schema'),name='redoc')]
