from django.contrib import admin

# Register your models here.
# crm/admin.py
from django.contrib import admin
from .models import Company, Customer, Interaction

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company', 'sales_rep', 'birth_date']
    list_filter = ['company', 'sales_rep']

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'interaction_type', 'interaction_date']
    list_filter = ['interaction_type', 'interaction_date']