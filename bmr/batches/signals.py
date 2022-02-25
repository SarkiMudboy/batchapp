from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (RawMaterialBillAuth, RawMaterialCheckRecord, ControlRecords, 
	 IndividualWeight, CleaningProcess)

@receiver(post_save, sender=RawMaterialBillAuth)
def update_auth(sender, instance, created, **kwargs):

	if getattr(instance, "_callSignal", None):
		form = getattr(instance, "_form", None)
		form.save_m2m()
		if instance.confirmed_by.exists():
			try:
				for bill in RawMaterialBillAuth.objects.filter(batch=instance.batch):
					if bill != instance:
						bill.confirmed_by.clear()
						bill.confirmed_by.add(*list(instance.confirmed_by.all()))
			except:
					pass
		else: 
			for bill in RawMaterialBillAuth.objects.filter(batch=instance.batch):
				if bill.confirmed_by.exists():
					instance.confirmed_by.add(*list(bill.confirmed_by.all()))
					break


@receiver(post_save, sender=RawMaterialCheckRecord)
def update_auth(sender, instance, created, **kwargs):

	if getattr(instance, "_callSignal", None):
		form = getattr(instance, "_form", None)
		form.save_m2m()
		if instance.check_done_by.exists():
			try:
				for check in RawMaterialCheckRecord.objects.filter(batch=instance.batch):
					if check != instance:
						check.check_done_by.clear()
						check.check_done_by.add(*list(instance.check_done_by.all()))
			except:
					pass
		else: 
			for check in RawMaterialCheckRecord.objects.filter(batch=instance.batch):
				if check.check_done_by.exists():
					instance.confirmed_by.add(*list(check.check_done_by.all()))
					break


@receiver(post_save, sender=ControlRecords)
def update_auth(sender, instance, created, **kwargs):

	if getattr(instance, "_callSignal", None):
		form = getattr(instance, "_form", None)
		form.save_m2m()
		if instance.approved_by.exists():
			try:
				for record in ControlRecords.objects.filter(batch=instance.batch):
					if record != instance:
						record.approved_by.clear()
						record.approved_by.add(*list(instance.approved_by.all()))
			except Exception as e:
				print(str(e))
		else:
			for record in ControlRecords.objects.filter(batch=instance.batch):
				if record.approved_by.exists():
					instance.approved_by.add(*list(record.approved_by.all()))
					break

		if instance.checked_by.exists():
			try:
				for record in ControlRecords.objects.filter(batch=instance.batch):
					if record != instance:
						record.checked_by.clear()
						record.checked_by.add(*list(instance.checked_by.all()))
			except:
					pass
		else: 
			for record in ControlRecords.objects.filter(batch=instance.batch):
				if record.checked_by.exists():
					instance.checked_by.add(*list(record.checked_by.all()))
					break

@receiver(post_save, sender=IndividualWeight)
def update_weight_auth(sender, instance, created, **kwargs):
	if getattr(instance, '_callSignal', None):
		form = getattr(instance, "_form", None)
		form.save_m2m()
		try:
			for record in ControlRecords.objects.filter(batch=instance.batch):
				if record.approved_by.exists():
					instance.approved_by.add(*list(record.approved_by.all()))
					break

			for record in ControlRecords.objects.filter(batch=instance.batch):
				if record.checked_by.exists():
					instance.checked_by.add(*list(record.checked_by.all()))
					break
		except Exception as e:
			print(str(e))


@receiver(post_save, sender=CleaningProcess)
def update_cleaning_auth(sender, instance, created, **kwargs):
	if getattr(instance, '_callSignal', None):
		form = getattr(instance, "_form", None)
		form.save_m2m()
		try:
			for record in ControlRecords.objects.filter(batch=instance.batch):
				if record.approved_by.exists():
					instance.approved_by.add(*list(record.approved_by.all()))
					break
					
			for record in ControlRecords.objects.filter(batch=instance.batch):
				if record.checked_by.exists():
					instance.checked_by.add(*list(record.checked_by.all()))
					break
		except Exception as e:
			print(str(e))
		
