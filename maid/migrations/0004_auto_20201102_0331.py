# Generated by Django 3.1.2 on 2020-11-02 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maid', '0003_maidemploymenthistory_maidworkduties'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MaidWorkDuties',
            new_name='MaidWorkDuty',
        ),
    ]