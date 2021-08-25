from django.db import models
from products.models import Product, Specification

# Create your models here.

class Batch(models.Model):

    # batch information
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=20)
    gross_weight = models.FloatField(help_text='in kilograms')
    net_weight = models.FloatField(help_text='in kilograms')
    manufacturing_date = models.DateField(blank=True)
    expiry_date = models.DateField(blank=True)
    batch_size = models.IntegerField(null=True)
    percentage_yield = models.IntegerField(help_text='in percentage', blank=True)
    expected_yield = models.IntegerField(help_text='in percentage', blank=True)
    actual_yield = models.FloatField(blank=True)
    pack_size = models.IntegerField(blank=True)
    production_commencement = models.DateField(blank=True)
    production_completion = models.DateField(blank=True)
    release_status = models.BooleanField(default=False)
    yield_deviation_limit = models.FloatField(help_text='+/-')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.batch_number} for {self.product.name}'

# Quality Control (Chemical and Microbiological)

class TestResult(models.Model):

    RESULT_TYPE = [
        ('CHM', 'CHEMICAL'),
        ('MCR', 'MICRO')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch = models.ForeignKey(batch, on_delete=models.CASCADE)
    # test
    result = models.IntegerField(blank=True, null=True)
    id_complies = models.NullBooleanField()
    result_type = models.CharField(max_length=20, choices=RESULT_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class QualityControlAnalysis(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch = models.ForeignKey(batch, on_delete=models.CASCADE)
    ar_number = models.CharField(max_length=50)

    # results
    results = models.ManyToManyField(TestResult)
    result_pharmacopiea = models.ForeignKey(Specification)
    pharmacopiea_specification_year = models.DateField()


