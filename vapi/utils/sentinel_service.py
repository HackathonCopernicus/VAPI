from sentinelhub import SentinelHubRequest, BBox, MimeType, CRS, DataCollection, bbox_to_dimensions, SHConfig

# def get_ndvi_map(bounds):
#     # Define las coordenadas de los límites y el sistema de referencia
#     bbox = BBox(bbox=bounds, crs=CRS.WGS84)

#     # Evalscript para calcular el NDVI
#     evalscript = """
#     //VERSION=3
#     function setup() {
#         return {
#             input: ["B04", "B08"],
#             output: { bands: 1, sampleType: "FLOAT32" }
#         };
#     }

#     function evaluatePixel(sample) {
#         let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
#         return [ndvi];
#     }
#     """

#     # Configuración de Sentinel Hub
#     config = SHConfig()
    
#     config = SHConfig()
#     config.instance_id = 'Yab7e8a16-5cd6-4db7-87c9-ff4f5a46d545'
#     config.sh_client_id = '88902725-5810-4c51-9b02-5ef3a0e02a76'
#     config.sh_client_secret = 'iDKdxxnXXTuUiVss75NpaIVgRqKCzGA9'

#     # Verifica que la configuración esté bien inicializada
#     if not all([config.instance_id, config.sh_client_id, config.sh_client_secret]):
#         print("Error: Configuración de Sentinel Hub incompleta o incorrecta")
#         return None

#     # Solicitud a Sentinel Hub
#     request = SentinelHubRequest(
#         evalscript=evalscript,
#         input_data=[
#             SentinelHubRequest.input_data(
#                 data_collection=DataCollection.SENTINEL2_L2A,
#                 time_interval=("2023-09-01", "2023-10-01")
#             )
#         ],
#         responses=[
#             SentinelHubRequest.output_response("default", MimeType.PNG)
#         ],
#         bbox=bbox,
#         size=bbox_to_dimensions(bbox, resolution=10),
#         config=config
#     )

#     # Devuelve la URL de las teselas
#     try:
#         # Usa el método get_url_list() para obtener las URL
#         tile_urls = request.get_url_list()
#         if tile_urls:
#             return tile_urls[0]  # Devuelve la primera URL de la lista para usar en Leaflet
#     except Exception as e:
#         print(f"Error al obtener el mapa NDVI: {e}")
#         return None

import json
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

# Credenciales de cliente
CLIENT_ID = '7a66f3b0-348b-4b19-9759-0d64b58dd9d8'
CLIENT_SECRET = 'BrsOARxAxR9LgXTFHoambzhOpDhO1RPV'
TOKEN_URL = 'https://services.sentinel-hub.com/oauth/token'
INSTANCE_ID = 'ab7e8a16-5cd6-4db7-87c9-ff4f5a46d545'
# URL para el servicio WMS de Sentinel Hub
WMS_URL = 'https://services.sentinel-hub.com/ogc/wms/{INSTANCE_ID}'

def get_ndvi_map(bbox_coords):
    # Paso 1: Autenticación para obtener el token de acceso
    client = BackendApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=TOKEN_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    # Paso 2: Parámetros de la solicitud WMS para el NDVI
    params = {
        'SERVICE': 'WMS',
        'REQUEST': 'GetMap',
        'LAYERS': 'NDVI',
        'MAXCC': '20',  # Máximo porcentaje de cobertura de nubes
        'BBOX': ','.join(map(str, bbox_coords)),
        'FORMAT': 'image/png',
        'CRS': 'EPSG:4326',
        'WIDTH': '512',
        'HEIGHT': '512',
        'TIME': '2023-01-01/2023-12-31',  # Puedes ajustar este rango de tiempo
    }

    headers = {
        'Authorization': f"Bearer {token['access_token']}",
    }

    # Paso 3: Solicitud GET al servicio WMS de Sentinel Hub
    try:
        response = oauth.get(WMS_URL.format(INSTANCE_ID='ab7e8a16-5cd6-4db7-87c9-ff4f5a46d545'), headers=headers, params=params)
        response.raise_for_status()

        # Si la respuesta es correcta, devolvemos la URL de la imagen
        return response.url

    except Exception as e:
        print(f"Error al obtener NDVI: {e}")
        return None
