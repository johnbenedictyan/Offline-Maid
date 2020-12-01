# Generated by Django 3.1.3 on 2020-12-01 10:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agency', '0005_auto_20201121_1321'),
        ('maid', '0005_remove_maid_status_complete'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployerBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer_name', models.CharField(max_length=40)),
                ('employer_email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('employer_mobile_number', models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='Please enter a valid contact number', regex='^[0-9]*$')], verbose_name='Mobile Number')),
                ('agency_employee', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='agency.agencyemployee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployerDocBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_ref_no', models.CharField(max_length=20, unique=True)),
                ('spouse_required', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('sponsor_required', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='employer_documentation.employerbase')),
                ('fdw', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='maid.maid')),
            ],
        ),
        migrations.CreateModel(
            name='EmployerDocServiceFeeBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b1_service_fee', models.PositiveIntegerField()),
                ('b2a_work_permit_application_collection', models.PositiveIntegerField()),
                ('b2b_medical_examination_fee', models.PositiveIntegerField()),
                ('b2c_security_bond_accident_insurance', models.PositiveIntegerField()),
                ('b2d_indemnity_policy_reimbursement', models.PositiveIntegerField()),
                ('b2e_home_service', models.PositiveIntegerField()),
                ('b2f_counselling', models.PositiveIntegerField()),
                ('b2g_sip', models.PositiveIntegerField()),
                ('b2h_replacement_months', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24')])),
                ('b2h_replacement_cost', models.PositiveIntegerField()),
                ('b2i_work_permit_renewal', models.PositiveIntegerField()),
                ('b2j1_other_services_description', models.CharField(blank=True, max_length=40, null=True)),
                ('b2j1_other_services_fee', models.PositiveIntegerField(blank=True, null=True)),
                ('b2j2_other_services_description', models.CharField(blank=True, max_length=40, null=True)),
                ('b2j2_other_services_fee', models.PositiveIntegerField(blank=True, null=True)),
                ('b2j3_other_services_description', models.CharField(blank=True, max_length=40, null=True)),
                ('b2j3_other_services_fee', models.PositiveIntegerField(blank=True, null=True)),
                ('ca_deposit', models.PositiveIntegerField()),
                ('employer_doc_base', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employer_documentation.employerdocbase')),
            ],
        ),
        migrations.CreateModel(
            name='EmployerExtraInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer_nric', models.CharField(max_length=20)),
                ('employer_address_1', models.CharField(max_length=100, null=True, verbose_name='Street Address')),
                ('employer_address_2', models.CharField(max_length=50, null=True, verbose_name='Unit Number')),
                ('employer_postal_code', models.CharField(max_length=25, null=True, verbose_name='Postal Code')),
                ('employer_base', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employer_documentation.employerbase')),
            ],
        ),
        migrations.CreateModel(
            name='EmployerDocSig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreement_date', models.DateField(blank=True, null=True)),
                ('employer_doc_base', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employer_documentation.employerdocbase')),
            ],
        ),
        migrations.CreateModel(
            name='EmployerDocServiceFeeReplacement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b4_loan_transferred', models.PositiveIntegerField()),
                ('fdw_replaced', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='maid.maid')),
                ('service_fee_schedule', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employer_documentation.employerdocservicefeebase')),
            ],
        ),
        migrations.CreateModel(
            name='EmployerDocServiceAgreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c1_3_handover_days', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30')])),
                ('c3_2_no_replacement_criteria_1', models.CharField(max_length=100)),
                ('c3_2_no_replacement_criteria_2', models.CharField(max_length=100)),
                ('c3_2_no_replacement_criteria_3', models.CharField(max_length=100)),
                ('c3_4_no_replacement_refund', models.PositiveIntegerField()),
                ('c4_1_number_of_replacements', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('c4_1_replacement_period', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24')])),
                ('c4_1_5_replacement_deadline', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24')])),
                ('c5_1_1_deployment_deadline', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30')])),
                ('c5_1_1_failed_deployment_refund', models.PositiveIntegerField()),
                ('c5_1_2_before_fdw_arrives_charge', models.PositiveIntegerField()),
                ('c5_1_2_after_fdw_arrives_charge', models.PositiveIntegerField()),
                ('c5_2_2_can_transfer_refund_within', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4')])),
                ('c5_3_2_cannot_transfer_refund_within', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4')])),
                ('c6_4_per_day_food_accommodation_cost', models.PositiveSmallIntegerField()),
                ('c6_6_per_session_counselling_cost', models.PositiveIntegerField()),
                ('c9_1_independent_mediator_1', models.CharField(max_length=40)),
                ('c9_2_independent_mediator_2', models.CharField(max_length=40)),
                ('c13_termination_notice', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30')])),
                ('employer_doc_base', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employer_documentation.employerdocbase')),
            ],
        ),
        migrations.CreateModel(
            name='EmployerDocMaidStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipa_approval_date', models.DateField(blank=True, null=True)),
                ('security_bond_approval_date', models.DateField(blank=True, null=True)),
                ('arrival_date', models.DateField(blank=True, null=True)),
                ('thumb_print_date', models.DateField(blank=True, null=True)),
                ('sip_date', models.DateField(blank=True, null=True)),
                ('employer_doc_base', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employer_documentation.employerdocbase')),
            ],
        ),
        migrations.CreateModel(
            name='EmployerDocJobOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer_race', models.CharField(choices=[('Chinese', 'Chinese'), ('Malay', 'Malay'), ('Indian', 'Indian'), ('Others', 'Others')], max_length=16)),
                ('type_of_property', models.CharField(choices=[('HDB 2 Room flat', 'HDB 2 Room flat'), ('HDB 3 Room flat', 'HDB 3 Room flat'), ('HDB 4 Room flat', 'HDB 4 Room flat'), ('HDB 5 Room flat', 'HDB 5 Room flat'), ('HDB Executive flat', 'HDB Executive flat'), ('HDB Maisonette flat', 'HDB Maisonette flat'), ('Condominium', 'Condominium'), ('Penthouse', 'Penthouse'), ('Terrace', 'Terrace'), ('Semi-Detached', 'Semi-Detached'), ('Bungalow', 'Bungalow'), ('Shophouse', 'Shophouse')], max_length=40)),
                ('no_of_bedrooms', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('no_of_toilets', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('no_of_family_members', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15')])),
                ('no_of_children_between_6_12', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('no_of_children_below_5', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('no_of_infants', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('fetch_children', models.TextField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('look_after_elderly', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('look_after_bed_ridden_patient', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('cooking', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('clothes_washing', models.CharField(choices=[('Hand', 'Hand'), ('Machine', 'Machine'), ('Both', 'Both')], max_length=10)),
                ('car_washing', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('take_care_of_pets', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('gardening', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('remarks', models.TextField(blank=True, max_length=300, null=True)),
                ('employer_doc_base', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employer_documentation.employerdocbase')),
            ],
        ),
        migrations.CreateModel(
            name='EmployerDocEmploymentContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c3_2_salary_payment_date', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28')])),
                ('c3_5_fdw_sleeping_arrangement', models.CharField(choices=[('Have own room', 'Have own room'), ('Sharing room with someone', 'Sharing room with someone'), ('Sleeping in common area', 'Sleeping in common area')], max_length=40)),
                ('c4_1_termination_notice', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30')])),
                ('employer_doc_base', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employer_documentation.employerdocbase')),
            ],
        ),
    ]
