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
    product_name = models.CharField(max_lenght=100)
    generic_name = models.CharField(max_lenght=100)
    unit_size = models.PositiveIntegerField(help_text='in milligrams', blank=True)
    label_claim = models.PositiveIntegerField(help_text='in milligrams', blank=True)
    packaging = models.ImageField(blank=True, upload_to='products')
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE, default=TABLET)
    product_for = model.CharField(max_length=20, choices=PRODUCT_FOR, default=HUMAN)
    registration_number = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name


class RawMaterial(models.Model):

    # product raw materials
    standard_quantity = models.FloatField(help_text='in kilograms or gram mil', null=True, blank=True)
    potency = models.FloatFieldField(help_text='in percentage', null=True, blank=True)
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

class Specification(models.Model):
    test = models.CharField(max_length=50)
    pharmacopiea = models.CharField(max_length=5, choices=PHARMACOPIEA)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.test

class ManufacturingProcess(models.Model):
    step = models.IntegerField()
    substep = models.CharField(max_length=2)
    action = TextField(blank=True)
    duration = models.IntegerField(help_text='in minutes or seconds')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.action[:10]
