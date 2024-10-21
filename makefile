.PHONY: docker-up docker-build migrate clean env

setup:
	make clean env docker-build; \

super-user:
	docker-compose up -d
	docker-compose exec -e DJANGO_SUPERUSER_EMAIL=$(DJANGO_SUPERUSER_EMAIL) web python manage.py shell -c "exec(open('/app/scripts/create_superuser.py').read())"
	docker-compose down

# Levantar los contenedores de Docker
docker-up:
	docker-compose up

# Construir la imagen de Docker
docker-build:
	docker-compose up --build

# Migrar la base de datos de Django
migrate:
	docker-compose up -d
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate
	docker-compose down

# Limpiar los datos y contenedores de Docker
clean:
	docker-compose down -v
	rm -rf $(VENV_DIR)
	rm -f .env
	docker system prune


# Crear el archivo .env automáticamente
env:
	@read -p "¿Estás trabajando en un entorno de producción? (y/n): " IS_PRODUCTION; \
	export IS_PRODUCTION; \
	echo "Configurando el archivo .env..."; 
	@if [ "$$IS_PRODUCTION" = "y" ]; then \
		read -p "Introduce el dominio del servidor (p.ej., example.com): " domain; \
	else \
		domain="localhost"; \
	fi; \
	echo "DJANGO_ALLOWED_HOSTS=$$domain" > .env; \
	echo "CSRF_TRUSTED_ORIGINS=https://$$domain" >> .env; \
	echo "CERTBOT_DOMAIN=$$domain" >> .env; \
	read -p "Introduce el correo electrónico para el superusuario: " email; \
	secret_key=$$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))'); \
	echo "POSTGRES_DB=valdi" >> .env; \
	echo "POSTGRES_USER=postgres" >> .env; \
	echo "POSTGRES_PASSWORD=copernicus" >> .env; \
	echo "POSTGRES_HOST=db" >> .env; \
	echo "POSTGRES_PORT=5432" >> .env; \
	read -p "Introduce una contraseña para el superusuario: " password; \
	echo "DJANGO_SECRET_KEY=$$secret_key" >> .env; \
	echo "DJANGO_APP=vapi" >> .env; \
	echo "IS_PRODUCTION=$$IS_PRODUCTION" >> .env; \
	if [ "$$IS_PRODUCTION" = "y" ]; then \
		echo "DJANGO_DEBUG=False" >> .env; \
		echo "NGINX_HTTPS_PORT=443" >> .env; \
	else \
		echo "DJANGO_DEBUG=True" >> .env; \
		echo "NGINX_HTTPS_PORT=" >> .env; \
	fi; \
	echo "DJANGO_SUPERUSER_EMAIL=$$email" >> .env; \
	echo "CERTBOT_EMAIL=$$email" >> .env;
