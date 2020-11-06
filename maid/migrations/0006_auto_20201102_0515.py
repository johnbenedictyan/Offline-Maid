# Generated by Django 3.1.2 on 2020-11-02 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maid', '0005_auto_20201102_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maid',
            name='maid_type',
            field=models.CharField(choices=[('NEW', 'No Experience'), ('TRF', 'Transfer'), ('SGE', 'Singapore Experience'), ('OVE', 'Overseas Experience')], default='NEW', max_length=3, verbose_name='Maid Type'),
        ),
        migrations.AlterField(
            model_name='maid',
            name='reference_number',
            field=models.CharField(max_length=255, verbose_name='Reference Number'),
        ),
        migrations.AlterField(
            model_name='maid',
            name='remarks',
            field=models.CharField(max_length=255, verbose_name='Remarks'),
        ),
        migrations.AlterField(
            model_name='maid',
            name='repatraition_airport',
            field=models.CharField(max_length=100, verbose_name='Repatraition airport'),
        ),
        migrations.AlterField(
            model_name='maidbiodata',
            name='address_1',
            field=models.CharField(max_length=100, null=True, verbose_name='Address 1'),
        ),
        migrations.AlterField(
            model_name='maidbiodata',
            name='address_2',
            field=models.CharField(max_length=100, null=True, verbose_name='Address 2'),
        ),
        migrations.AlterField(
            model_name='maidbiodata',
            name='country_of_origin',
            field=models.CharField(choices=[('BGD', 'Bangladesh'), ('KHM', 'Cambodia'), ('IND', 'India'), ('IDN', 'Indonesia'), ('MMR', 'Myanmar'), ('PHL', 'Philippines (the)'), ('LKA', 'Sri Lanka'), ('OTH', 'Others')], max_length=3, null=True, verbose_name='Country of Origin'),
        ),
        migrations.AlterField(
            model_name='maidbiodata',
            name='place_of_birth',
            field=models.CharField(max_length=25, null=True, verbose_name='Place of birth'),
        ),
        migrations.AlterField(
            model_name='maidbiodata',
            name='religion',
            field=models.CharField(choices=[('B', 'Buddhist'), ('M', 'Muslim'), ('H', 'Hindu'), ('CH', 'Christain'), ('CA', 'Catholic'), ('S', 'Sikh'), ('OTH', 'Others'), ('NONE', 'None')], default='NONE', max_length=4, verbose_name='Religion'),
        ),
        migrations.AlterField(
            model_name='maidcooking',
            name='preference',
            field=models.IntegerField(choices=[(1, 'Least preferred'), (2, 'Less preferred'), (3, 'No preference'), (4, 'More preferred'), (5, 'Most preferred')], default=3, verbose_name='Cooking preference'),
        ),
        migrations.AlterField(
            model_name='maidcooking',
            name='remarks',
            field=models.CharField(choices=[('OC', "Able to cook own country's cuisine"), ('C', 'Able to cook chinese cuisine'), ('I', 'Able to cook indian cuisine'), ('W', 'Able to cook western cuisine'), ('OC_C', "Able to cook own country's and chinese cuisine"), ('OC_I', "Able to cook own country's and indian cuisine"), ('OC_W', "Able to cook own country's and western cuisine"), ('C_I', 'Able to cook chinese and indian cuisine'), ('C_W', 'Able to cook chinese and western cuisine'), ('I_W', 'Able to cook indian and western cuisine'), ('OC_C_I', "Able to cook own country's, chinese and indian cuisine"), ('OC_C_W', "Able to cook own country's, chinese and western cuisine"), ('OC_I_W', "Able to cook own country's, indian and western cuisine"), ('C_I_W', 'Able to cook chinese, indian and western cuisine'), ('OC_C_I_W', "Able to cook own country's, chinese, indian and western cuisine"), ('OTH', 'Other remarks (Please specify)')], max_length=8, null=True, verbose_name='Remarks for cooking'),
        ),
        migrations.AlterField(
            model_name='maiddietaryrestriction',
            name='restriction',
            field=models.CharField(choices=[('P', 'No pork'), ('C', 'No chicken'), ('B', 'No beef'), ('S', 'No seafood')], default='P', max_length=1, verbose_name='Dietary restriction'),
        ),
        migrations.AlterField(
            model_name='maiddisabledcare',
            name='preference',
            field=models.IntegerField(choices=[(1, 'Least preferred'), (2, 'Less preferred'), (3, 'No preference'), (4, 'More preferred'), (5, 'Most preferred')], default=3, verbose_name='Disabled care preference'),
        ),
        migrations.AlterField(
            model_name='maiddisabledcare',
            name='remarks',
            field=models.CharField(choices=[('OC', 'Experience in own country'), ('OV', 'Experience in overseas'), ('SG', 'Experience in Singapore'), ('OC_SG', 'Experience in own country and Singapore'), ('OC_O', 'Experience in own country and overseas'), ('OC_O_SG', 'Experience in own country, overseas and Singapore'), ('NE', 'No experience, but willing to learn'), ('NW', 'Not willing to care for disabled'), ('OTH', 'Other remarks (Please specify)')], max_length=7, null=True, verbose_name='Remarks for disabled care'),
        ),
        migrations.AlterField(
            model_name='maidelderlycare',
            name='preference',
            field=models.IntegerField(choices=[(1, 'Least preferred'), (2, 'Less preferred'), (3, 'No preference'), (4, 'More preferred'), (5, 'Most preferred')], default=3, verbose_name='Elderly care preference'),
        ),
        migrations.AlterField(
            model_name='maidelderlycare',
            name='remarks',
            field=models.CharField(choices=[('OC', 'Experience in own country'), ('OV', 'Experience in overseas'), ('SG', 'Experience in Singapore'), ('OC_SG', 'Experience in own country and Singapore'), ('OC_O', 'Experience in own country and overseas'), ('OC_O_SG', 'Experience in own country, overseas and Singapore'), ('NE', 'No experience, but willing to learn'), ('NW', 'Not willing to care for elderly'), ('OTH', 'Other remarks (Please specify)')], max_length=7, null=True, verbose_name='Remarks for elderly care'),
        ),
        migrations.AlterField(
            model_name='maidemploymenthistory',
            name='country',
            field=models.CharField(choices=[('SG', 'SINGAPORE')], max_length=3, verbose_name='Country of employment'),
        ),
        migrations.AlterField(
            model_name='maidfamilydetails',
            name='age_of_children',
            field=models.CharField(default='N.A', max_length=50, verbose_name='Age of children'),
        ),
        migrations.AlterField(
            model_name='maidfamilydetails',
            name='marital_status',
            field=models.CharField(choices=[('S', 'Single'), ('M', 'Married'), ('W', 'Widowed'), ('SP', 'Single Parent'), ('D', 'Divorced')], default='S', max_length=2, verbose_name='Marital Status'),
        ),
        migrations.AlterField(
            model_name='maidfoodhandlingpreference',
            name='preference',
            field=models.CharField(choices=[('P', 'No pork'), ('C', 'No chicken'), ('B', 'No beef'), ('S', 'No seafood')], default='P', max_length=1, verbose_name='Food preference'),
        ),
        migrations.AlterField(
            model_name='maidgeneralhousework',
            name='preference',
            field=models.IntegerField(choices=[(1, 'Least preferred'), (2, 'Less preferred'), (3, 'No preference'), (4, 'More preferred'), (5, 'Most preferred')], default=3, verbose_name='General housework preference'),
        ),
        migrations.AlterField(
            model_name='maidgeneralhousework',
            name='remarks',
            field=models.CharField(choices=[('CAN', 'Able to do all general housework'), ('OTH', 'Other remarks (Please specify)')], max_length=7, null=True, verbose_name='Remarks for general housework'),
        ),
        migrations.AlterField(
            model_name='maidinfantchildcare',
            name='preference',
            field=models.IntegerField(choices=[(1, 'Least preferred'), (2, 'Less preferred'), (3, 'No preference'), (4, 'More preferred'), (5, 'Most preferred')], default=3, verbose_name='Infant child care preference'),
        ),
        migrations.AlterField(
            model_name='maidinfantchildcare',
            name='remarks',
            field=models.CharField(choices=[('OC', 'Experience in own country'), ('OV', 'Experience in overseas'), ('SG', 'Experience in Singapore'), ('OC_SG', 'Experience in own country and Singapore'), ('OC_O', 'Experience in own country and overseas'), ('OC_O_SG', 'Experience in own country, overseas and Singapore'), ('NE', 'No experience, but willing to learn'), ('NW', 'Not willing to care for infants/children'), ('OTH', 'Other remarks (Please specify)')], max_length=7, null=True, verbose_name='Remarks for infant child care'),
        ),
        migrations.AlterField(
            model_name='maidworkduty',
            name='name',
            field=models.CharField(choices=[('H', 'Housework'), ('H_HDB', 'Housework (HDB)'), ('H_CON', 'Housework (Condo)'), ('H_PLP', 'Housework (Landed Property)'), ('CO', 'Cooking'), ('CO_C', 'Cooking (Chinese Food)'), ('CO_I', 'Cooking (Indian Food)'), ('CO_M', 'Cooking (Malay Food)'), ('CA_IC', 'Infant child care'), ('CA_E', 'Elderly care'), ('CA_D', 'Disabled care'), ('CA_P', 'Pet care')], max_length=5, verbose_name="Maid's work duties"),
        ),
    ]