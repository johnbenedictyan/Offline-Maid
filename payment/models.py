# Imports from python

# Imports from django
from django.db import models
from django.db.models.enums import IntegerChoices
from django.utils.translation import ugettext_lazy as _

# Imports from project
from onlinemaid.storage_backends import PublicMediaStorage

# Imports from other apps
from agency.models import Agency

# Imports from within the app

# Utiliy Classes and Functions

# Start of Models

class Invoice(models.Model):
    agency = models.ForeignKey(
        Agency,
        on_delete=models.SET_NULL,
        related_name='invoices',
        null=True
    )
    
    created_on = models.DateTimeField(
        auto_now_add=True
    )

class Customer(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255
    )
    
    agency = models.OneToOneField(
        Agency,
        on_delete=models.CASCADE,
        related_name='customer_account'
    )
    
class SubscriptionProduct(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255
    )
    
    name = models.CharField(
        verbose_name=_('Subscription Product\'s Name'),
        max_length=255
    )
    
    description = models.TextField(
        verbose_name=_('Subscription Product\'s Description')
    )
    
    active = models.BooleanField(
        verbose_name=_('Subscription Product\'s Active State'),
        default=True
    )

    archived = models.BooleanField(
        verbose_name=_('Subscription Product\'s Archived State'),
        default=False
    )
    
class SubscriptionProductImage(models.Model):
    subscription_product = models.ForeignKey(
        SubscriptionProduct,
        on_delete=models.CASCADE,
        related_name='images'
    )
    
    photo = models.FileField(
        verbose_name=_('Subscription Product\'s Photo'),
        blank=False,
        null=True,
        storage=PublicMediaStorage()
    )
    
class SubscriptionProductPrice(models.Model):
    class Currencies(models.TextChoices):
        SGD = 'sgd', _('Singapore Dollars')
    
    class Intervals(models.TextChoices):
        DAY = 'day', _('Per Day')
        WEEK = 'week', _('Per Week')
        MONTH = 'month', _('Per Month')
        YEAR = 'year', _('Per Year')
        
    class IntervalCounts(models.IntegerChoices):
        ONE = 1
        THREE = 3
        SIX = 6
        TWELVE = 12
        
    id = models.CharField(
        primary_key=True,
        max_length=255
    )
        
    subscription_product = models.ForeignKey(
        SubscriptionProduct,
        on_delete=models.CASCADE,
        related_name='prices'
    )
    
    active = models.BooleanField(
        verbose_name=_('Subscription Product\'s Active State'),
        default=True
    )
    
    currency = models.CharField(
        max_length=3,
        choices=Currencies.choices,
        default=Currencies.SGD
    )
    
    interval = models.CharField(
        max_length=5,
        choices=Intervals.choices,
        default=Intervals.DAY
    )
    
    interval_count = models.IntegerField(
        choices=IntervalCounts.choices,
        default=IntervalCounts.ONE
    )
    
    unit_amount = models.PositiveIntegerField(
        verbose_name=_('Unit amount in cents')
    )