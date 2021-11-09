from django.db.models.signals import pre_save
from django.dispatch import receiver
from products.models import ManufacturingProcess

@receiver(pre_save, sender=ManufacturingProcess)
def add_serial(sender, instance, *args, **kwargs):
    duration = ''
    time = instance.duration
    splitted_time = time.split(':')
    hours = ''
    minutes = ''
    seconds = ''
    if splitted_time[0] != '00' and splitted_time[0][0] != '0':
        hours = splitted_time[0] + ' hours '
    elif splitted_time[0] != '00' and splitted_time[0][0] == '0':
        hours = splitted_time[0][1] + ' hours '
    if splitted_time[1] != '00' and splitted_time[1][0] != '0':
        minutes = splitted_time[1] + ' minutes '
    elif splitted_time[1] != '00' and splitted_time[1][0] == '0':
        minutes = splitted_time[1][1] + ' minutes '
    if splitted_time[2] != '00' and splitted_time[2][0] != '0':
        seconds = splitted_time[2] + ' seconds '
    elif splitted_time[2] != '00' and splitted_time[2][0] == '0':
        seconds = splitted_time[2][1] + ' seconds '

    real_time = hours + minutes + seconds

    duration += real_time

    instance.action_duration = duration
