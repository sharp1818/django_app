from django.shortcuts import render

# Create your views here.
# crm/views.py
from django.shortcuts import render
from django.db.models import Q
from .models import Customer
from datetime import datetime, timedelta
from django.utils import timezone

def crm_dashboard(request):
    # Parámetros de filtro
    search_query = request.GET.get('search', '')
    birthday_filter = request.GET.get('birthday', '')
    sort_by = request.GET.get('sort', 'first_name')
    
    # Base queryset
    customers = Customer.objects.select_related('company', 'sales_rep').prefetch_related('interactions')
    
    # Filtro por búsqueda
    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(company__name__icontains=search_query)
        )
    
    # Filtro por cumpleaños esta semana
    if birthday_filter == 'this_week':
        today = timezone.now().date()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        
        customers = customers.filter(
            birth_date__month=end_week.month,
            birth_date__day__range=(start_week.day, end_week.day)
        )
    
    # Ordenamiento
    if sort_by == 'company':
        customers = customers.order_by('company__name', 'first_name')
    elif sort_by == 'birth_date':
        customers = customers.order_by('birth_date__month', 'birth_date__day')
    elif sort_by == 'last_interaction':
        # Para ordenar por última interacción necesitamos una lógica especial
        customers = sorted(
            customers, 
            key=lambda x: x.get_last_interaction().interaction_date if x.get_last_interaction() else datetime.min, 
            reverse=True
        )
    else:
        customers = customers.order_by('first_name', 'last_name')
    
    context = {
        'customers': customers,
        'search_query': search_query,
        'birthday_filter': birthday_filter,
        'sort_by': sort_by,
    }
    
    return render(request, 'crm/dashboard.html', context)