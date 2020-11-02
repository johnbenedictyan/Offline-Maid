# Generated by Django 3.1.2 on 2020-11-02 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maid', '0002_maid_published'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaidWorkDuties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(choices=[('H', 'Housework'), ('H_HDB', 'Housework (HDB)'), ('H_CON', 'Housework (Condo)'), ('H_PLP', 'Housework (Landed Property)'), ('CO', 'Cooking'), ('CO_C', 'Cooking (Chinese Food)'), ('CO_I', 'Cooking (Indian Food)'), ('CO_M', 'Cooking (Malay Food)'), ('CA_IC', 'Infant child care'), ('CA_E', 'Elderly care'), ('CA_D', 'Disabled care'), ('CA_P', 'Pet care')], max_length=5, verbose_name="Maid's work duties")),
            ],
        ),
        migrations.CreateModel(
            name='MaidEmploymentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name="Maid employment's start date")),
                ('end_date', models.DateTimeField(verbose_name="Maid employment's end date")),
                ('country', models.TextField(choices=[('SG', 'SINGAPORE')], max_length=3, verbose_name='Country of employment')),
                ('work_duration', models.DurationField(blank=True, editable=False, verbose_name='Employment duration')),
                ('maid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employment_history', to='maid.maid')),
                ('work_duties', models.ManyToManyField(to='maid.MaidWorkDuties')),
            ],
        ),
    ]
