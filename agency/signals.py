# Imports from python

# Imports from django
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Imports from other apps
import stripe
from advertisement.models import Advertisement
from maid.models import Maid
from payment.models import Customer

# Imports from within the app
from .models import Agency, PotentialAgency, AgencyEmployee



# Start of Signals
@receiver(post_save, sender=Agency)
def agency_created(sender, instance, created, **kwargs):
    if created == True:
        try:
            pa = PotentialAgency.objects.get(
                license_number = instance.license_number
            )
        except PotentialAgency.DoesNotExist as e:
            print(e)
        else:
            pa.delete()

@receiver(post_save, sender=Agency)
def stripe_customer_created_or_update(sender, instance, created, **kwargs):
    agency = instance
    if created == True:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            stripe_customer = stripe.Customer.create(
                address = {
                    'city': None,
                    'country': None,
                    'line1': None,
                    'line2': None,
                    'postal_code': None,
                    'state': None,
                },
                description = f'Customer account for {agency.name}',
                email=None,
                name=agency.name,
                invoice_settings={
                    'custom_fields': None,
                    'default_payment_method': None,
                    'footer': ''
                }
            )
        except Exception as e:
            print(e)
        else:
            new_customer = Customer(
                agency = agency
            )
            new_customer.id = stripe_customer.id
            new_customer.save()
    else:
        pass
    
@receiver(post_save, sender=AgencyEmployee)
def agency_employee_counter(sender, instance, created, **kwargs):
    agency = instance.agency
    agency.amount_of_employees = AgencyEmployee.objects.filter(
        agency=agency
    ).count()
    agency.save()
    
@receiver(post_save, sender=Agency)
def deactivate_agency(sender, instance, created, **kwargs):
    agency = instance
    if agency.active == False:
        Maid.objects.filter(
            agency=agency
        ).update(
            frozen=True
        )
        Advertisement.objects.filter(
            agency=agency
        ).update(
            frozen=True
        )
        
@receiver(pre_save, sender=Agency)
def reactivate_agency(sender, instance, **kwargs):
    if instance.id:
        current = instance
        prev = agency = Agency.objects.get(
            pk=instance.pk
        )
        if prev.active == False and current.active == True:
            Maid.objects.filter(
                agency=agency
            ).update(
                frozen=False
            )
            Advertisement.objects.filter(
                agency=agency
            ).update(
                frozen=False
            )