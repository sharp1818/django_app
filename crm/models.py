from django.db import models

# Create your models here.
# crm/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class Company(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customers')
    sales_rep = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    def get_last_interaction(self):
        return self.interactions.first()

class Interaction(models.Model):
    INTERACTION_TYPES = [
        ('Call', 'Llamada'),
        ('Email', 'Correo'),
        ('SMS', 'SMS'),
        ('Facebook', 'Facebook'),
        ('WhatsApp', 'WhatsApp'),
        ('Meeting', 'Reunión'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    notes = models.TextField(blank=True)
    interaction_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.interaction_type} with {self.customer}"

    class Meta:
        ordering = ['-interaction_date']