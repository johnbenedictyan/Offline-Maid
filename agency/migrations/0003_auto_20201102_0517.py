# Generated by Django 3.1.2 on 2020-11-02 05:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0002_auto_20201102_0444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='license_number',
            field=models.CharField(max_length=100, verbose_name='License number'),
        ),
        migrations.AlterField(
            model_name='agency',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='agency',
            name='uen',
            field=models.CharField(max_length=10, verbose_name="Company's UEN code"),
        ),
        migrations.AlterField(
            model_name='agency',
            name='website_uri',
            field=models.CharField(max_length=100, validators=[django.core.validators.URLValidator(message='Please enter a valid URL')], verbose_name='Website URL'),
        ),
        migrations.AlterField(
            model_name='agencycontactinformation',
            name='mobile_number',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='Please enter a valid contact number', regex='^[0-9]*$')], verbose_name='Mobile Number'),
        ),
        migrations.AlterField(
            model_name='agencycontactinformation',
            name='office_number',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='Please enter a valid contact number', regex='^[0-9]*$')], verbose_name='Office Number'),
        ),
        migrations.AlterField(
            model_name='agencyemployee',
            name='contact_number',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Please enter a valid contact number', regex='^[0-9]*$')], verbose_name='Contact Number'),
        ),
        migrations.AlterField(
            model_name='agencyemployee',
            name='ea_personnel_number',
            field=models.CharField(max_length=50, verbose_name='EA personnel number'),
        ),
        migrations.AlterField(
            model_name='agencyemployee',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='agencyemployee',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='agencylocation',
            name='address_1',
            field=models.CharField(max_length=100, null=True, verbose_name='Street Address'),
        ),
        migrations.AlterField(
            model_name='agencylocation',
            name='address_2',
            field=models.CharField(max_length=50, null=True, verbose_name='Unit Number'),
        ),
        migrations.AlterField(
            model_name='agencylocation',
            name='area',
            field=models.CharField(choices=[('C', 'Central'), ('N', 'North'), ('NE', 'North East'), ('E', 'East'), ('W', 'West')], default='C', max_length=2, verbose_name='Area'),
        ),
        migrations.AlterField(
            model_name='agencylocation',
            name='postal_code',
            field=models.CharField(max_length=25, null=True, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='agencyoperatinghours',
            name='friday',
            field=models.CharField(blank=True, max_length=30, verbose_name="Friday's opening hours"),
        ),
        migrations.AlterField(
            model_name='agencyoperatinghours',
            name='monday',
            field=models.CharField(blank=True, max_length=30, verbose_name="Monday's opening hours"),
        ),
        migrations.AlterField(
            model_name='agencyoperatinghours',
            name='operating_type',
            field=models.CharField(choices=[('OH', 'Opening Hours'), ('AO', 'Appointment Only')], default='OH', max_length=2, verbose_name="Agency's operating hours type"),
        ),
        migrations.AlterField(
            model_name='agencyoperatinghours',
            name='public_holiday',
            field=models.CharField(blank=True, max_length=30, verbose_name='Public holiday opening hours'),
        ),
        migrations.AlterField(
            model_name='agencyoperatinghours',
            name='saturday',
            field=models.CharField(blank=True, max_length=30, verbose_name="Saturday's opening hours"),
        ),
        migrations.AlterField(
            model_name='agencyoperatinghours',
            name='sunday',
            field=models.CharField(blank=True, max_length=30, verbose_name="Sunday's opening hours"),
        ),
        migrations.AlterField(
            model_name='agencyoperatinghours',
            name='thursday',
            field=models.CharField(blank=True, max_length=30, verbose_name="Thursday's opening hours"),
        ),
        migrations.AlterField(
            model_name='agencyoperatinghours',
            name='tuesday',
            field=models.CharField(blank=True, max_length=30, verbose_name="Tuesday's opening hours"),
        ),
        migrations.AlterField(
            model_name='agencyoperatinghours',
            name='wednesday',
            field=models.CharField(blank=True, max_length=30, verbose_name="Wednesday's opening hours"),
        ),
        migrations.AlterField(
            model_name='agencyplan',
            name='choice',
            field=models.CharField(choices=[('B100', '100 Biodata'), ('B200', '200 Biodata'), ('B300', '300 Biodata')], default='B100', max_length=4, verbose_name='Plan type'),
        ),
        migrations.AlterField(
            model_name='agencyplan',
            name='remarks',
            field=models.CharField(blank=True, max_length=100, verbose_name='Remarks'),
        ),
    ]