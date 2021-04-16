# Imports from the system
import math
import random
import string
from datetime import date, datetime

# Imports from django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.crypto import get_random_string

# Imports from foreign installed apps
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

UserModel = get_user_model()

def r_string(length):
    r_str = ''.join(
        random.choice(string.ascii_lowercase) for i in range(length)
    )
    return r_str

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)

def r_contact_number():
    return random.randint(80000000, 99999999)

def create_test_user():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    email = f'{r_string(4)}@{r_string(4)}.com'
    password = f'{get_random_string(10, chars)}'
    return {
        'email': email,
        'password': password,
        'obj': get_user_model().objects.create_user(
            email=email,
            password=password
        )
    }

def encrypt_string(plaintext, encryption_key):
    # Data to be encrypted formatted as bytes literal
    bytes_literal = plaintext.encode('ascii')

    # Secret encryption key set in environment variables, does not change
    key = encryption_key.encode('ascii')

    # New nonce everytime
    nonce = get_random_bytes(32)
    
    # Create cipher object
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    # Generate encrypted ciphertext
    ciphertext, tag = cipher.encrypt_and_digest(bytes_literal)

    return ciphertext, nonce, tag

def decrypt_string(ciphertext, encryption_key, nonce, tag):
    cipher = AES.new(encryption_key.encode('ascii'), AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode('ascii')

def calculate_age(born):
    today = date.today()
    offset = ((today.month, today.day) < (born.month, born.day))
    return today.year - born.year - offset

def populate_necessary_rows():
    from maid.constants import MaidLanguageChoices, MaidResponsibilityChoices
    from maid.models import MaidLanguage, MaidResponsibility
    from .constants import AUTHORITY_GROUPS
    for language in MaidLanguageChoices.choices:
        MaidLanguage.objects.get_or_create(
            language=language[0]
        )

    for responsibility in MaidResponsibilityChoices.choices:
        MaidResponsibility.objects.get_or_create(
            name=responsibility[0]
        )

    for AG in AUTHORITY_GROUPS:
        Group.objects.get_or_create(
            name=AG
        )

def get_sg_region(post_code):
    from onlinemaid.sg_regions import SG_REGIONS

    if isinstance(post_code, str) and len(post_code)==6:
        for k,v in SG_REGIONS.items():
            if post_code[:2]==k:
                return v.get('region_code')
        return None
    else:
        return None

def humanise_time_duration(duration):
    if duration.days == 0 and duration.seconds >= 0 and duration.seconds < 60:
        return str(duration.seconds) +  "second" if seconds == 1 else str(duration.seconds) + " seconds"

    if duration.days == 0 and duration.seconds >= 60 and duration.seconds < 3600:
        minutes = math.floor(duration.seconds/60)
        return str(minutes) + " minute" if minutes == 1 else str(minutes) + " minutes"

    if duration.days == 0 and duration.seconds >= 3600 and duration.seconds < 86400:
        hours = math.floor(duration.seconds/3600)
        return str(hours) + " hour" if hours == 1 else str(hours) + " hours"

    if duration.days >= 1 and duration.days < 30:
        return str(duration.days) + " day" if duration.days == 1 else str(duration.days) + " days"

    if duration.days >= 30 and duration.days < 365:
        months = math.floor(duration.days/(365/12))
        return str(months) + " month" if months == 1 else str(months) + " months"

    if duration.days >= 365:
        years = math.floor(duration.days/365)
        months = math.floor(duration.days%365/(365/12))
        years_str = str(years) + " year" if years == 1 else str(years) + " years"
        months_str = str(months) + " month" if months == 1 else str(months) + " months"
        return years_str + " and " + months_str if months else years_str

def maid_seed_data():
    from agency.models import Agency

    from maid.constants import (
        TypeOfMaidChoices, MaidReligionChoices, MaidLanguageChoices,
        MaidCountryOfOrigin, MaritalStatusChoices, MaidAssessmentChoices,
        MaidCareRemarksChoices, MaidPassportStatusChoices,
        MaidGeneralHouseworkRemarksChoices
    )

    from maid.models import (
        Maid, MaidFinancialDetails, MaidLanguage, MaidPersonalDetails, 
        MaidFamilyDetails, MaidInfantChildCare, MaidElderlyCare, 
        MaidDisabledCare, MaidGeneralHousework, MaidCooking, 
        MaidLoanTransaction, MaidFinancialDetails, 
    )

    import json
    maid_data = json.load(open('./maid.json'))
    from django.core.files.uploadedfile import SimpleUploadedFile

    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    try:
        agency = Agency.objects.get(pk=1)
    except Agency.DoesNotExist:
        print('error')
    else:
        for maid in maid_data:
            try:
                selected_maid = Maid.objects.get(
                    reference_number = maid['reference_number'],
                )
            except Maid.DoesNotExist:
                encrption_thing = encrypt_string(
                    maid['passport_number'],
                    settings.ENCRYPTION_KEY
                )
                new_maid = Maid(
                    agency = agency,
                    reference_number = maid['reference_number'],
                    name = maid['name'],
                    passport_number = encrption_thing[0],
                    nonce = encrption_thing[1],
                    tag = encrption_thing[2],
                    maid_type = TypeOfMaidChoices.NEW,
                    days_off = maid['days_off'],
                    passport_status = MaidPassportStatusChoices.NOT_READY,
                    remarks = maid['remarks'],
                    published = True
                )
                new_maid.photo = 'maid.png'
                new_maid.save()
                selected_maid_personal_details = MaidPersonalDetails.objects.create(
                    maid=new_maid,
                    date_of_birth=datetime.strptime(
                        maid['date_of_birth'],
                        '%d %b %Y'
                    ),
                    country_of_origin=MaidCountryOfOrigin.INDONESIA,
                    height=maid['height'],
                    weight=maid['weight'],
                    place_of_birth=maid['place_of_birth'],
                    address_1=maid['address_1'],
                    address_2=maid['address_2'],
                    repatriation_airport=maid['repatriation_airport'],
                    religion=MaidReligionChoices.NONE,
                    preferred_language=MaidLanguage.objects.get(
                        language=MaidLanguageChoices.ENGLISH
                    )
                )
                selected_maid_personal_details.languages.add(
                    MaidLanguage.objects.get(
                        language=MaidLanguageChoices.ENGLISH
                    )
                )
                MaidFamilyDetails.objects.create(
                    maid=new_maid,
                    marital_status=MaritalStatusChoices.SINGLE,
                    number_of_children=0,
                    age_of_children='N.A.',
                    number_of_siblings=0
                )
                MaidFinancialDetails.objects.create(
                    maid=new_maid,
                    salary=maid['salary'],
                    personal_loan_amount=0
                )
                MaidInfantChildCare.objects.create(
                    maid=new_maid,
                    assessment=random.randint(1,5),
                    willingness=True,
                    experience=True,
                    remarks=MaidCareRemarksChoices.OWN_COUNTRY,
                    other_remarks=''
                )
                MaidElderlyCare.objects.create(
                    maid=new_maid,
                    assessment=random.randint(1,5),
                    willingness=True,
                    experience=True,
                    remarks=MaidCareRemarksChoices.OWN_COUNTRY,
                    other_remarks=''
                )
                MaidDisabledCare.objects.create(
                    maid=new_maid,
                    assessment=random.randint(1,5),
                    willingness=True,
                    experience=True,
                    remarks=MaidCareRemarksChoices.OWN_COUNTRY,
                    other_remarks=''
                )
                MaidGeneralHousework.objects.create(
                    maid=new_maid,
                    assessment=random.randint(1,5),
                    willingness=True,
                    experience=True,
                    remarks=MaidGeneralHouseworkRemarksChoices.CAN_DO_ALL_HOUSEWORK,
                    other_remarks=''
                )
                MaidCooking.objects.create(
                    maid=new_maid,
                    assessment=random.randint(1,5),
                    willingness=True,
                    experience=True,
                    remarks=MaidCareRemarksChoices.OWN_COUNTRY,
                    other_remarks=''
                )
                MaidLoanTransaction.objects.create(
                    maid=new_maid,
                    amount=100,
                    transaction_type='ADD',
                    description='this is a description',
                    transaction_date=date.today()
                )

def subscription_seed_data():
    from payment.models import SubscriptionProduct, SubscriptionProductPrice
    
    import json
    subscription_data = json.load(open('./subscriptions.json'))
    
    for subscription in subscription_data:
        sub_product, created = SubscriptionProduct.objects.get_or_create(
            id=subscription['subscription_product_id'],
            name=subscription['subscription_product_name'],
            description=subscription['subscription_product_description']
        )
        
        if created == True:
            for subscription_price in subscription['prices']:
                sub_product_price, created = SubscriptionProductPrice.objects.get_or_create(
                    id=subscription_price['subcription_price_id'],
                    subscription_product=sub_product,
                    interval=subscription_price['subcription_price_interval'],
                    interval_count=subscription_price['subcription_price_interval_count'],
                    unit_amount=subscription_price['subcription_price_unit_amount']
                )