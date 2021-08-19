from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='home'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('settings/', views.settings, name='settings'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
