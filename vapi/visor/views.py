from django.shortcuts import render
from django.http import JsonResponse
import requests
from utils.sentinel_service import get_ndvi_map
from django.db.models import Q
import json
from visor.models import Finca
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Renderiza la página del mapa
def mapa(request):
    return render(request, "visor/mapa.html")

def ndvi_view(request):
    if request.method == "POST":
        try:
            # Cargar los datos de la solicitud
            data = json.loads(request.body)
            bounds = data.get("bounds", {})

            if not bounds or 'coordinates' not in bounds:
                return JsonResponse({"error": "No se recibieron límites válidos."}, status=400)

            # Extraer las coordenadas del bbox (lat, lon)
            bbox_coords = [
                bounds["coordinates"][0][0][1],  # latitud del suroeste
                bounds["coordinates"][0][0][0],  # longitud del suroeste
                bounds["coordinates"][0][2][1],  # latitud del noreste
                bounds["coordinates"][0][2][0]   # longitud del noreste
            ]

            # Llama a la función para obtener la URL del NDVI
            ndvi_url = get_ndvi_map(bbox_coords)
            if not ndvi_url:
                return JsonResponse({"error": ndvi_url}, status=500)

            return JsonResponse({"ndvi_url": ndvi_url})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato de JSON inválido."}, status=400)

        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido."}, status=405)

class Fincas(generic.ListView):
    template_name = "visor/visorList.html"
    model = Finca
    paginate_by = 12  # Paginación de 12 elementos

    def get_queryset(self):
        # Obtener usuario y la búsqueda del campo 'buscar'
        queryset2 = self.request.GET.get('buscar')
        usuario = self.request.user
        
        # Filtrar por usuario que sea dueño o tenga acceso compartido
        consulta = Q(tecnico=usuario)   # Relación con sharedUsers
        queryset = Finca.objects.filter(consulta).distinct()
        
        # Si se ha ingresado una búsqueda, aplicarla
        if queryset2:
            palabras = queryset2.split()
            condiciones_busqueda = []

            for palabra in palabras:
                # Búsqueda en nombre y descripción de la finca
                condiciones_busqueda.append(Q(nombre__icontains=palabra) | Q(descripcion__icontains=palabra))

            # Aplicar las condiciones de búsqueda
            consulta = Q()
            for condicion in condiciones_busqueda:
                consulta |= condicion
            queryset = queryset.filter(consulta)

        return queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
   
