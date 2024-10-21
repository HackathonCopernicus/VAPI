from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views import generic
from . import views
from . import models

urlpatterns = [
    path('mapa/', views.mapa, name='Mapa'),
    path('ndvi-map/', views.ndvi_view, name='ndvi_view'),
    path('project/', views.Fincas.as_view(), name='project-list'),
]
