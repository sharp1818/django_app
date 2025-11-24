# crm/management/commands/generate_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from crm.models import Company, Customer, Interaction
from datetime import datetime, timedelta, date
import random
from django.utils import timezone
import numpy as np

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

        # 3. Crear 1000 clientes 
        first_names = ['Ana', 'Carlos', 'María', 'José', 'Laura', 'Miguel', 'Sofia', 'David', 'Elena', 'Pablo']
        last_names = ['García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Flores']

        # Borrar clientes existentes para evitar duplicados
        Customer.objects.all().delete()
        
        # Generar datos de clientes con numpy
        n_customers = 1000
        
        # Generar años, meses y días de nacimiento de forma vectorizada
        birth_years = np.random.randint(1960, 2001, n_customers)
        birth_months = np.random.randint(1, 13, n_customers)
        birth_days = np.random.randint(1, 29, n_customers)
        
        # Seleccionar compañías y representantes aleatorios
        company_indices = np.random.randint(0, len(companies), n_customers)
        user_indices = np.random.randint(0, len(users), n_customers)
        
        # Crear clientes en lotes
        customers = []
        batch_size = 100
        
        for i in range(0, n_customers, batch_size):
            end_idx = min(i + batch_size, n_customers)
            batch_customers = []
            
            for j in range(i, end_idx):
                customer = Customer(
                    first_name=random.choice(first_names),
                    last_name=random.choice(last_names),
                    birth_date=date(int(birth_years[j]), int(birth_months[j]), int(birth_days[j])),
                    company=companies[company_indices[j]],
                    sales_rep=users[user_indices[j]]
                )
                batch_customers.append(customer)
            
            # Bulk create del lote
            Customer.objects.bulk_create(batch_customers)
            customers.extend(batch_customers)
            self.stdout.write(f'Clientes creados: {end_idx}/{n_customers}')

        self.stdout.write('✓ 1000 clientes creados')

        # 4. Crear 500 interacciones por cliente
        interaction_types = ['Call', 'Email', 'SMS', 'Facebook', 'WhatsApp', 'Meeting']
        
        # Borrar interacciones existentes
        Interaction.objects.all().delete()

        self.stdout.write('Creando interacciones con numpy...')

        total_interactions_needed = len(customers) * 500
        batch_size = 10000

        
        # 1. Generar índices de clientes (cada cliente repetido 500 veces)
        customer_indices = np.repeat(np.arange(len(customers)), 500)
        
        # 2. Generar tipos de interacción aleatorios
        random_types = np.random.choice(interaction_types, total_interactions_needed)
        
        # 3. Generar días aleatorios (0-365 días atrás)
        random_days = np.random.randint(0, 366, total_interactions_needed)
        
        # 4. Generar todas las fechas de una vez
        now = timezone.now()
        random_dates = [now - timedelta(days=int(days)) for days in random_days]
        
        # 5. Crear interacciones en lotes
        interactions_batch = []
        
        for i in range(total_interactions_needed):
            customer_idx = customer_indices[i]
            customer = customers[customer_idx]
            interaction_num = (i % 500) + 1
            
            interactions_batch.append(
                Interaction(
                    customer=customer,
                    interaction_type=str(random_types[i]),
                    notes=f"Interacción {interaction_num} con {customer.full_name}",
                    interaction_date=random_dates[i]
                )
            )
            
            # Crear por lotes para no sobrecargar la memoria
            if len(interactions_batch) >= batch_size:
                Interaction.objects.bulk_create(interactions_batch)
                self.stdout.write(f'Lote creado: {len(interactions_batch)} interacciones (total: {i+1}/{total_interactions_needed})')
                interactions_batch = []
        
        # Crear las interacciones restantes
        if interactions_batch:
            Interaction.objects.bulk_create(interactions_batch)
            self.stdout.write(f'Lote final creado: {len(interactions_batch)} interacciones')

        self.stdout.write(f'✓ {total_interactions_needed} interacciones creadas con numpy')
        self.stdout.write(self.style.SUCCESS('¡Todos los datos generados exitosamente!'))

        # Estadísticas de rendimiento
        self.stdout.write(f'\n--- ESTADÍSTICAS ---')
        self.stdout.write(f'• Usuarios creados: {len(users)}')
        self.stdout.write(f'• Compañías creadas: {len(companies)}')
        self.stdout.write(f'• Clientes creados: {len(customers)}')
        self.stdout.write(f'• Interacciones creadas: {total_interactions_needed:,}')
        self.stdout.write(f'• Relación interacciones/cliente: 500:1')