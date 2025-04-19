"""
URL configuration for ecosphere project.
"""
from django.contrib import admin
from django.urls import path
from landingecosphere import views as landingecosphere_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landingecosphere_views.landing_page, name='landing_page'),
    path('registro/', landingecosphere_views.registro_view_html, name='registro_view_html'),
    path('login/', landingecosphere_views.login_view_html, name='login_view_html'),
    path('registro/success/', landingecosphere_views.registro_view, name='registro'),
    path('login/success/', landingecosphere_views.login_view, name='login'),
    path('detect/', landingecosphere_views.waste_detection_html, name='waste_detection_html'),
    path('detect/process/', landingecosphere_views.waste_detection, name='waste_detection'),  # Nueva URL
    path('dashboard/', landingecosphere_views.dashboard, name='dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)