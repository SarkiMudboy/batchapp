from django.db import models

# Create your models here.

class RawMaterial(models.Model):

    # raw materials
    name = models.CharField(max_length=64)
    code_number = models.CharField(max_length=10, blank=True, null=True)
    lrn_number = models.CharField(max_length=10, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name