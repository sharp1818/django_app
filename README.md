# django_app
Sharp Santillan

# Crear env, activarlo e instalar requirements.txt
python -m venv env
env\Scripts\activate
pip install -r requirements.txt

# Crear models y aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Generar datos
python manage.py generate_data

# Ejecutar servidor
python manage.py runserver

# En el navegador ingresar con el link:
http://127.0.0.1:8000/