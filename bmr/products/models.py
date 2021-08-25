from django.db import models

# Create your models here.

class Product(models.Model):

    # PRODUCT TYPE
    CAPLET = 'CP'
    TABLET = 'TB'
    BOLUS = 'BL'

    # PRODUCT FOR
    HUMAN = 'HM'
    VET = 'VT'

    PRODUCT_TYPE = [
        (CAPLET, 'CAPLET'),
        (TABLET, 'TABLET'),
        (BOLUS, 'BOLUS'),
    ]

    PRODUCT_FOR = [
        (HUMAN, 'HUMAN'),
        (VET, 'VET'),
    ]

    product_name = models.CharField(max_lenght=100)
    generic_name = models.CharField(max_lenght=100)
    unit_size = models.IntegerField(blank=True)
    label_claim = models.IntegerField(blank=True)
    packaging = models.ImageField(upload_to='products')
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE, default=TABLET)
    product_for = model.CharField(max_length=20, choices=PRODUCT_FOR, default=HUMAN)
    
    def __str__(self):
        return self.product_name


class RawMaterial(models.Model):
    pass

class Equipment(models.Model):
    pass

class Specification(models.Model):
    pass

class ManufacturingProcess(models.Model):
    pass