# Generated by Django 3.1.4 on 2020-12-23 02:20

from django.db import migrations, models
import onlinemaid.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='logo',
            field=models.FileField(null=True, storage=onlinemaid.storage_backends.PublicMediaStorage(), upload_to='', verbose_name='Website Logo'),
        ),
        migrations.AddField(
            model_name='agency',
            name='qr_code',
            field=models.FileField(null=True, storage=onlinemaid.storage_backends.PublicMediaStorage(), upload_to='', verbose_name='Website QR Code'),
        ),
    ]
