# Imagen base
FROM python:3.11

# Setea el directorio de trabajo
WORKDIR /app

# Copia los archivos de la app al contenedor
COPY . /app/
COPY requirements.txt /app/
COPY ./vapi/secrets/ /app/secrets/
COPY ./scripts/ /app/scripts/

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # fonts-freefont-ttf \
    postgresql \
    libgdal-dev \
    gdal-bin \
    python3-psycopg2 \
    binutils \
    postgresql-contrib \
    nginx && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y \
    postgis && \
    rm -rf /var/lib/apt/lists/*

# Instala las dependencias de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Ejecuta el servidor de Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "vapi.wsgi:application"]
