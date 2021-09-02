from django.db import models
from rawmaterials.models import RawMaterialBatch
from django.urls import reverse

# Create your models here.

class Product(models.Model):

    # PRODUCT TYPE
    CAPLET = 'CP'
    TABLET = 'TB'
    BOLUS = 'BL'

    # PRODUCT FOR
    HUMAN = 'HM'
    VET = 'VT'

    # PHARMACOPIEA
    USP = 'USP'
    BP = 'BP'

    PRODUCT_TYPE = [
        (CAPLET, 'CAPLET'),
        (TABLET, 'TABLET'),
        (BOLUS, 'BOLUS'),
    ]

    PRODUCT_FOR = [
        (HUMAN, 'HUMAN'),
        (VET, 'VET'),
    ]

    PHARMACOPIEA = [
        (USP, 'USP'),
        (BP, 'BP')
        ]

    # product drug
    product_name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    unit_size = models.PositiveIntegerField(help_text='in milligrams', blank=True, null=True)
    label_claim = models.PositiveIntegerField(help_text='in milligrams', blank=True, null=True)
    packaging = models.ImageField(blank=True, null=True, upload_to='products')
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE, default=TABLET)
    product_for = models.CharField(max_length=20, choices=PRODUCT_FOR, default=HUMAN)
    equipments = models.ManyToManyField('Equipment', blank=True, null=True)
    registration_number = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk' : self.pk})


class RawMaterial(models.Model):

    # product raw materials
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.ForeignKey(RawMaterialBatch, on_delete=models.CASCADE)
    standard_quantity = models.FloatField(help_text='in kilograms or gram mil', null=True, blank=True)
    potency = models.FloatField(help_text='in percentage', null=True, blank=True)
    percentage_formula = models.FloatField(help_text='in percentage', null=True, blank=True)
    unit_formula_quantity = models.FloatField(help_text='in milligrams', null=True, blank=True)
    batch_formula = models.FloatField(help_text='in kilograms or gram mil', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    id_num = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Test(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    specification = models.FloatField(blank=True)
    deviation = models.FloatField(blank=True, null=True)
    pharmacopiea = models.CharField(max_length=5, choices=Product.PHARMACOPIEA)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.test

class ManufacturingProcess(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    step = models.IntegerField()
    substep = models.CharField(max_length=2)
    action = models.TextField(max_length=250)
    duration = models.DurationField(help_text='in minutes or seconds', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.action[:10]
