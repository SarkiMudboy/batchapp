from django.db import models

# Create your models here.

class Staff(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    id_num = models.CharField(max_length=50)
    signature = models.ImageField(upload_to='staff', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)