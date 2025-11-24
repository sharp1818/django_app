# crm/management/commands/generate_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from crm.models import Company, Customer, Interaction
from datetime import datetime, timedelta, date
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Generate fake data for CRM'

    def handle(self, *args, **options):
        self.stdout.write('Generando datos ficticios...')

        # 1. Crear usuarios representantes
        users = []
        for i in range(1, 4):
            user, created = User.objects.get_or_create(
                username=f'rep{i}',
                defaults={
                    'first_name': f'Rep{i}',
                    'last_name': 'Ventas',
                    'email': f'rep{i}@empresa.com',
                    'is_staff': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
            self.stdout.write(f'Usuario creado: {user.username}')

        # 2. Crear compañías
        companies = []
        company_names = [
            'Tech Solutions', 'Global Corp', 'Innovate Ltd', 'Future Systems',
            'Digital Works', 'Smart Tech', 'Next Gen', 'Cloud Masters',
            'Data Systems', 'Web Innovators'
        ]
        
        for name in company_names:
            company, created = Company.objects.get_or_create(name=name)
            companies.append(company)
            self.stdout.write(f'Compañía creada: {company.name}')

        # 3. Crear clientes (1000)
        first_names = ['Ana', 'Carlos', 'María', 'José', 'Laura', 'Miguel', 'Sofia', 'David', 'Elena', 'Pablo']
        last_names = ['García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Flores']

        # Primero borrar clientes existentes para evitar duplicados
        Customer.objects.all().delete()
        
        customers = []
        for i in range(1000):
            birth_year = random.randint(1960, 2000)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            
            customer = Customer.objects.create(
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                birth_date=date(birth_year, birth_month, birth_day),
                company=random.choice(companies),
                sales_rep=random.choice(users)
            )
            customers.append(customer)
            
            if i % 100 == 0:
                self.stdout.write(f'Clientes creados: {i}')

        self.stdout.write('✓ 1000 clientes creados')

        # 4. Crear interacciones (500 por cliente para pruebas)
        interaction_types = ['Call', 'Email', 'SMS', 'Facebook', 'WhatsApp', 'Meeting']
        
        # Borrar interacciones existentes
        Interaction.objects.all().delete()
        
        total_interactions = 0
        for customer in customers:
            # Crear 500 interacciones por cliente
            for j in range(500):
                days_ago = random.randint(0, 365)
                interaction_date = timezone.now() - timedelta(days=days_ago)
                
                Interaction.objects.create(
                    customer=customer,
                    interaction_type=random.choice(interaction_types),
                    notes=f"Interacción {j+1} con {customer.full_name}",
                    interaction_date=interaction_date
                )
                total_interactions += 1

            if customers.index(customer) % 100 == 0:
                self.stdout.write(f'Interacciones creadas: {total_interactions}')

        self.stdout.write(f'✓ {total_interactions} interacciones creadas')
        self.stdout.write(self.style.SUCCESS('¡Todos los datos generados exitosamente!'))