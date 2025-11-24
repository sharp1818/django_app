# django_app
Sharp Santillan

# Crear env, activarlo e instalar requirements.txt
python -m venv env <br>
env\Scripts\activate <br>
pip install -r requirements.txt <br>

# Crear models y aplicar migraciones
python manage.py makemigrations <br>
python manage.py migrate <br>

# Generar datos
python manage.py generate_data <br>

# Ejecutar servidor
python manage.py runserver <br>

# En el navegador ingresar con el link:
http://127.0.0.1:8000/ <br>
