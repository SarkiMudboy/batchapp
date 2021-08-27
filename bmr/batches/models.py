from django.db import models
from products.models import Product, Specification
from staff.models import Staff

# Create your models here.

class Batch(models.Model):

    # batch information
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=20)
    gross_weight = models.FloatField(help_text='in kilograms', blank=True, null=True)
    net_weight = models.FloatField(help_text='in kilograms', blank=True, null=True)
    manufacturing_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    batch_size = models.IntegerField(null=True, blank=True)
    percentage_yield = models.IntegerField(help_text='in percentage', blank=True, null=True)
    expected_yield = models.IntegerField(help_text='in percentage', blank=True, null=True)
    actual_yield = models.FloatField(blank=True, null=True)
    pack_size = models.IntegerField(blank=True, null=True)
    production_commencement = models.DateField(blank=True, null=True)
    production_completion = models.DateField(blank=True, null=True)
    release_status = models.BooleanField(default=False, blank=True, null=True)
    yield_deviation_limit = models.FloatField(help_text='+/-', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.batch_number} for {self.product.name}'

# Quality Control (Chemical and Microbiological)

class Test(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class TestResult(models.Model):

    RESULT_TYPE = [
        ('CHM', 'CHEMICAL'),
        ('MCR', 'MICRO')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    result = models.IntegerField(blank=True, null=True)
    id_complies = models.NullBooleanField(blank=True, null=True)
    result_type = models.CharField(max_length=20, choices=RESULT_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.test + self.batch + ' test result' 

class QualityControlAnalysis(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch = models.ForeignKey(batch, on_delete=models.CASCADE)
    ar_number = models.CharField(max_length=50)

    # results
    results = models.ManyToManyField(TestResult, blank=True, null=True)
    result_pharmacopiea = models.ForeignKey(Specification, blank=True, null=True)
    pharmacopiea_specification_year = models.DateField(blank=True, null=True)

    # auth 
    chemical_analyst = models.Foreignkey(Staff, blank=True, null=True, on_delete=models.CASCADE)
    microbiologist = models.Foreignkey(Staff, blank=True, null=True, on_delete=models.CASCADE)
    quality_control_manager = models.Foreignkey(Staff, blank=True, null=True, on_delete=models.CASCADE) # check back later for correction

    def __str__(self):
        return self.batch + ' quality control analysis'

# Quality Control In Process

class ControlRecords(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    test = models.CharField(max_length=50)
    result = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=10, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.test + self.batch + ' control record'

class IndividualWieght(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    position = models.AutoField()
    weight = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + self.position + "'s weight"


class CleaningProcess(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    process_description = models.TextField(max_length=1000)
    action_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.process_description[:10] + self.batch + ' cleaning process'

class InprocessAuth(models.Models):
    batch = OneToOneField(Batch)
    action_by = models.ManyToManyField(Staff, blank=True, null=True, on_delete=models.CASCADE)
    checked_by = models.ManyToManyField(Staff, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + ' in process authentication'

# Raw Materials

class RawMaterialBatch(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    batch = model.CharField(max_length=50)
    manufacturing_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return {self.raw_material} + ' ' + {self.batch}

class RawMaterialCheckRecord(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterialBatch, on_delete=models.CASCADE)
    weighed_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.CASCADE)
    date_tested = models.DateField(null=True, blank=True)
    result = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.raw_material + self.batch + ' check record'

class RawMaterialCheckRecordAuth(models.Model):
    batch = OneToOneField(Batch)
    check_done_by = models.ManyToManyField(Staff, blank=True, null=True)
    assignment = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.CASCADE)
    total_assignment = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + ' check record authentication'

class RawMaterialPackagingBill(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    action_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.CASCADE)
    quantity_dispensed = models.IntegerField(help_text='in kilograms', blank=True, null=True)
    dispensed_to = models.CharField(max_length=50)
    dispense_label_auth = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.raw_material + self.batch + ' raw material packaging bill'

class RawMaterialBillAuth(models.Model):
    batch = models.OneToOneField(Batch)
    confirmed_by = models.ManyToManyField(Staff, blank=True, null=True, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + ' raw material bill authentication'














