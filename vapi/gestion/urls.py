from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from gestion.views import home

urlpatterns = [
    path('', home, name = "Inicio"),
]