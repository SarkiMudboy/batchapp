from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from products.models import Product, Specification, Test, Equipment, ManufacturingProcess
from staff.models import Staff
from rawmaterials.models import RawMaterial, RawMaterialBatch

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

class TestResult(models.Model):

    RESULT_TYPE = [
        ('CHM', 'CHEMICAL'),
        ('MCR', 'MICRO')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    result = models.IntegerField(blank=True, null=True)
    id_complies = models.BooleanField(blank=True, null=True)
    result_type = models.CharField(max_length=20, choices=RESULT_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.test + self.batch + ' test result' 

class QualityControlAnalysis(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    ar_number = models.CharField(max_length=50)

    # results
    results = models.ManyToManyField(TestResult, blank=True, null=True)
    result_pharmacopiea = models.ForeignKey(Specification, blank=True, null=True, on_delete=models.CASCADE)
    pharmacopiea_specification_year = models.DateField(blank=True, null=True)

    # auth 
    chemical_analyst = models.ForeignKey(Staff, related_name='%(class)s_chemical_analyst', blank=True, null=True, on_delete=models.CASCADE)
    microbiologist = models.ForeignKey(Staff, related_name='%(class)s_microbiologist', blank=True, null=True, on_delete=models.CASCADE)
    quality_control_manager = models.ForeignKey(Staff, related_name='%(class)s_QC_manager', blank=True, null=True, on_delete=models.CASCADE) # check back later for correction

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
    weight = models.CharField(validators=[validate_comma_separated_integer_list], max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + self.position + "'s weight"


class CleaningProcess(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    process_description = models.TextField(max_length=1000)
    action_by = models.ForeignKey(Staff, blank=True, null=True, related_name='%(class)s_action_by', on_delete=models.CASCADE)
    checked_by = models.ForeignKey(Staff, blank=True, null=True, related_name='%(class)s_checked_by', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.process_description[:10] + self.batch + ' cleaning process'

class InprocessAuth(models.Model):
    batch = models.OneToOneField(Batch, on_delete=models.CASCADE)
    action_by = models.ManyToManyField(Staff, related_name='%(class)s_action_by', blank=True, null=True)
    checked_by = models.ManyToManyField(Staff, related_name='%(class)s_checked_by', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + ' in process authentication'

# Raw Materials

class RawMaterialCheckRecord(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterialBatch, on_delete=models.CASCADE)
    weighed_by = models.ForeignKey(Staff, related_name='%(class)s_weighed_by', blank=True, null=True, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(Staff, related_name='%(class)s_checked_by', blank=True, null=True, on_delete=models.CASCADE)
    date_tested = models.DateField(null=True, blank=True)
    result = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.raw_material + self.batch + ' check record'

class RawMaterialCheckRecordAuth(models.Model):
    batch = models.OneToOneField(Batch, on_delete=models.CASCADE)
    check_done_by = models.ManyToManyField(Staff, blank=True, null=True)
    assignment = models.ForeignKey(Staff, related_name='%(class)s_assignment', blank=True, null=True, on_delete=models.CASCADE)
    total_assignment = models.ForeignKey(Staff, related_name='%(class)s_total_assignment', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + ' check record authentication'

class RawMaterialPackagingBill(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    action_by = models.ForeignKey(Staff, related_name='%(class)s_action_by', blank=True, null=True, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(Staff, related_name='%(class)s_checked_by', blank=True, null=True, on_delete=models.CASCADE)
    quantity_dispensed = models.IntegerField(help_text='in kilograms', blank=True, null=True)
    dispensed_to = models.CharField(max_length=50)
    dispense_label_auth = models.ForeignKey(Staff, related_name='%(class)s_auth_by', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.raw_material + self.batch + ' raw material packaging bill'

class RawMaterialBillAuth(models.Model):
    batch = models.OneToOneField(Batch, on_delete=models.CASCADE)
    confirmed_by = models.ManyToManyField(Staff, blank=True)
    approved_by = models.ForeignKey(Staff, related_name='%(class)s_approved_by', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + ' raw material bill authentication'

# Equipments

class EquipmentCheck(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    remark = models.CharField(max_length=10)
    last_product = models.ForeignKey(Product, related_name='%(class)s_last_product', blank=True, null=True, on_delete=models.CASCADE)
    action_by = models.ForeignKey(Staff, related_name='%(class)s_action_by', blank=True, null=True, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(Staff, related_name='%(class)s_checked_by', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + self.equipment + 'check'

class EquipmentClearance(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    last_product = models.ForeignKey(Product, related_name='%(class)s_last_product', blank=True, null=True, on_delete=models.CASCADE)
    next_product = models.ForeignKey(Product, related_name='%(class)s_next_product', blank=True, null=True, on_delete=models.CASCADE)
    check = models.TextField(max_length=500)
    cleaned_by = models.ForeignKey(Staff, related_name='%(class)s_cleaned_by', blank=True, null=True, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(Staff, related_name='%(class)s_checked_by', blank=True, null=True, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(Staff, related_name='%(class)s_approved_by', blank=True, null=True, on_delete=models.CASCADE)
    quality_assurance_manager = models.ForeignKey(Staff, related_name='%(class)s_qa_manager', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + self.equipment + 'clearance'

# Manufacturing 

class BatchManufacturingProcess(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    step = models.ForeignKey(ManufacturingProcess, on_delete=models.CASCADE)
    action_from = models.DateTimeField(blank=True, null=True)
    action_to = models.DateTimeField(blank=True, null=True)
    action_by = models.ForeignKey(Staff, related_name='%(class)s_action_by', blank=True, null=True, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(Staff, related_name='%(class)s_checked_by', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + self.step + 'process'

# Auth
class BatchManufacturingProcessAuth(models.Model):
    process = models.OneToOneField(BatchManufacturingProcess, on_delete=models.CASCADE)
    manufacturing_commenced = models.DateField()
    manufacturing_completed = models.DateField()
    production_manager = models.ForeignKey(Staff, related_name='%(class)s_production_manager', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + self.process + 'authentication'

# Packaging

class PackagingMaterial(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    material = models.CharField(max_length=100)
    dimension = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.material


class BillOfPackaging(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    material = models.ForeignKey(PackagingMaterial, on_delete=models.CASCADE)
    quantity_required = models.IntegerField(null=True, blank=True)
    actual_quantity = models.IntegerField(null=True, blank=True)
    action_by = models.ForeignKey(Staff, related_name='%(class)s_action_by', blank=True, null=True, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(Staff, related_name='%(class)s_checked_by', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + self.material + "packaging bill"

class BatchPackagingProcess(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    process = models.TextField(max_length=100)
    action_by = models.ForeignKey(Staff, related_name='%(class)s_action_by', blank=True, null=True, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(Staff, related_name='%(class)s_checked_by', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + "packaging process"

class BatchPackagingAuth(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    confirmed_by = models.ManyToManyField(Staff)
    approved_by = models.ForeignKey(Staff, related_name='%(class)s_approved_by', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + "packaging process authentication"

# product reconciliation

class ProductReconciliation(models.Model):

    # samples
    purpose = models.TextField(max_length=100)
    quantity = models.IntegerField(null=True, blank=True)
    collected_by = models.ForeignKey(Staff, related_name='%(class)s_approved_by', blank=True, null=True, on_delete=models.CASCADE)
    issued_by = models.ForeignKey(Staff, related_name='%(class)s_issued_by', blank=True, null=True, on_delete=models.CASCADE)
    sales_quantity = models.CharField(max_length=100)
    remarks = models.TextField(max_length=50)

    # packaging materials
    item = models.ForeignKey(PackagingMaterial, on_delete=models.CASCADE)
    quantity_supplied = models.IntegerField(blank=True, null=True)
    quantity_damaged = models.IntegerField(blank=True, null=True)
    quantity_rejected = models.IntegerField(blank=True, null=True)
    quantity_returned = models.IntegerField(blank=True, null=True)
    quantity_used = models.IntegerField(blank=True, null=True)
    percentage_breakage = models.FloatField(help_text='in percentage', blank=True, null=True)
    percentage_damages = models.FloatField(help_text='in percentage', blank=True, null=True)
    deviation = models.FloatField(help_text='+/- (%)', blank=True, null=True)
    comments = models.TextField(null=True, blank=True)

    # yeild
    pack_sizes = models.CharField(validators=[validate_comma_separated_integer_list], max_length=200, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + "product reconciliation"

# release profile

class ReleaseProfile(models.Model):
    parameter = models.CharField(max_length=100)
    test = models.ForeignKey(Test, blank=True, null=True, on_delete=models.CASCADE)
    analytical_result = models.BooleanField(default=False)
    checked_by = models.ForeignKey(Staff, related_name='%(class)s_checked_by', blank=True, null=True, on_delete=models.CASCADE)
    remark = models.TextField(max_length=50)
    quality_assurance_manager = models.ForeignKey(Staff, related_name='%(class)s_qa_manager', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch + "release profile"

class Guide(models.Model):
    standard_instructions = models.TextField(max_length=8000)
    issuance = models.TextField(max_length=8000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.batch + "guide"






    


















