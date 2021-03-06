from typing import Any, Dict

from agency.models import Agency, AgencyEmployee
from crispy_forms.bootstrap import PrependedText, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, Button, Column, Field, Hidden, Layout,
                                 Row, Submit)
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput
from django.utils.translation import ugettext_lazy as _
from maid.models import Maid
from onlinemaid import constants as om_constants
from onlinemaid.helper_functions import (encrypt_string, is_married,
                                         is_not_null, is_null)
from onlinemaid.validators import (validate_age, validate_ea_personnel_number,
                                   validate_fin, validate_nric,
                                   validate_passport, validate_passport_date)

from .constants import (EmployerTypeOfApplicantChoices,
                        ResidentialStatusFullChoices)
from .helper_functions import (is_foreigner, is_local,
                               nationality_residential_status_match)
from .models import (CaseSignature, CaseStatus, DocSafetyAgreement,
                     DocServAgmtEmpCtr, DocServiceFeeSchedule, DocUpload,
                     Employer, EmployerDoc, EmployerHousehold, EmployerIncome,
                     EmployerJointApplicant, EmployerSponsor, MaidInventory)


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        exclude = [
            'employer_nric_nonce',
            'employer_nric_tag',
            'employer_fin_nonce',
            'employer_fin_tag',
            'employer_passport_nonce',
            'employer_passport_tag',
            'spouse_nric_nonce',
            'spouse_nric_tag',
            'spouse_fin_nonce',
            'spouse_fin_tag',
            'spouse_passport_nonce',
            'spouse_passport_tag',
            'potential_employer'
        ]

    def __init__(self, *args, **kwargs):
        self.user_pk = kwargs.pop('user_pk')
        self.user_obj = get_user_model().objects.get(pk=self.user_pk)
        self.authority = kwargs.pop('authority')
        self.form_type = kwargs.pop('form_type')
        super().__init__(*args, **kwargs)

        # Decryption
        instance = self.instance
        self.initial.update({
            'employer_nric_num': instance.get_employer_nric_full(),
            'employer_fin_num': instance.get_employer_fin_full(),
            'employer_passport_num': instance.get_employer_passport_full(),
            'spouse_nric_num': instance.get_employer_spouse_nric_full(),
            'spouse_fin_num': instance.get_employer_spouse_fin_full(),
            'spouse_passport_num': instance.get_employer_spouse_passport_full()
        })

        # CrispyForm Helper
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'applicant_type',
                    css_class='form-group col-lg-12 pr-md-3'
                ),
                Column(
                    'household_details_required',
                    css_class='form-group col-lg-12 pl-md-3',
                )
            ),
            Row(
                Column(
                    # Note: Current position in layout helper object is
                    # self.helper.layout.fields[1][1].
                    # If position is changed,
                    # MUST update 'del self.helper.layout.fields[1][1]' line
                    # as this removes this object from the layout helper.
                    'agency_employee',
                    css_class='form-group col-lg-12 pr-lg-3'
                )
            ),

            # Employer Details
            Row(
                Column(
                    HTML(
                        """
                        <h5 class="fs-14">Employer Information</h5>
                    """),
                    css_class='mb-3 mb-lg-4'
                )
            ),
            Row(
                Column(
                    'employer_name',
                    css_class='form-group col-lg-12 pr-md-3'
                ),
                Column(
                    'employer_gender',
                    css_class='form-group col-lg-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    PrependedText(
                        'employer_mobile_number', '+65',
                    ),
                    css_class='form-group col-xl-12 pr-md-3',
                ),
                Column(
                    PrependedText(
                        'employer_home_number', '+65',
                    ),
                    css_class='form-group col-xl-12 pl-md-3',
                )
            ),
            Row(
                Column(
                    'employer_email',
                    css_class='form-group col-lg-12 pr-md-3'
                ),
                Column(
                    'employer_address_1',
                    css_class='form-group col-lg-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    'employer_address_2',
                    css_class='form-group col-lg-12 pr-md-3'
                ),
                Column(
                    'employer_post_code',
                    css_class='form-group col-lg-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    Field(
                        'employer_date_of_birth',
                        type='text',
                        onfocus="(this.type='date')",
                        placeholder='Employer date of birth',
                    ),
                    css_class='form-group col-lg-12 pr-md-3'
                ),
                Column(
                    'employer_nationality',
                    css_class='form-group col-lg-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    'employer_residential_status',
                    css_class='form-group col-lg-12 pr-md-3'
                ),
                Column(
                    'employer_nric_num',
                    css_class='form-group col-lg-12 pl-md-3',
                    id='employer_id_nric',
                )
            ),
            Row(
                Column(
                    'employer_fin_num',
                    css_class='form-group col-lg-12 pr-md-3'
                ),
                Column(
                    'employer_passport_num',
                    css_class='form-group col-lg-12 pl-md-3'
                ),
                id='employer_id_other'
            ),
            Row(
                Column(
                    Field(
                        'employer_passport_date',
                        type='text',
                        onfocus="(this.type='date')",
                        placeholder='Employer passport expiry date',
                    ),
                    css_class='form-group col-lg-12 pr-md-3',
                    id='employer_id_other_2',
                ),
                Column(
                    'employer_marital_status',
                    css_class='form-group col-lg-12 pr-md-3'
                )
            ),

            # Spouse's Information
            Row(
                Column(
                    HTML(
                        """
                        <h5 class="fs-14">Spouse Information</h5>
                    """),
                    Row(
                        Column(
                            'spouse_name',
                            css_class='form-group col-lg-12 employer-spouse spouse-only pr-md-3',
                        ),
                        Column(
                            'spouse_gender',
                            css_class='form-group col-lg-12 employer-spouse spouse-only pl-md-3',
                        )
                    ),
                    Row(
                        Column(
                            Field(
                                'spouse_date_of_birth',
                                type='text',
                                onfocus="(this.type='date')",
                                placeholder='Employer spouse date of birth',
                            ),
                            css_class='form-group col-lg-12 pr-md-3'
                        ),
                        Column(
                            'spouse_nationality',
                            css_class='form-group col-lg-12 pl-md-3'
                        )
                    ),
                    Row(
                        Column(
                            'spouse_residential_status',
                            css_class='form-group col-lg-12 pr-md-3'
                        ),
                        Column(
                            'spouse_nric_num',
                            css_class='form-group col-lg-12 pl-md-3',
                            id='spouse_id_nric',
                        )
                    ),
                    Row(
                        Column(
                            'spouse_fin_num',
                            css_class='form-group col-lg-12 pr-md-3'
                        ),
                        Column(
                            'spouse_passport_num',
                            css_class='form-group col-lg-12 pl-md-3'
                        ),
                        id='spouse_id_other',
                    ),
                    Row(
                        Column(
                            Field(
                                'spouse_passport_date',
                                type='text',
                                onfocus="(this.type='date')",
                                placeholder='Employer spouse passport expiry date',
                            ),
                            css_class='form-group col-lg-12 pr-md-3',
                            id='spouse_id_other_2',
                        ),
                        Column(
                            'employer_marriage_sg_registered',
                            css_class='form-group col-lg-12 pl-md-3'
                        )
                    ),
                ),
                id='spouse-section',
            ),

            # Submit
            Row(
                Column(
                    Submit(
                        'submit',
                        'Next',
                        css_class="btn btn-xs-lg btn-primary w-50"
                    ),
                    css_class='form-group col-24 text-center'
                )
            )
        )

        if self.authority == om_constants.AG_OWNERS:
            qs = AgencyEmployee.objects.filter(
                agency=self.user_obj.agency_owner.agency,
            )
            q_pks = [obj.pk for obj in qs if obj.is_ea_personnel_no_valid()]
            self.fields['agency_employee'].queryset = qs.filter(pk__in=q_pks)
        elif self.authority == om_constants.AG_ADMINS:
            qs = AgencyEmployee.objects.filter(
                agency=self.user_obj.agency_employee.agency,
            )
            q_pks = [obj.pk for obj in qs if obj.is_ea_personnel_no_valid()]
            self.fields['agency_employee'].queryset = qs.filter(pk__in=q_pks)
        elif self.authority == om_constants.AG_MANAGERS:
            qs = AgencyEmployee.objects.filter(
                agency=self.user_obj.agency_employee.agency,
                branch=self.user_obj.agency_employee.branch,
            )
            q_pks = [obj.pk for obj in qs if obj.is_ea_personnel_no_valid()]
            self.fields['agency_employee'].queryset = qs.filter(pk__in=q_pks)
        else:
            # Remember to make this match the position of the
            # 'agency_employee' field in the layout
            # helper object above
            del self.helper.layout.fields[2][0][0]
            del self.fields['agency_employee']

    def check_queryset(self, queryset, error_msg):
        for employer_obj in queryset:
            if not employer_obj == self.instance:
                # Check if it belongs to current user's agency
                if self.authority == om_constants.AG_OWNERS:
                    if (
                        employer_obj.agency_employee.agency
                        == self.user_obj.agency_owner.agency
                    ):
                        raise ValidationError(error_msg)
                elif (
                    employer_obj.agency_employee.agency
                    == self.user_obj.agency_employee.agency
                ):
                    raise ValidationError(error_msg)

    def clean_agency_employee(self):
        cleaned_field = self.cleaned_data.get('agency_employee')
        validate_ea_personnel_number(cleaned_field.ea_personnel_number)
        return cleaned_field

    def clean_employer_email(self):
        cleaned_field = self.cleaned_data.get('employer_email')

        try:
            # Check if employer_email exists in database
            employer_queryset = Employer.objects.filter(
                employer_email=cleaned_field
            )
        except Employer.DoesNotExist:
            # If no entries for employer_email, then no further checks
            pass
        else:
            self.check_queryset(
                employer_queryset,
                'An employer with this email address already exists in your \
                    agency'
            )
        finally:
            return cleaned_field

    def clean_employer_mobile_number(self):
        cleaned_field = self.cleaned_data.get('employer_mobile_number')

        try:
            # Check if employer_mobile_number exists in database
            employer_queryset = Employer.objects.filter(
                employer_mobile_number=cleaned_field
            )
        except Employer.DoesNotExist:
            # If no entries for employer_mobile_number, then no further checks
            pass
        else:
            self.check_queryset(
                employer_queryset,
                'An employer with this mobile number already exists in your \
                    agency'
            )
        finally:
            return cleaned_field

    def clean_employer_nric_num(self):
        cleaned_field = self.cleaned_data.get('employer_nric_num')
        employer_residential_status = self.cleaned_data.get(
            'employer_residential_status'
        )
        if is_not_null(cleaned_field):
            if is_local(employer_residential_status):
                validate_nric("Employer", cleaned_field)
                ciphertext, nonce, tag = encrypt_string(
                    cleaned_field,
                    settings.ENCRYPTION_KEY
                )
                self.instance.employer_nric_nonce = nonce
                self.instance.employer_nric_tag = tag
                return ciphertext
            else:
                return None
        else:
            return None

    def clean_employer_fin_num(self):
        cleaned_field = self.cleaned_data.get('employer_fin_num')
        employer_residential_status = self.cleaned_data.get(
            'employer_residential_status'
        )
        if is_foreigner(employer_residential_status):
            validate_fin('Employer', cleaned_field)
            ciphertext, nonce, tag = encrypt_string(
                cleaned_field,
                settings.ENCRYPTION_KEY
            )
            self.instance.employer_fin_nonce = nonce
            self.instance.employer_fin_tag = tag
            return ciphertext
        else:
            return None

    def clean_employer_passport_num(self):
        cleaned_field = self.cleaned_data.get('employer_passport_num')
        employer_residential_status = self.cleaned_data.get(
            'employer_residential_status'
        )
        if is_foreigner(employer_residential_status):
            validate_passport('Employer', cleaned_field)
            ciphertext, nonce, tag = encrypt_string(
                cleaned_field,
                settings.ENCRYPTION_KEY
            )
            self.instance.employer_passport_nonce = nonce
            self.instance.employer_passport_tag = tag
            return ciphertext
        else:
            return None

    def clean_employer_passport_date(self):
        cleaned_field = self.cleaned_data.get('employer_passport_date')
        employer_residential_status = self.cleaned_data.get(
            'employer_residential_status'
        )
        if is_foreigner(employer_residential_status):
            if is_null(cleaned_field):
                error_msg = _('Passport expiry date field cannot be empty')
                raise ValidationError(error_msg)
            else:
                validate_passport_date(cleaned_field)
        else:
            return None

        return cleaned_field

    def clean_employer_marital_status(self):
        cleaned_field = self.cleaned_data.get('employer_marital_status')
        applicant_type = self.cleaned_data.get('applicant_type')
        if (
            applicant_type == EmployerTypeOfApplicantChoices.SPOUSE
            and cleaned_field != om_constants.MaritalStatusChoices.MARRIED
        ):
            raise ValidationError(
                _('''
                    Employer with Spouse application requires marriage status
                    to be "Married"
                ''')
            )
        else:
            return cleaned_field

    # def clean_employer_marriage_sg_registered(self):
    #     cleaned_field = self.cleaned_data.get(
    #         'employer_marriage_sg_registered'
    #     )
    #     marital_status = self.cleaned_data.get('employer_marital_status')
    #     if is_married(marital_status):
    #         if is_null(cleaned_field):
    #             error_msg = _('Marriage registration field cannot be empty')
    #             raise ValidationError(error_msg)
    #         else:
    #             return cleaned_field
    #     else:
    #         return cleaned_field

    def clean_spouse_name(self):
        cleaned_field = self.cleaned_data.get('spouse_name')
        marital_status = self.cleaned_data.get('employer_marital_status')
        if is_married(marital_status):
            if is_null(cleaned_field):
                error_msg = _('Employer spouse name field cannot be empty')
                raise ValidationError(error_msg)
            else:
                return cleaned_field
        else:
            return None

    def clean_spouse_gender(self):
        cleaned_field = self.cleaned_data.get('spouse_gender')
        marital_status = self.cleaned_data.get('employer_marital_status')
        if is_married(marital_status):
            if is_null(cleaned_field):
                error_msg = _('Employer spouse gender field cannot be empty')
                raise ValidationError(error_msg)
            else:
                return cleaned_field
        else:
            return None

    def clean_spouse_date_of_birth(self):
        cleaned_field = self.cleaned_data.get('spouse_date_of_birth')
        marital_status = self.cleaned_data.get('employer_marital_status')
        if is_married(marital_status):
            if is_null(cleaned_field):
                error_msg = _(
                    'Employer spouse date of birth field cannot be empty')
                raise ValidationError(error_msg)
            else:
                validate_age(cleaned_field, 18)
                return cleaned_field
        else:
            return None

    def clean_spouse_nationality(self):
        cleaned_field = self.cleaned_data.get('spouse_nationality')
        marital_status = self.cleaned_data.get('employer_marital_status')
        if is_married(marital_status):
            if is_null(cleaned_field):
                error_msg = _(
                    'Employer spouse nationality field cannot be empty')
                raise ValidationError(error_msg)
            else:
                return cleaned_field
        else:
            return None

    def clean_spouse_residential_status(self):
        cleaned_field = self.cleaned_data.get('spouse_residential_status')
        marital_status = self.cleaned_data.get('employer_marital_status')
        if is_married(marital_status):
            if is_null(cleaned_field):
                error_msg = _(
                    'Employer spouse residential status field cannot be empty')
                raise ValidationError(error_msg)
            else:
                return cleaned_field
        else:
            return None

    def clean_spouse_nric_num(self):
        cleaned_field = self.cleaned_data.get('spouse_nric_num')
        marital_status = self.cleaned_data.get('employer_marital_status')
        if is_married(marital_status):
            spouse_residential_status = self.cleaned_data.get(
                'spouse_residential_status'
            )
            if is_not_null(cleaned_field):
                if is_local(spouse_residential_status):
                    validate_nric("Employer's spouse's", cleaned_field)
                    ciphertext, nonce, tag = encrypt_string(
                        cleaned_field,
                        settings.ENCRYPTION_KEY
                    )
                    self.instance.spouse_nric_nonce = nonce
                    self.instance.spouse_nric_tag = tag
                    return ciphertext
                else:
                    return None
            else:
                return None
        else:
            return None

    def clean_spouse_fin_num(self):
        cleaned_field = self.cleaned_data.get('spouse_fin_num')
        marital_status = self.cleaned_data.get('employer_marital_status')
        if is_married(marital_status):
            spouse_residential_status = self.cleaned_data.get(
                'spouse_residential_status'
            )
            if is_foreigner(spouse_residential_status):
                validate_fin("Employer's spouse's", cleaned_field)
                ciphertext, nonce, tag = encrypt_string(
                    cleaned_field,
                    settings.ENCRYPTION_KEY
                )
                self.instance.spouse_fin_nonce = nonce
                self.instance.spouse_fin_tag = tag
                return ciphertext
            else:
                return None
        else:
            return None

    def clean_spouse_passport_num(self):
        cleaned_field = self.cleaned_data.get('spouse_passport_num')
        marital_status = self.cleaned_data.get('employer_marital_status')
        if is_not_null(cleaned_field):
            if is_married(marital_status):
                spouse_residential_status = self.cleaned_data.get(
                    'spouse_residential_status'
                )
                if is_foreigner(spouse_residential_status):
                    validate_passport("Employer's spouse", cleaned_field)
                    ciphertext, nonce, tag = encrypt_string(
                        cleaned_field,
                        settings.ENCRYPTION_KEY
                    )
                    self.instance.spouse_passport_nonce = nonce
                    self.instance.spouse_passport_tag = tag
                    return ciphertext
                else:
                    return None
            else:
                return None
        else:
            return None

    def clean_spouse_passport_date(self):
        cleaned_field = self.cleaned_data.get('spouse_passport_date')
        marital_status = self.cleaned_data.get('employer_marital_status')
        if is_not_null(cleaned_field):
            if is_married(marital_status):
                spouse_residential_status = self.cleaned_data.get(
                    'spouse_residential_status'
                )
                if is_foreigner(spouse_residential_status):
                    if is_null(cleaned_field):
                        error_msg = _('Passport expiry date field cannot be empty')
                        raise ValidationError(error_msg)
                    else:
                        validate_passport_date(cleaned_field)
                        return cleaned_field
                else:
                    return None
        else:
            return None


    def clean_employer_date_of_birth(self):
        cleaned_field = self.cleaned_data.get('employer_date_of_birth')
        validate_age(cleaned_field, 18)
        return cleaned_field

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        employer_nationality = cleaned_data.get('employer_nationality')
        employer_residential_status = cleaned_data.get(
            'employer_residential_status'
        )
        employer_spouse_nationality = cleaned_data.get(
            'employer_spouse_nationality'
        )
        employer_spouse_residential_status = cleaned_data.get(
            'employer_spouse_residential_status'
        )
        if employer_nationality == om_constants.FullNationsChoices.SINGAPORE:
            if not employer_residential_status == ResidentialStatusFullChoices.SC:
                error_msg = _('This employer must be a citizen of Singapore')
                raise ValidationError(error_msg)

        if employer_residential_status == ResidentialStatusFullChoices.SC:
            if not employer_nationality == om_constants.FullNationsChoices.SINGAPORE:
                error_msg = _('This employer must be a citizen of Singapore')
                raise ValidationError(error_msg)

        if employer_spouse_nationality:
            if employer_spouse_nationality == om_constants.FullNationsChoices.SINGAPORE:
                if not employer_spouse_residential_status == ResidentialStatusFullChoices.SC:
                    error_msg = _('This employer must be a citizen of Singapore')
                    raise ValidationError(error_msg)

            if employer_spouse_residential_status == ResidentialStatusFullChoices.SC:
                if not employer_spouse_nationality == om_constants.FullNationsChoices.SINGAPORE:
                    error_msg = _('This employer\'s spouse must be a citizen of Singapore')
                    raise ValidationError(error_msg)
        return cleaned_data

    def save(self):
        if self.changed_data and self.form_type == 'UPDATE':
            employer_strict_fields = [
                'employer_name',
                'employer_gender',
                'employer_mobile_number',
                'employer_home_number',
                'employer_email',
                'employer_address_1',
                'employer_address_2',
                'employer_post_code',
                'employer_date_of_birth',
                'employer_nationality',
                'employer_residential_status',
                'employer_nric_num',
                'employer_fin_num',
                'employer_passport_num',
                'employer_passport_date',
                'employer_marital_status',
                'employer_marriage_sg_registered',
                'spouse_name',
                'spouse_gender',
                'spouse_date_of_birth',
                'spouse_nationality',
                'spouse_residential_status',
                'spouse_nric_num',
                'spouse_fin_num',
                'spouse_passport_num',
                'spouse_passport_date',
            ]
            if not set(employer_strict_fields).isdisjoint(self.changed_data):
                employer_doc_qs = EmployerDoc.objects.filter(
                    employer=self.instance
                )
                for employer_doc in employer_doc_qs:
                    employer_doc.set_increment_version_number()

            if 'employer_email' in self.changed_data:
                self.instance.set_potential_employer_relation(
                    self.cleaned_data.get(
                        'employer_email'
                    )
                )
        else:
            if not self.instance.potential_employer:
                self.instance.set_potential_employer_relation(
                    self.cleaned_data.get(
                        'employer_email'
                    )
                )
        return super().save()


class EmployerSponsorForm(forms.ModelForm):
    class Meta:
        model = EmployerSponsor
        exclude = [
            'employer',
            'sponsor_1_nric_nonce',
            'sponsor_1_nric_tag',
            'sponsor_1_spouse_nric_nonce',
            'sponsor_1_spouse_nric_tag',
            'sponsor_1_spouse_fin_nonce',
            'sponsor_1_spouse_fin_tag',
            'sponsor_1_spouse_passport_nonce',
            'sponsor_1_spouse_passport_tag',
            'sponsor_2_nric_nonce',
            'sponsor_2_nric_tag',
            'sponsor_2_spouse_nric_nonce',
            'sponsor_2_spouse_nric_tag',
            'sponsor_2_spouse_fin_nonce',
            'sponsor_2_spouse_fin_tag',
            'sponsor_2_spouse_passport_nonce',
            'sponsor_2_spouse_passport_tag',
        ]

    def __init__(self, *args, **kwargs):
        self.user_pk = kwargs.pop('user_pk')
        self.authority = kwargs.pop('authority')
        self.form_type = kwargs.pop('form_type')
        self.level_0_pk = kwargs.pop('level_0_pk')
        super().__init__(*args, **kwargs)

        instance = self.instance
        s_1_nric_num = instance.get_sponsor_1_nric_full()
        s_1_spouse_nric_num = instance.get_sponsor_1_spouse_nric_full()
        s_1_spouse_fin_num = instance.get_sponsor_1_spouse_fin_full()
        s_1_spouse_passport_num = instance.get_sponsor_1_spouse_passport_full()
        s_2_nric_num = instance.get_sponsor_2_nric_full()
        s_2_spouse_nric_num = instance.get_sponsor_2_spouse_nric_full()
        s_2_spouse_fin_num = instance.get_sponsor_2_spouse_fin_full()
        s_2_spouse_passport_num = instance.get_sponsor_2_spouse_passport_full()
        self.initial.update({
            'sponsor_1_nric_num': s_1_nric_num,
            'sponsor_1_spouse_nric_num': s_1_spouse_nric_num,
            'sponsor_1_spouse_fin_num': s_1_spouse_fin_num,
            'sponsor_1_spouse_passport_num': s_1_spouse_passport_num,
            'sponsor_2_nric_num': s_2_nric_num,
            'sponsor_2_spouse_nric_num': s_2_spouse_nric_num,
            'sponsor_2_spouse_fin_num': s_2_spouse_fin_num,
            'sponsor_2_spouse_passport_num': s_2_spouse_passport_num
        })
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Sponsors
            Row(
                Column(
                    Row(
                        Column(
                            HTML(
                                """
                                <h5 class="fs-14">Sponsor 1's Information</h5>
                            """),
                            Row(
                                Column(
                                    'sponsor_1_relationship',
                                    css_class='form-group col-md-12 pr-md-3',
                                ),
                                Column(
                                    'sponsor_1_name',
                                    css_class='form-group col-md-12 pl-md-3',
                                )
                            ),
                            Row(
                                Column(
                                    'sponsor_1_gender',
                                    css_class='form-group col-md-12 pr-md-3',
                                ),
                                Column(
                                    'sponsor_1_nric_num',
                                    css_class='form-group col-md-12 pl-md-3',
                                )
                            ),
                            Row(
                                Column(
                                    Field(
                                        'sponsor_1_date_of_birth',
                                        type='text',
                                        onfocus="(this.type='date')",
                                        placeholder='Sponsor 1 date of birth'
                                    ),
                                    css_class='form-group col-md-12 pr-md-3',
                                ),
                                Column(
                                    'sponsor_1_nationality',
                                    css_class='form-group col-md-12 pl-md-3',
                                )
                            ),
                            Row(
                                Column(
                                    'sponsor_1_residential_status',
                                    css_class='form-group col-md-12 pr-md-3',
                                ),
                                Column(
                                    PrependedText(
                                        'sponsor_1_mobile_number', '+65',
                                    ),
                                    css_class='form-group col-md-12 pl-md-3',
                                )
                            ),
                            Row(
                                Column(
                                    'sponsor_1_email',
                                    css_class='form-group col-md-12 pr-md-3',
                                ),
                                Column(
                                    'sponsor_1_address_1',
                                    css_class='form-group col-md-12 pl-md-3',
                                )
                            ),
                            Row(
                                Column(
                                    'sponsor_1_address_2',
                                    css_class='form-group col-md-12 pr-md-3',
                                ),
                                Column(
                                    'sponsor_1_post_code',
                                    css_class='form-group col-md-12 pl-md-3',
                                )
                            ),
                            Row(
                                Column(
                                    'sponsor_1_marital_status',
                                    css_class='form-group col-md-12 pr-md-3',
                                )
                            ),
                            # Sponsor 1 spouse
                            Row(
                                Column(
                                    HTML(
                                        """
                                            <h5 class="fs-14">Sponsor 1 Spouse's Information</h5>
                                        """
                                    ),
                                    Row(
                                        Column(
                                            'sponsor_1_marriage_sg_registered',
                                            css_class='form-group col-md-12 spouse-1 pr-md-3',
                                        ),
                                        Column(
                                            'sponsor_1_spouse_name',
                                            css_class='form-group col-md-12 spouse-1 pl-md-3',
                                        )
                                    ),
                                    Row(
                                        Column(
                                            'sponsor_1_spouse_gender',
                                            css_class='form-group col-md-12 spouse-1 pr-md-3',
                                        ),
                                        Column(
                                            Field(
                                                'sponsor_1_spouse_date_of_birth',
                                                type='text',
                                                onfocus="(this.type='date')",
                                                placeholder='Sponsor 1 spouse date of birth'
                                            ),
                                            css_class='form-group col-md-12 spouse-1 pl-md-3',
                                        )
                                    ),
                                    Row(
                                        Column(
                                            'sponsor_1_spouse_nationality',
                                            css_class='form-group col-md-12 spouse-1 pr-md-3',
                                        ),
                                        Column(
                                            'sponsor_1_spouse_residential_status',
                                            css_class='form-group col-md-12 spouse-1 pl-md-3',
                                        )
                                    ),
                                    Row(
                                        Column(
                                            'sponsor_1_spouse_nric_num',
                                            css_class='form-group col-md-12 spouse-1 pr-md-3',
                                            id='sponsor1spouse_id_nric',
                                        ),
                                        Column(
                                            'sponsor_1_spouse_fin_num',
                                            css_class='form-group col-md-12 spouse-1 pl-md-3',
                                            id='sponsor1spouse_id_fin',
                                        )
                                    ),
                                    Row(
                                        Column(
                                            'sponsor_1_spouse_passport_num',
                                            css_class='form-group col-md-12 spouse-1 pr-md-3',
                                        ),
                                        Column(
                                            Field(
                                                'sponsor_1_spouse_passport_date',
                                                type='text',
                                                onfocus="(this.type='date')",
                                                placeholder='Sponsor 1 spouse passport expiry date',
                                            ),
                                            css_class='form-group col-md-12 spouse-1 pl-md-3',
                                        ),
                                        id='sponsor1spouse_id_passport',
                                    ),
                                ),
                                id="sponsor_1_spouse",
                                # hidden='true',
                            ),
                        ),
                        id="sponsor_1",
                    ),

                    # Is Sponsor 2 required?
                    Row(
                        Column(
                            HTML(
                                """
                                <h5 class="fs-14">Is Sponsor 2 required?</h5>
                            """),
                            Row(
                                Column(
                                    'sponsor_2_required',
                                    css_class='form-group col-md-12 pr-md-3',
                                )
                            ),
                        ),
                    ),

                    # Sponsor 2
                    Row(
                        Column(
                            HTML(
                                """
                                <h5 class="fs-14">Sponsor 2's Information</h5>
                            """),
                            Row(
                                Column(
                                    'sponsor_2_relationship',
                                    css_class='form-group col-md-12 sponsor-2 pr-md-3',
                                ),
                                Column(
                                    'sponsor_2_name',
                                    css_class='form-group col-md-12 sponsor-2 pl-md-3',
                                )
                            ),
                            Row(
                                Column(
                                    'sponsor_2_gender',
                                    css_class='form-group col-md-12 sponsor-2 pr-md-3',
                                ),
                                Column(
                                    'sponsor_2_nric_num',
                                    css_class='form-group col-md-12 sponsor-2 pl-md-3',
                                )
                            ),
                            Row(
                                Column(
                                    Field(
                                        'sponsor_2_date_of_birth',
                                        type='text',
                                        onfocus="(this.type='date')",
                                        placeholder='Sponsor 2 date of birth',
                                    ),
                                    css_class='form-group col-md-12 sponsor-2 pr-md-3',
                                ),
                                Column(
                                    'sponsor_2_nationality',
                                    css_class='form-group col-md-12 sponsor-2 pl-md-3',
                                )
                            ),
                            Row(
                                Column(
                                    'sponsor_2_residential_status',
                                    css_class='form-group col-md-12 sponsor-2 pr-md-3',
                                ),
                                Column(
                                    PrependedText(
                                        'sponsor_2_mobile_number', '+65',
                                    ),
                                    css_class='form-group col-md-12 pl-md-3',
                                )
                            ),
                            Row(
                                Column(
                                    'sponsor_2_email',
                                    css_class='form-group col-md-12 sponsor-2 pr-md-3',
                                ),
                                Column(
                                    'sponsor_2_address_1',
                                    css_class='form-group col-md-12 sponsor-2 pl-md-3',
                                )
                            ),
                            Row(
                                Column(
                                    'sponsor_2_address_2',
                                    css_class='form-group col-md-12 sponsor-2 pr-md-3',
                                ),
                                Column(
                                    'sponsor_2_post_code',
                                    css_class='form-group col-md-12 sponsor-2 pl-md-3',
                                )
                            ),
                            Row(
                                Column(
                                    'sponsor_2_marital_status',
                                    css_class='form-group col-md-12 sponsor-2 pr-md-3',
                                )
                            ),
                            # Sponsor 2 spouse
                            Row(
                                Column(
                                    HTML(
                                        """
                                            <h5 class="fs-14">Sponsor 2 Spouse's Information</h5>
                                        """),
                                    Row(
                                        Column(
                                            'sponsor_2_marriage_sg_registered',
                                            css_class='form-group col-md-12 spouse-2 pr-md-3',
                                        ),
                                        Column(
                                            'sponsor_2_spouse_name',
                                            css_class='form-group col-md-12 spouse-2 pl-md-3',
                                        )
                                    ),
                                    Row(
                                        Column(
                                            'sponsor_2_spouse_gender',
                                            css_class='form-group col-md-12 spouse-2 pr-md-3',
                                        ),
                                        Column(
                                            Field(
                                                'sponsor_2_spouse_date_of_birth',
                                                type='text',
                                                onfocus="(this.type='date')",
                                                placeholder='Sponsor 2 date of birth',
                                            ),
                                            css_class='form-group col-md-12 spouse-2',
                                        )
                                    ),
                                    Row(
                                        Column(
                                            'sponsor_2_spouse_nationality',
                                            css_class='form-group col-md-12 spouse-2 pr-md-3',
                                        ),
                                        Column(
                                            'sponsor_2_spouse_residential_status',
                                            css_class='form-group col-md-12 spouse-2 pl-md-3',
                                        )
                                    ),
                                    Row(
                                        Column(
                                            'sponsor_2_spouse_nric_num',
                                            css_class='form-group col-md-12 spouse-2 pr-md-3',
                                            id='sponsor2spouse_id_nric',
                                        ),
                                        Column(
                                            'sponsor_2_spouse_fin_num',
                                            css_class='form-group col-md-12 spouse-2 pl-md-3',
                                            id='sponsor2spouse_id_fin',
                                        )
                                    ),
                                    Row(
                                        Column(
                                            'sponsor_2_spouse_passport_num',
                                            css_class='form-group col-md-12 spouse-2 pr-md-3',
                                        ),
                                        Column(
                                            Field(
                                                'sponsor_2_spouse_passport_date',
                                                type='text',
                                                onfocus="(this.type='date')",
                                                placeholder='Sponsor 2 spouse passport expiry date',
                                            ),
                                            css_class='form-group col-md-12 spouse-2 pl-md-3',
                                        ),
                                        id='sponsor2spouse_id_passport',
                                    ),
                                ),
                                id="sponsor_2_spouse",
                                # hidden="true",
                            ),
                        ),
                        id="sponsor_2",
                        # hidden="true",
                    ),
                ),
                id='sponsors-section',
            ),

            # Submit
            Row(
                Column(
                    HTML(
                        '''
                        <a href="{% url 'employer_update_route' level_0_pk %}"
                        class="btn btn-xs-lg btn-outline-primary w-xs-40 w-25 mx-2">Back</a>
                        '''
                    ),
                    Submit(
                        'submit',
                        'Next',
                        css_class="btn btn-xs-lg btn-primary w-xs-40 w-25 mx-2"
                    ),
                    css_class='form-group col-24 text-center'
                )
            )
        )

    def clean_sponsor_1_nric_num(self):
        cleaned_field = self.cleaned_data.get('sponsor_1_nric_num')
        validate_nric("Sponsor 1", cleaned_field)
        ciphertext, nonce, tag = encrypt_string(
            cleaned_field,
            settings.ENCRYPTION_KEY
        )
        self.instance.sponsor_1_nric_nonce = nonce
        self.instance.sponsor_1_nric_tag = tag
        return ciphertext

    def clean_sponsor_1_marriage_sg_registered(self):
        cleaned_field = self.cleaned_data.get(
            'sponsor_1_marriage_sg_registered'
        )
        marital_status = self.cleaned_data.get('sponsor_1_marital_status')
        if is_married(marital_status):
            if is_null(cleaned_field):
                error_msg = _('Marriage registration field cannot be empty')
                raise ValidationError(error_msg)
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_1_date_of_birth(self):
        cleaned_field = self.cleaned_data.get('sponsor_1_date_of_birth')
        if is_null(cleaned_field):
            raise ValidationError(
                _('Sponsor 1 date of birth field cannot be empty')
            )
        else:
            validate_age(cleaned_field, 18)
            return cleaned_field

    def clean_sponsor_1_spouse_name(self):
        cleaned_field = self.cleaned_data.get('sponsor_1_spouse_name')
        marital_status = self.cleaned_data.get('sponsor_1_marital_status')
        if is_married(marital_status):
            if is_null(cleaned_field):
                error_msg = _('Sponsor 1 spouse name field cannot be empty')
                raise ValidationError(error_msg)
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_1_spouse_gender(self):
        cleaned_field = self.cleaned_data.get('sponsor_1_spouse_gender')
        marital_status = self.cleaned_data.get('sponsor_1_marital_status')
        if is_married(marital_status):
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 1 spouse gender field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_1_spouse_date_of_birth(self):
        cleaned_field = self.cleaned_data.get('sponsor_1_spouse_date_of_birth')
        marital_status = self.cleaned_data.get('sponsor_1_marital_status')
        if is_married(marital_status):
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 1 spouse date of birth field cannot be empty')
                )
            else:
                validate_age(cleaned_field, 18)
                return cleaned_field
        else:
            return None

    def clean_sponsor_1_spouse_nationality(self):
        cleaned_field = self.cleaned_data.get('sponsor_1_spouse_nationality')
        marital_status = self.cleaned_data.get('sponsor_1_marital_status')
        if is_married(marital_status):
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 1 spouse nationality field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_1_spouse_residential_status(self):
        cleaned_field = self.cleaned_data.get(
            'sponsor_1_spouse_residential_status'
        )
        marital_status = self.cleaned_data.get('sponsor_1_marital_status')
        if is_married(marital_status):
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 1 spouse residential status field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_1_spouse_nric_num(self):
        cleaned_field = self.cleaned_data.get('sponsor_1_spouse_nric_num')
        marital_status = self.cleaned_data.get('sponsor_1_marital_status')
        if is_married(marital_status):
            spouse_residential_status = self.cleaned_data.get(
                'sponsor_1_spouse_residential_status'
            )
            if is_not_null(cleaned_field):
                if is_local(spouse_residential_status):
                    validate_nric("Sponsor 1's spouse", cleaned_field)
                    ciphertext, nonce, tag = encrypt_string(
                        cleaned_field,
                        settings.ENCRYPTION_KEY
                    )
                    self.instance.sponsor_1_spouse_nric_nonce = nonce
                    self.instance.sponsor_1_spouse_nric_tag = tag
                    return ciphertext
                else:
                    return None
            else:
                return None
        else:
            return None

    def clean_sponsor_1_spouse_fin_num(self):
        cleaned_field = self.cleaned_data.get('sponsor_1_spouse_fin_num')
        marital_status = self.cleaned_data.get('sponsor_1_marital_status')
        if is_married(marital_status):
            spouse_residential_status = self.cleaned_data.get(
                'sponsor_1_spouse_residential_status'
            )
            if is_foreigner(spouse_residential_status):
                validate_fin("Sponsor 1's spouse's", cleaned_field)
                ciphertext, nonce, tag = encrypt_string(
                    cleaned_field,
                    settings.ENCRYPTION_KEY
                )
                self.instance.sponsor_1_spouse_fin_nonce = nonce
                self.instance.sponsor_1_spouse_fin_tag = tag
                return ciphertext
            else:
                return None
        else:
            return None

    def clean_sponsor_1_spouse_passport_num(self):
        cleaned_field = self.cleaned_data.get('sponsor_1_spouse_passport_num')
        marital_status = self.cleaned_data.get('sponsor_1_marital_status')
        if is_not_null(cleaned_field):
            if is_married(marital_status):
                spouse_residential_status = self.cleaned_data.get(
                    'sponsor_1_spouse_residential_status'
                )
                if is_foreigner(spouse_residential_status):
                    validate_passport("Sponsor 1's spouse", cleaned_field)
                    ciphertext, nonce, tag = encrypt_string(
                        cleaned_field,
                        settings.ENCRYPTION_KEY
                    )
                    self.instance.sponsor_1_spouse_passport_nonce = nonce
                    self.instance.sponsor_1_spouse_passport_tag = tag
                    return ciphertext
                else:
                    return None
            else:
                return None
        else:
            return None

    def clean_sponsor_1_spouse_passport_date(self):
        cleaned_field = self.cleaned_data.get('sponsor_1_spouse_passport_date')
        marital_status = self.cleaned_data.get('sponsor_1_marital_status')
        if is_not_null(cleaned_field):
            if is_married(marital_status):
                spouse_residential_status = self.cleaned_data.get(
                    'sponsor_1_spouse_residential_status'
                )
                if is_foreigner(spouse_residential_status):
                    if is_null(cleaned_field):
                        error_msg = _('Passport expiry date field cannot be empty')
                        raise ValidationError(error_msg)

                validate_passport_date(cleaned_field)
            else:
                return None
        else:
            return None

        return cleaned_field

    def clean_sponsor_2_relationship(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_relationship')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 relationship field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_name(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_name')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 name field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_gender(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_gender')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 gender field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_date_of_birth(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_date_of_birth')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 date of birth field cannot be empty')
                )
            else:
                validate_age(cleaned_field, 18)
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_nric_num(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_nric_num')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            validate_nric("Sponsor 2", cleaned_field)
            ciphertext, nonce, tag = encrypt_string(
                cleaned_field,
                settings.ENCRYPTION_KEY
            )
            self.instance.sponsor_2_nric_nonce = nonce
            self.instance.sponsor_2_nric_tag = tag
            return ciphertext
        else:
            return None

    def clean_sponsor_2_nationality(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_nationality')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 nationality field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_residential_status(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_residential_status')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 residential status field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_mobile_number(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_mobile_number')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 mobile field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_email(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_email')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 email field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_address_1(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_address_1')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 address field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_post_code(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_post_code')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 postal code field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_marital_status(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_marital_status')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 marital status field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_marriage_sg_registered(self):
        cleaned_field = self.cleaned_data.get(
            'sponsor_2_marriage_sg_registered'
        )
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 marriage registration field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_spouse_name(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_spouse_name')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        marital_status = self.cleaned_data.get('sponsor_2_marital_status')
        if sponsor_2_required:
            if is_married(marital_status):
                if is_null(cleaned_field):
                    raise ValidationError(
                        _('Sponsor 2 spouse name field cannot be empty')
                    )
                else:
                    return cleaned_field
            else:
                return None
        else:
            return None

    def clean_sponsor_2_spouse_gender(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_spouse_gender')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        marital_status = self.cleaned_data.get('sponsor_2_marital_status')
        if sponsor_2_required and is_married(marital_status):
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 spouse gender field cannot be empty')
                )
            else:
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_spouse_date_of_birth(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_spouse_date_of_birth')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        marital_status = self.cleaned_data.get('sponsor_2_marital_status')
        if sponsor_2_required and is_married(marital_status):
            if is_null(cleaned_field):
                raise ValidationError(
                    _('Sponsor 2 spouse date of birth field cannot be empty')
                )
            else:
                validate_age(cleaned_field, 18)
                return cleaned_field
        else:
            return None

    def clean_sponsor_2_spouse_nationality(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_spouse_nationality')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        marital_status = self.cleaned_data.get('sponsor_2_marital_status')
        if sponsor_2_required:
            if is_married(marital_status):
                if is_null(cleaned_field):
                    raise ValidationError(
                        _('Sponsor 2 spouse nationality field cannot be empty')
                    )
                else:
                    return cleaned_field
            else:
                return None
        else:
            return None

    def clean_sponsor_2_spouse_residential_status(self):
        cleaned_field = self.cleaned_data.get(
            'sponsor_2_spouse_residential_status'
        )
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        marital_status = self.cleaned_data.get('sponsor_2_marital_status')
        if sponsor_2_required:
            if is_married(marital_status):
                if is_null(cleaned_field):
                    error_msg = _(
                        'Sponsor 2 spouse residential status field cannot be empty')
                    raise ValidationError(error_msg)
                else:
                    return cleaned_field
            else:
                return None
        else:
            return None

    def clean_sponsor_2_spouse_nric_num(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_spouse_nric_num')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        marital_status = self.cleaned_data.get('sponsor_2_marital_status')
        if sponsor_2_required:
            if is_married(marital_status):
                spouse_residential_status = self.cleaned_data.get(
                    'sponsor_2_spouse_residential_status'
                )
                if is_not_null(cleaned_field):
                    if is_local(spouse_residential_status):
                        validate_nric("Sponsor 2's spouse", cleaned_field)
                        ciphertext, nonce, tag = encrypt_string(
                            cleaned_field,
                            settings.ENCRYPTION_KEY
                        )
                        self.instance.sponsor_2_spouse_nric_nonce = nonce
                        self.instance.sponsor_2_spouse_nric_tag = tag
                        return ciphertext
                    else:
                        return None
                else:
                    return None
            else:
                return None
        else:
            return None

    def clean_sponsor_2_spouse_fin_num(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_spouse_fin_num')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        marital_status = self.cleaned_data.get('sponsor_2_marital_status')
        if sponsor_2_required and is_married(marital_status):
            spouse_residential_status = self.cleaned_data.get(
                'sponsor_2_spouse_residential_status'
            )
            if is_foreigner(spouse_residential_status):
                validate_fin("Sponsor 2's spouse's", cleaned_field)
                ciphertext, nonce, tag = encrypt_string(
                    cleaned_field,
                    settings.ENCRYPTION_KEY
                )
                self.instance.sponsor_2_spouse_fin_nonce = nonce
                self.instance.sponsor_2_spouse_fin_tag = tag
                return ciphertext
            else:
                return None
        else:
            return None

    def clean_sponsor_2_spouse_passport_num(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_spouse_passport_num')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        marital_status = self.cleaned_data.get('sponsor_2_marital_status')
        if is_not_null(cleaned_field):
            if sponsor_2_required and is_married(marital_status):
                spouse_residential_status = self.cleaned_data.get(
                    'sponsor_2_spouse_residential_status'
                )
                if is_foreigner(spouse_residential_status):
                    validate_passport("Sponsor 2's spouse", cleaned_field)
                    ciphertext, nonce, tag = encrypt_string(
                        cleaned_field,
                        settings.ENCRYPTION_KEY
                    )
                    self.instance.sponsor_2_spouse_passport_nonce = nonce
                    self.instance.sponsor_2_spouse_passport_tag = tag
                    return ciphertext
                else:
                    return None
            else:
                return None
        else:
            return None

    def clean_sponsor_2_spouse_passport_date(self):
        cleaned_field = self.cleaned_data.get('sponsor_2_spouse_passport_date')
        sponsor_2_required = self.cleaned_data.get('sponsor_2_required')
        marital_status = self.cleaned_data.get('sponsor_2_marital_status')
        if is_not_null(cleaned_field):
            if sponsor_2_required and is_married(marital_status):
                spouse_residential_status = self.cleaned_data.get(
                    'sponsor_2_spouse_residential_status'
                )
                if is_foreigner(spouse_residential_status):
                    error_msg = _('Passport expiry date field cannot be empty')
                    error_msg = error_msg if not cleaned_field else None
                    if error_msg:
                        raise ValidationError(error_msg)
                    else:
                        return cleaned_field
                else:
                    return None
            else:
                return None
        else:
            return None

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        sponsor_1_nationality = cleaned_data.get('sponsor_1_nationality')
        sponsor_1_residential_status = cleaned_data.get(
            'sponsor_1_residential_status'
        )
        sponsor_1_spouse_nationality = cleaned_data.get(
            'sponsor_1_spouse_nationality'
        )
        sponsor_1_spouse_residential_status = cleaned_data.get(
            'sponsor_1_spouse_residential_status'
        )

        if not nationality_residential_status_match(
            sponsor_1_nationality,
            sponsor_1_residential_status
        ):
            error_msg = _('Sponsor 1 must be a citizen of Singapore')
            raise ValidationError(error_msg)

        if sponsor_1_spouse_nationality:
            if not nationality_residential_status_match(
                sponsor_1_spouse_nationality,
                sponsor_1_spouse_residential_status
            ):
                error_msg = _(
                    'Sponsor 1\'s spouse must be a citizen of Singapore')
                raise ValidationError(error_msg)

        sponsor_2_required = cleaned_data.get('sponsor_2_required')
        if sponsor_2_required:
            sponsor_2_nationality = cleaned_data.get('sponsor_2_nationality')
            sponsor_2_residential_status = cleaned_data.get(
                'sponsor_2_residential_status'
            )
            sponsor_2_spouse_nationality = cleaned_data.get(
                'sponsor_2_spouse_nationality'
            )
            sponsor_2_spouse_residential_status = cleaned_data.get(
                'sponsor_2_spouse_residential_status'
            )

            if not nationality_residential_status_match(
                sponsor_2_nationality,
                sponsor_2_residential_status
            ):
                error_msg = _('Sponsor 2 must be a citizen of Singapore')
                raise ValidationError(error_msg)

            if sponsor_2_spouse_nationality:
                if not nationality_residential_status_match(
                    sponsor_2_spouse_nationality,
                    sponsor_2_spouse_residential_status
                ):
                    error_msg = _(
                        'Sponsor 2\'s spouse must be a citizen of Singapore')
                    raise ValidationError(error_msg)

        return cleaned_data

    def save(self):
        if self.changed_data and self.form_type == 'UPDATE':
            strict_fields = [
                'sponsor_1_relationship',
                'sponsor_1_name',
                'sponsor_1_gender',
                'sponsor_1_date_of_birth',
                'sponsor_1_nric_num',
                'sponsor_1_nationality',
                'sponsor_1_residential_status',
                'sponsor_1_mobile_number',
                'sponsor_1_email',
                'sponsor_1_address_1',
                'sponsor_1_address_2',
                'sponsor_1_post_code',
                'sponsor_1_marital_status',
                'sponsor_1_marriage_sg_registered',
                'sponsor_1_spouse_name',
                'sponsor_1_spouse_gender',
                'sponsor_1_spouse_date_of_birth',
                'sponsor_1_spouse_nationality',
                'sponsor_1_spouse_residential_status',
                'sponsor_1_spouse_nric_num',
                'sponsor_1_spouse_fin_num',
                'sponsor_1_spouse_passport_num',
                'sponsor_1_spouse_passport_date',
                'sponsor_2_required',
                'sponsor_2_relationship',
                'sponsor_2_name',
                'sponsor_2_gender',
                'sponsor_2_date_of_birth',
                'sponsor_2_nric_num',
                'sponsor_2_nationality',
                'sponsor_2_residential_status',
                'sponsor_2_mobile_number',
                'sponsor_2_email',
                'sponsor_2_address_1',
                'sponsor_2_address_2',
                'sponsor_2_post_code',
                'sponsor_2_marital_status',
                'sponsor_2_marriage_sg_registered',
                'sponsor_2_spouse_name',
                'sponsor_2_spouse_gender',
                'sponsor_2_spouse_date_of_birth',
                'sponsor_2_spouse_nationality',
                'sponsor_2_spouse_residential_status',
                'sponsor_2_spouse_nric_num',
                'sponsor_2_spouse_fin_num',
                'sponsor_2_spouse_passport_num',
                'sponsor_2_spouse_passport_date'
            ]
            if not set(strict_fields).isdisjoint(self.changed_data):
                employer_doc_qs = EmployerDoc.objects.filter(
                    employer__rn_sponsor_employer=self.instance
                )
                for employer_doc in employer_doc_qs:
                    employer_doc.set_increment_version_number()
        return super().save()


class EmployerJointApplicantForm(forms.ModelForm):
    class Meta:
        model = EmployerJointApplicant
        exclude = [
            'employer',
            'joint_applicant_nric_nonce',
            'joint_applicant_nric_tag',
            'joint_applicant_spouse_nric_nonce',
            'joint_applicant_spouse_nric_tag',
            'joint_applicant_spouse_fin_nonce',
            'joint_applicant_spouse_fin_tag',
            'joint_applicant_spouse_passport_nonce',
            'joint_applicant_spouse_passport_tag',
        ]

    def __init__(self, *args, **kwargs):
        self.user_pk = kwargs.pop('user_pk')
        self.authority = kwargs.pop('authority')
        self.form_type = kwargs.pop('form_type')
        self.level_0_pk = kwargs.pop('level_0_pk')
        super().__init__(*args, **kwargs)

        ja_nric_num = self.instance.get_joint_applicant_nric_full()
        jas_nric_num = self.instance.get_joint_applicant_spouse_nric_full()
        jas_fin_num = self.instance.get_joint_applicant_spouse_fin_full()
        jas_pass_num = self.instance.get_joint_applicant_spouse_passport_full()
        self.initial.update({
            'joint_applicant_nric_num': ja_nric_num,
            'joint_applicant_spouse_nric_num': jas_nric_num,
            'joint_applicant_spouse_fin_num': jas_fin_num,
            'joint_applicant_spouse_passport_num': jas_pass_num
        })

        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Joint Applicants
            Row(
                Column(
                    HTML(
                        """
                        <h5 class="fs-14">Joint Applicant's Information</h5>
                    """),
                    Row(
                        Column(
                            'joint_applicant_relationship',
                            css_class='form-group col-md-12 pr-md-3',
                        ),
                        Column(
                            'joint_applicant_name',
                            css_class='form-group col-md-12 pl-md-3',
                        )
                    ),
                    Row(
                        Column(
                            'joint_applicant_gender',
                            css_class='form-group col-md-12 pr-md-3',
                        ),
                        Column(
                            Field(
                                'joint_applicant_date_of_birth',
                                type='text',
                                onfocus="(this.type='date')",
                                placeholder='Joint applicant date of birth'
                            ),
                            css_class='form-group col-md-12 pl-md-3',
                        )
                    ),
                    Row(
                        Column(
                            'joint_applicant_nric_num',
                            css_class='form-group col-md-12 pr-md-3',
                        ),
                        Column(
                            'joint_applicant_nationality',
                            css_class='form-group col-md-12 pl-md-3',
                        )
                    ),
                    Row(
                        Column(
                            'joint_applicant_residential_status',
                            css_class='form-group col-md-12 pr-md-3',
                        ),
                        Column(
                            'joint_applicant_address_1',
                            css_class='form-group col-md-12 pl-md-3',
                        )
                    ),
                    Row(
                        Column(
                            'joint_applicant_address_2',
                            css_class='form-group col-md-12 pr-md-3',
                        ),
                        Column(
                            'joint_applicant_post_code',
                            css_class='form-group col-md-12 pl-md-3',
                        )
                    ),
                    Row(
                        Column(
                            'joint_applicant_marital_status',
                            css_class='form-group col-md-12 pl-md-3',
                        )
                    ),

                    # Joint applicant spouse
                    Row(
                        Column(
                            HTML(
                                """
                                <h5 class="fs-14">Joint Applicant Spouse's Information</h5>
                                """),
                            Row(
                                Column(
                                    'joint_applicant_marriage_sg_registered',
                                    css_class='form-group col-md-12 spouse-1',
                                ),
                                Column(
                                    'joint_applicant_spouse_name',
                                    css_class='form-group col-md-12 spouse-1',
                                )
                            ),
                            Row(
                                Column(
                                    'joint_applicant_spouse_gender',
                                    css_class='form-group col-md-12 spouse-1',
                                ),
                                Column(
                                    Field(
                                        'joint_applicant_spouse_date_of_birth',
                                        type='text',
                                        onfocus="(this.type='date')",
                                        placeholder='Joint applicant spouse date of birth'
                                    ),
                                    css_class='form-group col-md-12 spouse-1',
                                )
                            ),
                            Row(
                                Column(
                                    'joint_applicant_spouse_nationality',
                                    css_class='form-group col-md-12 spouse-1',
                                ),
                                Column(
                                    'joint_applicant_spouse_residential_status',
                                    css_class='form-group col-md-12 spouse-1',
                                )
                            ),
                            Row(
                                Column(
                                    'joint_applicant_spouse_nric_num',
                                    css_class='form-group col-md-12 spouse-1',
                                    id='ja_spouse_id_nric',
                                ),
                                Column(
                                    'joint_applicant_spouse_fin_num',
                                    css_class='form-group col-md-12 spouse-1',
                                    id='ja_spouse_id_fin',
                                )
                            ),
                            Row(
                                Column(
                                    'joint_applicant_spouse_passport_num',
                                    css_class='form-group col-md-12 spouse-1',
                                ),
                                Column(
                                    Field(
                                        'joint_applicant_spouse_passport_date',
                                        type='text',
                                        onfocus="(this.type='date')",
                                        placeholder='Joint applicant spouse passport expiry date',
                                    ),
                                    css_class='form-group col-md-12 spouse-1',
                                ),
                                id='ja_spouse_id_passport',
                            ),
                        ),
                        id="joint_applicant_spouse",
                        # hidden="true",
                    ),
                ),
            ),

            # Submit
            Row(
                Column(
                    HTML(
                        '''
                        <a href="{% url 'employer_update_route' level_0_pk %}"
                        class="btn btn-xs-lg btn-outline-primary w-xs-40 w-25 mx-2">Back</a>
                        '''
                    ),
                    Submit(
                        'submit',
                        'Next',
                        css_class="btn btn-xs-lg btn-primary w-xs-40 w-25 mx-2"
                    ),
                    css_class='form-group col-24 text-center'
                )
            )
        )

    def clean_joint_applicant_nric_num(self):
        cleaned_field = self.cleaned_data.get('joint_applicant_nric_num')
        validate_nric("The joint applicant", cleaned_field)
        ciphertext, nonce, tag = encrypt_string(
            cleaned_field,
            settings.ENCRYPTION_KEY
        )
        self.instance.joint_applicant_nric_nonce = nonce
        self.instance.joint_applicant_nric_tag = tag
        return ciphertext

    def clean_joint_applicant_date_of_birth(self):
        cleaned_field = self.cleaned_data.get('joint_applicant_date_of_birth')
        validate_age(cleaned_field, 18)
        return cleaned_field

    def clean_joint_applicant_spouse_nric_num(self):
        cleaned_field = self.cleaned_data.get(
            'joint_applicant_spouse_nric_num'
        )
        marital_status = self.cleaned_data.get(
            'joint_applicant_marital_status'
        )
        if is_married(marital_status):
            spouse_residential_status = self.cleaned_data.get(
                'joint_applicant_spouse_residential_status'
            )
            if is_not_null(cleaned_field):
                if is_local(spouse_residential_status):
                    validate_nric("The joint applicant's spouse", cleaned_field)
                    ciphertext, nonce, tag = encrypt_string(
                        cleaned_field,
                        settings.ENCRYPTION_KEY
                    )
                    self.instance.joint_applicant_spouse_nric_nonce = nonce
                    self.instance.joint_applicant_spouse_nric_tag = tag
                    return ciphertext
                else:
                    return None
            else:
                return None
        else:
            return None

    def clean_joint_applicant_spouse_fin_num(self):
        cleaned_field = self.cleaned_data.get('joint_applicant_spouse_fin_num')
        marital_status = self.cleaned_data.get(
            'joint_applicant_marital_status'
        )
        if is_married(marital_status):
            spouse_residential_status = self.cleaned_data.get(
                'joint_applicant_spouse_residential_status'
            )
            if is_foreigner(spouse_residential_status):
                validate_fin("The Joint Applicant spouse's", cleaned_field)
                ciphertext, nonce, tag = encrypt_string(
                    cleaned_field,
                    settings.ENCRYPTION_KEY
                )
                self.instance.joint_applicant_spouse_fin_nonce = nonce
                self.instance.joint_applicant_spouse_fin_tag = tag
                return ciphertext
            else:
                return None
        else:
            return None

    def clean_joint_applicant_spouse_passport_num(self):
        cleaned_field = self.cleaned_data.get(
            'joint_applicant_spouse_passport_num'
        )
        marital_status = self.cleaned_data.get(
            'joint_applicant_marital_status'
        )
        if is_married(marital_status):
            spouse_residential_status = self.cleaned_data.get(
                'joint_applicant_spouse_residential_status'
            )
            if is_foreigner(spouse_residential_status):
                validate_passport("The joint applicant's spouse", cleaned_field)
                ciphertext, nonce, tag = encrypt_string(
                    cleaned_field,
                    settings.ENCRYPTION_KEY
                )
                self.instance.joint_applicant_spouse_passport_nonce = nonce
                self.instance.joint_applicant_spouse_passport_tag = tag
                return ciphertext
            else:
                return None
        else:
            return None

    def clean_joint_applicant_spouse_passport_date(self):
        cleaned_field = self.cleaned_data.get(
            'joint_applicant_spouse_passport_date'
        )
        marital_status = self.cleaned_data.get(
            'joint_applicant_marital_status'
        )
        if is_married(marital_status):
            spouse_residential_status = self.cleaned_data.get(
                'joint_applicant_spouse_residential_status'
            )
            if is_foreigner(spouse_residential_status):
                if is_null(cleaned_field):
                    error_msg = _('Passport expiry date field cannot be empty')
                    raise ValidationError(error_msg)
                else:
                    return cleaned_field
            else:
                return None
        else:
            return None

    def clean_joint_applicant_spouse_date_of_birth(self):
        cleaned_field = self.cleaned_data.get(
            'joint_applicant_spouse_date_of_birth')
        marital_status = self.cleaned_data.get(
            'joint_applicant_marital_status'
        )
        if is_married(marital_status):
            if is_null(cleaned_field):
                error_msg = _('Spouse date of birth field cannot be empty')
                raise ValidationError(error_msg)
            else:
                validate_age(cleaned_field, 18)
        else:
            return None

        return cleaned_field

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        joint_applicant_nationality = cleaned_data.get('employer_nationality')
        joint_applicant_residential_status = cleaned_data.get(
            'employer_residential_status'
        )
        joint_applicant_spouse_nationality = cleaned_data.get(
            'employer_spouse_nationality'
        )
        joint_applicant_spouse_residential_status = cleaned_data.get(
            'employer_spouse_residential_status'
        )
        if not (
            joint_applicant_nationality == om_constants.FullNationsChoices.SINGAPORE
            and joint_applicant_residential_status == ResidentialStatusFullChoices.SC
        ):
            error_msg = _(
                'This joint applicant must be a citizen of Singapore')
            raise ValidationError(error_msg)

        if joint_applicant_spouse_nationality:
            if not (
                joint_applicant_spouse_nationality == om_constants.FullNationsChoices.SINGAPORE
                and joint_applicant_spouse_residential_status == ResidentialStatusFullChoices.SC
            ):
                error_msg = _(
                    'This joint applicant\'s spouse must be a citizen of Singapore')
                raise ValidationError(error_msg)

        joint_applicant_address_1 = cleaned_data.get(
            'joint_applicant_address_1')
        joint_applicant_address_2 = cleaned_data.get(
            'joint_applicant_address_2')
        joint_applicant_post_code = cleaned_data.get(
            'joint_applicant_post_code')
        employer_obj = Employer.objects.get(pk=self.level_0_pk)
        if (
            employer_obj.employer_address_1 != joint_applicant_address_1
            or employer_obj.employer_address_2 != joint_applicant_address_2
            or employer_obj.employer_post_code != joint_applicant_post_code
        ):
            error_msg = _(
                'The joint applicant must stay in the same residence as the employer')
            raise ValidationError(error_msg)

        return cleaned_data

    def save(self):
        if self.changed_data and self.form_type == 'UPDATE':
            strict_fields = [
                'joint_applicant_relationship',
                'joint_applicant_name',
                'joint_applicant_gender',
                'joint_applicant_date_of_birth',
                'joint_applicant_nric_num',
                'joint_applicant_nationality',
                'joint_applicant_residential_status',
                'joint_applicant_address_1',
                'joint_applicant_address_2',
                'joint_applicant_post_code',
                'joint_applicant_marital_status',
                'joint_applicant_marriage_sg_registered',
                'joint_applicant_spouse_name',
                'joint_applicant_spouse_gender',
                'joint_applicant_spouse_date_of_birth',
                'joint_applicant_spouse_nationality',
                'joint_applicant_spouse_residential_status',
                'joint_applicant_spouse_nric_num',
                'joint_applicant_spouse_fin_num',
                'joint_applicant_spouse_passport_num',
                'joint_applicant_spouse_passport_date'
            ]
            if not set(strict_fields).isdisjoint(self.changed_data):
                employer_doc_qs = EmployerDoc.objects.filter(
                    employer__rn_ja_employer=self.instance
                )
                for employer_doc in employer_doc_qs:
                    employer_doc.set_increment_version_number()
        return super().save()


class EmployerIncomeDetailsForm(forms.ModelForm):
    class Meta:
        model = EmployerIncome
        exclude = [
            'employer'
        ]

    def __init__(self, *args, **kwargs):
        self.user_pk = kwargs.pop('user_pk')
        self.authority = kwargs.pop('authority')
        self.form_type = kwargs.pop('form_type')
        self.monthly_income_label = kwargs.pop('monthly_income_label')
        self.level_0_pk = kwargs.pop('level_0_pk')
        super().__init__(*args, **kwargs)

        employer = Employer.objects.get(pk=self.level_0_pk)
        if employer.applicant_type == EmployerTypeOfApplicantChoices.SPONSOR:
            back_url = 'employer_sponsor_update_route'
        elif employer.applicant_type == EmployerTypeOfApplicantChoices.JOINT_APPLICANT:
            back_url = 'employer_jointapplicant_update_route'
        else:
            back_url = 'employer_update_route'

        # Set form field label based on applicant type
        self.fields['monthly_income'].label = self.monthly_income_label[0]
        self.fields['worked_in_sg'].label = self.monthly_income_label[1]

        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Income Details
            Row(
                Column(
                    HTML(
                        """
                        <h5 class="fs-14">Income Details</h5>
                    """),
                    Row(
                        Column(
                            'worked_in_sg',
                            css_class='form-group col-xl-12 pr-xl-3'
                        ),
                        Column(
                            'monthly_income',
                            css_class='form-group col-xl-12 pl-xl-3',
                        )
                    ),
                ),
                id='income-details-section',
            ),

            # Submit
            Row(
                Column(
                    HTML(
                        f'''
                        <a href="{{% url '{back_url}' level_0_pk %}}"
                        class="btn btn-xs-lg btn-outline-primary w-xs-40 w-25 mx-2">Back</a>
                        '''
                    ),
                    Submit(
                        'submit',
                        'Next',
                        css_class="btn btn-xs-lg btn-primary w-xs-40 w-25 mx-2"
                    ),
                    css_class='form-group col-24 text-center'
                )
            )
        )

    def save(self):
        if self.changed_data and self.form_type == 'UPDATE':
            strict_fields = [
                'worked_in_sg',
                'monthly_income',
            ]
            if not set(strict_fields).isdisjoint(self.changed_data):
                employer_doc_qs = EmployerDoc.objects.filter(
                    employer__rn_income_employer=self.instance
                )
                for employer_doc in employer_doc_qs:
                    employer_doc.set_increment_version_number()
        return super().save()


class EmployerHouseholdDetailsForm(forms.ModelForm):
    class Meta:
        model = EmployerHousehold
        exclude = [
            'employer',
            'household_id_nonce',
            'household_id_tag',
        ]

    def save(self, *args, **kwargs):
        self.instance.employer = self.employer
        return super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.employer_id = kwargs.pop('employer_id')
        self.employer = Employer.objects.get(
            pk=self.employer_id
        )
        super().__init__(*args, **kwargs)
        instance = self.instance
        self.initial.update({
            'household_id_num': instance.get_household_id_full(),
        })

    def clean_household_id_num(self):
        cleaned_field = self.cleaned_data.get('household_id_num')
        validate_nric("This member", cleaned_field)
        ciphertext, nonce, tag = encrypt_string(
            cleaned_field,
            settings.ENCRYPTION_KEY
        )
        self.instance.household_id_nonce = nonce
        self.instance.household_id_tag = tag
        return ciphertext


class MaidInventoryForm(forms.ModelForm):
    class Meta:
        model = MaidInventory
        exclude = [
            'employer_doc',
        ]

    def save(self, *args, **kwargs):
        self.instance.employer_doc = self.employer_doc
        return super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.employer_doc_id = kwargs.pop('employer_doc_id')
        self.employer_doc = EmployerDoc.objects.get(
            pk=self.employer_doc_id
        )
        super().__init__(*args, **kwargs)


class EmployerDocForm(forms.ModelForm):
    class Meta:
        model = EmployerDoc
        exclude = []

    def __init__(self, *args, **kwargs):
        self.user_pk = kwargs.pop('user_pk')
        self.authority = kwargs.pop('authority')
        self.form_type = kwargs.pop('form_type')
        self.agency_id = kwargs.pop('agency_id')
        super().__init__(*args, **kwargs)

        current_user = get_user_model().objects.get(pk=self.user_pk)
        employers_qs = Employer.objects.filter(
            agency_employee__agency__pk=self.agency_id,
        )
        fdw_qs = Maid.objects.filter(agency=Agency.objects.get(
            pk=self.agency_id
        ))
        self.fields['fdw'].queryset = fdw_qs

        if (
            self.authority == om_constants.AG_OWNERS
            or self.authority == om_constants.AG_ADMINS
            or self.authority == om_constants.AG_ADMIN_STAFF
        ):
            self.fields['employer'].queryset = employers_qs
        elif self.authority == om_constants.AG_MANAGERS:
            self.fields['employer'].queryset = employers_qs.filter(
                agency_employee__branch=current_user.agency_employee.branch
            )
        else:
            self.fields['employer'].queryset = employers_qs.filter(
                agency_employee=current_user.agency_employee
            )

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                """
                <h5 class="doc-section-header">Case Information</h5>
            """),

            Row(
                Column(
                    'case_ref_no',
                    css_class='form-group col-lg-12 pr-lg-3'
                ),
                Column(
                    Field(
                        'agreement_date',
                        type='text',
                        onfocus="(this.type='date')",
                        placeholder='Contract date'
                    ),
                    css_class='form-group col-lg-12 pl-lg-3'
                )
            ),
            Row(
                Column(
                    'employer',
                    css_class='form-group col-lg-12 pr-lg-3',
                ),
                Column(
                    'fdw',
                    css_class='form-group col-lg-12 pl-lg-3'
                )
            ),
            Row(
                Column(
                    PrependedText(
                        'fdw_salary', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-lg-12 pr-lg-3'
                ),
                Column(
                    PrependedText(
                        'fdw_loan', '$',
                        min='0', max='10000',
                    ),
                    css_class='form-group col-lg-12 pl-lg-3'
                )
            ),
            Row(
                Column(
                    'fdw_off_days',
                    css_class='form-group col-xl-12 pr-xl-3',
                ),
                Column(
                    PrependedText(
                        'fdw_monthly_loan_repayment', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-lg-12 pl-lg-3'
                ),
                Column(
                    'fdw_off_day_of_week',
                    css_class='form-group col-lg-12 pr-lg-3',
                )
            ),
            # Submit
            Row(
                Column(
                    Submit(
                        'submit',
                        'Next',
                        css_class="btn btn-xs-lg btn-primary w-xs-40 w-25 mx-2"
                    ),
                    css_class='form-group col-24 text-center'
                )
            )
        )

    def clean_fdw_monthly_loan_repayment(self):
        fdw_monthly_loan_repayment = self.cleaned_data.get(
            'fdw_monthly_loan_repayment'
        )
        fdw_salary = self.cleaned_data.get(
            'fdw_salary'
        )
        if fdw_monthly_loan_repayment >= fdw_salary:
            self.add_error(
                'fdw_monthly_loan_repayment',
                ValidationError(
                    '''The FDW monthly loan repayment should be less than the
                    FDW basic salary''',
                    code='fdw_monthly_loan_repayment_error',
                )
            )
        return fdw_monthly_loan_repayment

    def save(self):
        if self.changed_data and self.form_type == 'UPDATE':
            strict_fields = [
                'case_ref_no',
                'agreement_date',
                'fdw_salary',
                'fdw_loan',
                'fdw_off_days',
                'fdw_off_day_of_week'
            ]
            if not set(strict_fields).isdisjoint(self.changed_data):
                self.instance.set_increment_version_number()
        return super().save()


class DocServiceFeeScheduleForm(forms.ModelForm):
    class Meta:
        model = DocServiceFeeSchedule
        exclude = [
            'employer_doc',
            'fdw_replaced_passport_nonce',
            'fdw_replaced_passport_tag',
            'ca_remaining_payment_amount'
        ]

    def __init__(self, *args, **kwargs):
        self.user_pk = kwargs.pop('user_pk')
        self.authority = kwargs.pop('authority')
        self.form_type = kwargs.pop('form_type')
        self.level_1_pk = kwargs.pop('level_1_pk')
        super().__init__(*args, **kwargs)

        passport_num = self.instance.get_fdw_replaced_passport_full()
        self.initial.update({
            'fdw_replaced_passport_num': passport_num
        })

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                """
                    <h5 class="doc-section-header"
                    id="id-doc-service-fee-schedule">
                    Service Fee Schedule
                    </h5>
                """),

            Row(
                Column(
                    'is_new_case',
                    css_class='form-group col-md-12 pr-md-3'
                )
            ),

            # Form B
            Row(
                Column(
                    Row(
                        Column(
                            'fdw_replaced_name',
                            css_class='form-group col-md-12 pr-md-3'
                        ),
                        Column(
                            'fdw_replaced_passport_num',
                            css_class='form-group col-md-12 pl-md-3'
                        )
                    ),
                    Row(
                        Column(
                            PrependedText(
                                'b4_loan_transferred', '$',
                                min='0', max='1000',
                            ),
                            css_class='form-group col-md-12 pr-md-3'
                        )
                    ),
                ),
                id="form_b",
            ),

            # Form A
            HTML(
                """
                <h6>1. Service Fee</h6>
            """),
            Row(
                Column(
                    PrependedText(
                        'b1_service_fee', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pr-md-3'
                )
            ),

            HTML(
                """
                <h6>2. Administrative Cost</h6>
            """),
            Row(
                Column(
                    PrependedText(
                        'b2a_work_permit_application_collection', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    PrependedText(
                        'b2b_medical_examination_fee', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    PrependedText(
                        'b2c_security_bond_accident_insurance', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    PrependedText(
                        'b2d_indemnity_policy_reimbursement', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    PrependedText(
                        'b2e_home_service', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    PrependedText(
                        'b2f_sip', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    'b2g1_other_services_description',
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    PrependedText(
                        'b2g1_other_services_fee', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    'b2g2_other_services_description',
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    PrependedText(
                        'b2g2_other_services_fee', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    'b2g3_other_services_description',
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    PrependedText(
                        'b2g3_other_services_fee', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    Row(
                        Column(
                            'b2h_replacement_months',
                            css_class='form-group col-md-12 pr-md-3'
                        ),
                        Column(
                            PrependedText(
                                'b2h_replacement_cost', '$',
                                min='0', max='1000',
                            ),
                            css_class='form-group col-md-12 pl-md-3'
                        )
                    ),
                    Row(
                        Column(
                            PrependedText(
                                'b2i_work_permit_renewal', '$',
                                min='0', max='1000',
                            ),
                            css_class='form-group col-md-12 pr-md-3'
                        )
                    ),
                ),
                id="b2j_b2k"
            ),

            HTML(
                """
                <h6>3. Placement Fee</h6>
            """),
            Row(
                Column(
                    PrependedText(
                        'b3_agency_fee', '$',
                        min='0', max='10000',
                    ),
                    css_class='form-group col-md-12 pr-md-3'
                )
            ),

            HTML(
                """
                <h6>4. Deposit</h6>
            """),
            Row(
                Column(
                    PrependedText(
                        'ca_deposit_amount', '$',
                        min='0', max='10000',
                    ),
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    Field(
                        'ca_deposit_detail'
                    ),
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),

            # Submit
            Row(
                Column(
                    HTML(
                        '''
                        <a href="{% url 'case_update_route' level_1_pk %}"
                        class="btn btn-xs-lg btn-outline-primary w-xs-40 w-25 mx-2">Back</a>
                        '''
                    ),
                    Submit(
                        'submit',
                        'Next',
                        css_class="btn btn-xs-lg btn-primary w-xs-40 w-25 mx-2"
                    ),
                    css_class='form-group col-24 text-center'
                )
            )
        )

    def clean_fdw_replaced_passport_num(self):
        cleaned_field = self.cleaned_data.get('fdw_replaced_passport_num')
        if cleaned_field:
            validate_passport("FDW", cleaned_field)
            ciphertext, nonce, tag = encrypt_string(
                cleaned_field,
                settings.ENCRYPTION_KEY
            )
            self.instance.fdw_replaced_passport_nonce = nonce
            self.instance.fdw_replaced_passport_tag = tag
            return ciphertext

    def clean_b4_loan_transferred(self):
        is_new_case = self.cleaned_data.get('is_new_case')
        cleaned_field = self.cleaned_data.get('b4_loan_transferred')

        if is_new_case:
            return cleaned_field
        elif not is_new_case and not cleaned_field:
            raise ValidationError('Loan being transferred is a required \
                field')
        else:
            return cleaned_field

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        fdw_replaced_passport_num = cleaned_data.get(
            'fdw_replaced_passport_num')
        is_new_case = cleaned_data.get('is_new_case')
        if not is_new_case and fdw_replaced_passport_num:
            error_msg = _('The replaced FDW passport number is required')
            raise ValidationError(error_msg)

    def save(self):
        if self.changed_data and self.form_type == 'UPDATE':
            strict_fields = [
                'is_new_case',
                'fdw_replaced_name',
                'fdw_replaced_passport_num',
                'fdw_replaced_passport_nonce',
                'fdw_replaced_passport_tag',
                'b4_loan_transferred',
                'b1_service_fee',
                'b2a_work_permit_application_collection',
                'b2b_medical_examination_fee',
                'b2c_security_bond_accident_insurance',
                'b2d_indemnity_policy_reimbursement',
                'b2e_home_service',
                'b2f_sip',
                'b2g1_other_services_description',
                'b2g1_other_services_fee',
                'b2g2_other_services_description',
                'b2g2_other_services_fee',
                'b2g3_other_services_description',
                'b2g3_other_services_fee',
                'b2h_replacement_months',
                'b2h_replacement_cost',
                'b2i_work_permit_renewal',
                'b3_agency_fee',
                'ca_deposit_amount',
                'ca_deposit_date'
            ]
            if not set(strict_fields).isdisjoint(self.changed_data):
                employer_doc_qs = EmployerDoc.objects.filter(
                    rn_servicefeeschedule_ed=self.instance
                )
                for employer_doc in employer_doc_qs:
                    employer_doc.set_increment_version_number()
        return super().save()


class DocServAgmtEmpCtrForm(forms.ModelForm):
    class Meta:
        model = DocServAgmtEmpCtr
        exclude = ['employer_doc']

    def __init__(self, *args, **kwargs):
        self.user_pk = kwargs.pop('user_pk')
        self.authority = kwargs.pop('authority')
        self.form_type = kwargs.pop('form_type')
        self.level_1_pk = kwargs.pop('level_1_pk')
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Service Agreement
            HTML(
                """
                    <h5 class="doc-section-header"
                    id="id-doc-service-agreement">
                    Service Agreement</h5>
                """),
            Row(
                Column(
                    'c1_3_handover_days',
                    css_class='form-group col-md-12 pr-md-3'
                )
            ),
            Row(
                Column(
                    'c3_2_no_replacement_criteria_1',
                    css_class='form-group col'
                )
            ),
            Row(
                Column(
                    'c3_2_no_replacement_criteria_2',
                    css_class='form-group col'
                )
            ),
            Row(
                Column(
                    'c3_2_no_replacement_criteria_3',
                    css_class='form-group col'
                )
            ),
            Row(
                Column(
                    PrependedText(
                        'c3_4_no_replacement_refund', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pr-md-3'
                )
            ),

            Row(
                Column(
                    'c4_1_number_of_replacements',
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    'c4_1_replacement_period',
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    'c4_1_replacement_after_min_working_days',
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    'c4_1_5_replacement_deadline',
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),

            Row(
                Column(
                    'c5_1_1_deployment_deadline',
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    PrependedText(
                        'c5_1_1_failed_deployment_refund', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    'c5_1_2_refund_within_days',
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    PrependedText(
                        'c5_1_2_before_fdw_arrives_charge', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    PrependedText(
                        'c5_1_2_after_fdw_arrives_charge', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    'c5_2_2_can_transfer_refund_within',
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    'c5_3_2_cannot_transfer_refund_within',
                    css_class='form-group col-md-12 pr-md-3'
                )
            ),

            Row(
                Column(
                    PrependedText(
                        'c6_4_per_day_food_accommodation_cost', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    PrependedText(
                        'c6_6_per_session_counselling_cost', '$',
                        min='0', max='1000',
                    ),
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),

            Row(
                Column(
                    'c9_1_independent_mediator_1',
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    'c9_2_independent_mediator_2',
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),

            Row(
                Column(
                    'c13_termination_notice',
                    css_class='form-group col-md-12 pr-md-3'
                )
            ),

            # Employment Contract
            HTML(
                """
                    <h5 class="doc-section-header"
                        id="id-doc-employment-contract">
                        Employment Contract</h5>
                """),
            Row(
                Column(
                    'c3_5_fdw_sleeping_arrangement',
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    'c4_1_termination_notice',
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),

            # Submit
            Row(
                Column(
                    HTML(
                        '''
                        <a
                        href="{% url 'servicefee_create_route' level_1_pk %}"
                        class="btn btn-xs-lg btn-outline-primary w-xs-40 w-25 mx-2">Back</a>
                        '''
                    ),
                    Submit(
                        'submit',
                        'Next',
                        css_class="btn btn-xs-lg btn-primary w-xs-40 w-25 mx-2"
                    ),
                    css_class='form-group col-24 text-center'
                )
            )
        )

    def save(self):
        if self.changed_data and self.form_type == 'UPDATE':
            strict_fields = [
                'c1_3_handover_days',
                'c3_2_no_replacement_criteria_1',
                'c3_2_no_replacement_criteria_2',
                'c3_2_no_replacement_criteria_3',
                'c3_4_no_replacement_refund',
                'c4_1_number_of_replacements',
                'c4_1_replacement_period',
                'c4_1_replacement_after_min_working_days',
                'c4_1_5_replacement_deadline',
                'c5_1_1_deployment_deadline',
                'c5_1_1_failed_deployment_refund',
                'c5_1_2_refund_within_days',
                'c5_1_2_before_fdw_arrives_charge',
                'c5_1_2_after_fdw_arrives_charge',
                'c5_2_2_can_transfer_refund_within',
                'c5_3_2_cannot_transfer_refund_within',
                'c6_4_per_day_food_accommodation_cost',
                'c6_6_per_session_counselling_cost',
                'c9_1_independent_mediator_1',
                'c9_2_independent_mediator_2',
                'c13_termination_notice',
                'c3_5_fdw_sleeping_arrangement',
                'c4_1_termination_notice'
            ]
            if not set(strict_fields).isdisjoint(self.changed_data):
                employer_doc_qs = EmployerDoc.objects.filter(
                    rn_serviceagreement_ed=self.instance
                )
                for employer_doc in employer_doc_qs:
                    employer_doc.set_increment_version_number()
        return super().save()


class DocSafetyAgreementForm(forms.ModelForm):
    class Meta:
        model = DocSafetyAgreement
        exclude = ['employer_doc']

    def __init__(self, *args, **kwargs):
        self.user_pk = kwargs.pop('user_pk')
        self.authority = kwargs.pop('authority')
        self.form_type = kwargs.pop('form_type')
        self.level_1_pk = kwargs.pop('level_1_pk')
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                """
                    <h5 class="doc-section-header"
                        id="id-doc-safety-agreement">Safety Agreement</h5>
                """),
            Row(
                Column(
                    'residential_dwelling_type',
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    'fdw_clean_window_exterior',
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    'window_exterior_location',
                    css_class='form-group col-md-12 pr-md-3 d-none'
                ),
                Column(
                    'grilles_installed_require_cleaning',
                    css_class='form-group col-md-12 pl-md-3 d-none'
                )
            ),
            Row(
                Column(
                    'adult_supervision',
                    css_class='form-group col-md-12 pr-md-3 d-none'
                ),
                Column(
                    'verifiy_employer_understands_window_cleaning',
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),

            # Submit
            Row(
                Column(
                    HTML(
                        '''
                        <a
                        href="{% url 'case_status_update_route' level_1_pk %}"
                        class="btn btn-xs-lg btn-outline-primary w-xs-40 w-25 mx-2">Back</a>
                        '''
                    ),
                    Submit(
                        'submit',
                        'Next',
                        css_class="btn btn-xs-lg btn-primary w-xs-40 w-25 mx-2"
                    ),
                    css_class='form-group col-24 text-center'
                )
            )
        )

    def clean(self):
        DSA = DocSafetyAgreement
        w_s_l_verbose_name = DSA._meta.get_field(
            'window_exterior_location'
        ).verbose_name
        window_exterior_error_msg = (
            w_s_l_verbose_name + ' field cannot be blank'
        )
        if (
            self.cleaned_data.get('fdw_clean_window_exterior')
            and not self.cleaned_data.get('window_exterior_location')
        ):
            self.add_error(
                'window_exterior_location',
                ValidationError(
                    window_exterior_error_msg,
                    code='error_window_exterior_location',
                    params={
                        'window_exterior_location': w_s_l_verbose_name
                    },
                )
            )

        g_l_verbose_name = DSA._meta.get_field(
            'grilles_installed_require_cleaning'
        ).verbose_name
        grilles_installed_error_msg = (
            g_l_verbose_name + ' field cannot be blank'
        )
        if (
            self.cleaned_data.get('window_exterior_location') == 'OTHER'
            and not self.cleaned_data.get('grilles_installed_require_cleaning')
        ):
            self.add_error(
                'grilles_installed_require_cleaning',
                ValidationError(
                    grilles_installed_error_msg,
                    code='error_grilles_installed_require_cleaning',
                    params={
                        'grilles_installed_require_cleaning': g_l_verbose_name
                    },
                )
            )

        adult_supervision_verbose_name = DSA._meta.get_field(
            'adult_supervision'
        ).verbose_name
        adult_supervision_error_msg = '''
            Adult supervision is required if grilles installed on windows are
            to be cleaned by FDW
        '''
        if (
            self.cleaned_data.get('grilles_installed_require_cleaning')
            and not self.cleaned_data.get('adult_supervision')
        ):
            self.add_error(
                'adult_supervision',
                ValidationError(
                    adult_supervision_error_msg,
                    code='error_adult_supervision',
                    params={
                        'adult_supervision': adult_supervision_verbose_name
                    },
                )
            )

        verifiy_employer_understands_verbose_name = DSA._meta.get_field(
            'verifiy_employer_understands_window_cleaning'
        ).verbose_name
        verifiy_employer_understands_error_msg = '''
            This field must correspond with previous fields
        '''
        w_e_l = self.cleaned_data.get('window_exterior_location')
        v_e_u_w_c = self.cleaned_data.get(
            'verifiy_employer_understands_window_cleaning'
        )
        if (
            (
                not self.cleaned_data.get('fdw_clean_window_exterior')
                and not self.cleaned_data.get(
                    'verifiy_employer_understands_window_cleaning'
                ) == 1
            )
            or w_e_l == 'GROUND' and not v_e_u_w_c == 2
            or w_e_l == 'COMMON' and not v_e_u_w_c == 3
            or w_e_l == 'OTHER' and not v_e_u_w_c == 4
            or (
                v_e_u_w_c == 1
                and self.cleaned_data.get('fdw_clean_window_exterior')
            )
            or v_e_u_w_c == 2 and not w_e_l == 'GROUND'
            or v_e_u_w_c == 3 and not w_e_l == 'COMMON'
            or v_e_u_w_c == 4 and not w_e_l == 'OTHER'
            or (
                v_e_u_w_c == 4
                and w_e_l == 'OTHER'
                and not self.cleaned_data.get(
                    'grilles_installed_require_cleaning'
                )
            )
        ):
            veu_v_n = verifiy_employer_understands_verbose_name
            self.add_error(
                'verifiy_employer_understands_window_cleaning',
                ValidationError(
                    verifiy_employer_understands_error_msg,
                    code='error_verifiy_employer_understands',
                    params={
                        'verifiy_employer_understands_window_cleaning': veu_v_n
                    },
                )
            )

        return self.cleaned_data

    def save(self):
        if self.changed_data and self.form_type == 'UPDATE':
            strict_fields = [
                'residential_dwelling_type',
                'fdw_clean_window_exterior',
                'window_exterior_location',
                'grilles_installed_require_cleaning',
                'adult_supervision',
                'verifiy_employer_understands_window_cleaning'
            ]
            if not set(strict_fields).isdisjoint(self.changed_data):
                employer_doc_qs = EmployerDoc.objects.filter(
                    rn_safetyagreement_ed=self.instance
                )
                for employer_doc in employer_doc_qs:
                    employer_doc.set_increment_version_number()
        return super().save()


class RemainingAmountDetailForm(forms.ModelForm):
    class Meta:
        model = DocServiceFeeSchedule
        fields = [
            'ca_remaining_payment_detail',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                """
                    <h5 class="fs-14">Remaining Amount Details</h5>
                """),
            Row(
                Column(
                    'ca_remaining_payment_detail'
                ),
            ),

            # Submit
            Row(
                Column(
                    Submit(
                        'submit',
                        'Submit',
                        css_class="btn btn-xs-lg btn-primary w-xs-40 w-25 mx-2"
                    ),
                    css_class='form-group col-24 text-center'
                )
            )
        )

# Temporary solution to blank out S3 bucket URL


class CustomClearableFileInput(ClearableFileInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['is_initial'] = False
        return context


class DocUploadForm(forms.ModelForm):
    class Meta:
        model = DocUpload
        exclude = ['employer_doc']

    def __init__(self, *args, **kwargs):
        self.user_pk = kwargs.pop('user_pk')
        self.authority = kwargs.pop('authority')
        self.level_1_pk = kwargs.pop('level_1_pk')
        super().__init__(*args, **kwargs)

        # Temporary solution to blank out S3 bucket URL
        self.fields['job_order_pdf'].widget = CustomClearableFileInput()
        self.fields['ipa_pdf'].widget = CustomClearableFileInput()
        self.fields['medical_report_pdf'].widget = CustomClearableFileInput()

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                """
                <h5 class="doc-section-header"
                    id="id-doc-upload">
                    Upload Documents
                </h5>
            """),
            Row(
                Column(
                    'job_order_pdf',
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    'ipa_pdf',
                    css_class='form-group col-md-12 pl-md-3'
                )
            ),
            Row(
                Column(
                    'medical_report_pdf',
                    css_class='form-group col-md-12 pr-md-3'
                )
            ),

            # Submit
            Row(
                Column(
                    HTML(
                        '''
                        <a href="{% url 'safetyagreement_create_route' level_1_pk %}"
                        class="btn btn-xs-lg btn-outline-primary w-xs-40 w-25 mx-2">Back</a>
                        '''
                    ),
                    Submit(
                        'submit',
                        'Submit',
                        css_class="btn btn-xs-lg btn-primary w-xs-40 w-25 mx-2"
                    ),
                    css_class='form-group col-24 text-center'
                )
            )
        )


class CaseStatusForm(forms.ModelForm):
    class Meta:
        model = CaseStatus
        exclude = ['employer_doc']

    def __init__(self, *args, **kwargs):
        self.user_pk = kwargs.pop('user_pk')
        self.authority = kwargs.pop('authority')
        self.level_1_pk = kwargs.pop('level_1_pk')
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                '''
                    <h3>Case Status</h3>
                '''
            ),
            Row(
                Column(
                    Field(
                        'ipa_approval_date',
                        type='text',
                        onfocus="(this.type='date')",
                        placeholder='IPA approval date'
                    ),
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    Field(
                        'arrival_date',
                        type='text',
                        onfocus="(this.type='date')",
                        placeholder='FDW arrival date'
                    ),
                    css_class='form-group col-md-12 pl-md-3'
                ),
                Column(
                    Field(
                        'shn_end_date',
                        type='text',
                        onfocus="(this.type='date')",
                        placeholder='Security bond approval date'
                    ),
                    css_class='form-group col-md-12 pr-md-3'
                ),
                Column(
                    Field(
                        'thumb_print_date',
                        type='text',
                        onfocus="(this.type='date')",
                        placeholder='Thumb print date'
                    ),
                    css_class='form-group col-md-12 pl-md-3'
                ),
                Column(
                    Field(
                        'fdw_work_commencement_date',
                        type='text',
                        onfocus="(this.type='date')",
                        placeholder='FDW work commencement date'
                    ),
                    css_class='form-group col-md-12 pr-md-3'
                )
            ),
            Row(
                Column(
                    HTML(
                        '''
                        <a href="{% url 'serviceagreement_create_route' level_1_pk %}"
                        class="btn btn-xs-lg btn-outline-primary w-xs-40 w-25 mx-2">Back</a>
                        '''
                    ),
                    Submit(
                        'submit',
                        'Next',
                        css_class="btn btn-xs-lg btn-primary w-xs-40 w-25 mx-2"
                    ),
                    css_class='form-group col-24 text-center'
                )
            )
        )

# Signature Forms


class SignatureForm(forms.ModelForm):
    class Meta:
        model = CaseSignature
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Assign model_field_name in urls.py or views.py
        self.model_field_name = kwargs.pop('model_field_name')
        self.form_fields = kwargs.pop('form_fields')
        super().__init__(*args, **kwargs)

        # Make copy of all field names, then remove fields that are not
        # in self.form_fields.
        fields_copy = list(self.fields)
        for field in fields_copy:
            if field not in self.form_fields:
                del self.fields[field]

        # Instantiate blank Layout instance
        self.helper = FormHelper()
        self.helper.form_class = 'employer-docsig-form'
        self.helper.layout = Layout()

        # Append form fields to Layout instance
        for field in self.fields:
            if field == self.model_field_name:
                self.helper.layout.append(
                    Hidden(
                        self.model_field_name,
                        self.model_field_name,
                        id='id_signature'
                    ),
                )
            else:
                self.helper.layout.append(
                    Row(
                        Column(field, css_class='form-group col-md-12')
                    )
                )

        # Signature pad
        self.helper.layout.append(
            Row(
                Column(
                    HTML("""
                        <canvas
                            id="signature-pad"
                            class=""
                            style="border: 1px solid #d2d2d2"
                        >
                        </canvas>
                    """)
                )
            )
        )
        # Label for signature pad
        self.helper.layout.append(
            Row(
                Column(
                    HTML("""
                        <h6>{{ model_field_verbose_name }}</h6>
                    """)
                )
            )
        )
        # Submit form and clear signature pad buttons
        self.helper.layout.append(
            Row(
                Column(
                    Submit("submit", "Submit"),
                    StrictButton(
                        "Clear",
                        onclick="signaturePad.clear()",
                        css_class="btn btn-xs-lg btn-secondary"
                    ),
                )
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        base64_sig = cleaned_data.get(self.model_field_name)
        if base64_sig is None:
            error_msg = "There was an issue uploading your signature, \
                please try again."
            raise ValidationError(error_msg)
        elif not base64_sig.startswith("data:image/png;base64,"):
            error_msg = "There was an issue uploading your signature, \
                please try again."
            raise ValidationError(error_msg)
        elif base64_sig == 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAACWCAYAAABkW7XSAAAAxUlEQVR4nO3BMQEAAADCoPVPbQhfoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOA1v9QAATX68/0AAAAASUVORK5CYII=':
            error_msg = "Signature cannot be blank"
            raise ValidationError(error_msg)
        elif base64_sig == 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAACWCAYAAABkW7XSAAAEYklEQVR4Xu3UAQkAAAwCwdm/9HI83BLIOdw5AgQIRAQWySkmAQIEzmB5AgIEMgIGK1OVoAQIGCw/QIBARsBgZaoSlAABg+UHCBDICBisTFWCEiBgsPwAAQIZAYOVqUpQAgQMlh8gQCAjYLAyVQlKgIDB8gMECGQEDFamKkEJEDBYfoAAgYyAwcpUJSgBAgbLDxAgkBEwWJmqBCVAwGD5AQIEMgIGK1OVoAQIGCw/QIBARsBgZaoSlAABg+UHCBDICBisTFWCEiBgsPwAAQIZAYOVqUpQAgQMlh8gQCAjYLAyVQlKgIDB8gMECGQEDFamKkEJEDBYfoAAgYyAwcpUJSgBAgbLDxAgkBEwWJmqBCVAwGD5AQIEMgIGK1OVoAQIGCw/QIBARsBgZaoSlAABg+UHCBDICBisTFWCEiBgsPwAAQIZAYOVqUpQAgQMlh8gQCAjYLAyVQlKgIDB8gMECGQEDFamKkEJEDBYfoAAgYyAwcpUJSgBAgbLDxAgkBEwWJmqBCVAwGD5AQIEMgIGK1OVoAQIGCw/QIBARsBgZaoSlAABg+UHCBDICBisTFWCEiBgsPwAAQIZAYOVqUpQAgQMlh8gQCAjYLAyVQlKgIDB8gMECGQEDFamKkEJEDBYfoAAgYyAwcpUJSgBAgbLDxAgkBEwWJmqBCVAwGD5AQIEMgIGK1OVoAQIGCw/QIBARsBgZaoSlAABg+UHCBDICBisTFWCEiBgsPwAAQIZAYOVqUpQAgQMlh8gQCAjYLAyVQlKgIDB8gMECGQEDFamKkEJEDBYfoAAgYyAwcpUJSgBAgbLDxAgkBEwWJmqBCVAwGD5AQIEMgIGK1OVoAQIGCw/QIBARsBgZaoSlAABg+UHCBDICBisTFWCEiBgsPwAAQIZAYOVqUpQAgQMlh8gQCAjYLAyVQlKgIDB8gMECGQEDFamKkEJEDBYfoAAgYyAwcpUJSgBAgbLDxAgkBEwWJmqBCVAwGD5AQIEMgIGK1OVoAQIGCw/QIBARsBgZaoSlAABg+UHCBDICBisTFWCEiBgsPwAAQIZAYOVqUpQAgQMlh8gQCAjYLAyVQlKgIDB8gMECGQEDFamKkEJEDBYfoAAgYyAwcpUJSgBAgbLDxAgkBEwWJmqBCVAwGD5AQIEMgIGK1OVoAQIGCw/QIBARsBgZaoSlAABg+UHCBDICBisTFWCEiBgsPwAAQIZAYOVqUpQAgQMlh8gQCAjYLAyVQlKgIDB8gMECGQEDFamKkEJEDBYfoAAgYyAwcpUJSgBAgbLDxAgkBEwWJmqBCVAwGD5AQIEMgIGK1OVoAQIGCw/QIBARsBgZaoSlAABg+UHCBDICBisTFWCEiBgsPwAAQIZAYOVqUpQAgQMlh8gQCAjYLAyVQlKgIDB8gMECGQEDFamKkEJEDBYfoAAgYyAwcpUJSgBAgbLDxAgkBEwWJmqBCVAwGD5AQIEMgIGK1OVoAQIGCw/QIBARsBgZaoSlACBB1YxAJfjJb2jAAAAAElFTkSuQmCC':
            error_msg = "Signature cannot be blank"
            raise ValidationError(error_msg)
        else:
            return cleaned_data


class ChallengeForm(forms.Form):
    nric_fin = forms.CharField(
        label='Last Four Characters of NRIC/FIN',
        max_length=4
    )
    mobile = forms.CharField(
        label='Mobile Phone Number',
        max_length=8
    )

    def __init__(self, *args, **kwargs):
        self.object = kwargs.pop('object')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'nric_fin',
                    css_class='form-group col-md-18 my-2',
                ),
                Column(
                    'mobile',
                    css_class='form-group col-md-18 my-2',
                ),
                Column(
                    Submit(
                        'submit',
                        'Confirm',
                        css_class="btn btn-xs-lg btn-primary w-75",
                    ),
                    css_class='form-group col-md-18 my-3 text-center',
                )
            )
        )

    def clean_nric_fin(self):
        cleaned_field = self.cleaned_data.get('nric_fin', '').upper()
        valid = False
        obj = self.object.employer
        if is_local(obj.employer_residential_status):
            if cleaned_field == obj.get_employer_nric_partial(
                padded=False
            ):
                valid = True
        else:
            if cleaned_field == obj.get_employer_fin_partial(padded=False):
                valid = True

        return cleaned_field if valid else None

    def clean_mobile(self):
        cleaned_field = self.cleaned_data.get('mobile')
        valid = False
        obj = self.object.employer
        if cleaned_field == obj.employer_mobile_number:
            valid = True

        return cleaned_field if valid else None

    def clean(self):
        cleaned_data = super().clean()
        nric_fin = cleaned_data.get('nric_fin')
        mobile = cleaned_data.get('mobile')

        if nric_fin and mobile:
            return cleaned_data
        else:
            error_msg = _('Invalid Credentials')
            raise ValidationError(
                error_msg,
                code='invalid',
            )


class EmployerSignatureForm(forms.Form):
    employer_signature = forms.CharField(
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column(
                            'employer_signature'
                        )
                    ),
                    Row(
                        Column(
                            HTML(
                                """
                                <h6>Employer Signature</h6>
                                <canvas
                                    id="employer-signature-pad"
                                    class=""
                                    style="border: 1px solid #d2d2d2"
                                >
                                </canvas>
                                """
                            )
                        )
                    ),
                    Row(
                        Column(
                            Button(
                                'Clear Signatures',
                                'Clear Signatures',
                                css_class='''
                                    btn btn-xs-lg btn-outline-secondary w-xs-100 w-25 mr-2
                                ''',
                                css_id='signature-form-clear-button'
                            ),
                            Button(
                                'Confirm',
                                'Confirm',
                                css_class='btn btn-xs-lg btn-primary w-25 ml-2 w-xs-100',
                                css_id='signature-form-submit-button'
                            ),
                            css_class='d-flex justify-content-center mt-4'
                        )
                    )
                ),
                css_class='form-group'
            )
        )


class EmployerWithSpouseSignatureForm(forms.Form):
    employer_signature = forms.CharField(
        widget=forms.HiddenInput()
    )
    employer_spouse_signature = forms.CharField(
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column(
                            'employer_signature'
                        )
                    ),
                    Row(
                        Column(
                            HTML(
                                """
                                <h6>Employer Signature</h6>
                                <canvas
                                    id="employer-signature-pad"
                                    class=""
                                    style="border: 1px solid #d2d2d2"
                                >
                                </canvas>
                                """
                            )
                        )
                    )
                ),
                Column(
                    Row(
                        Column(
                            'employer_spouse_signature'
                        )
                    ),
                    Row(
                        Column(
                            HTML(
                                """
                                <h6>Employer Spouse Signature</h6>
                                <canvas
                                    id="employer-spouse-signature-pad"
                                    class=""
                                    style="border: 1px solid #d2d2d2"
                                >
                                </canvas>
                                """
                            )
                        )
                    )
                ),
                css_class='form-group'
            ),
            Row(
                Column(
                    Button(
                        'Clear Signatures',
                        'Clear Signatures',
                        css_class='btn btn-xs-lg btn-outline-secondary w-25 mr-2 w-xs-100',
                        css_id='signature-form-clear-button'
                    ),
                    Button(
                        'Confirm',
                        'Confirm',
                        css_class='btn btn-xs-lg btn-primary w-25 ml-2 w-xs-100',
                        css_id='signature-form-submit-button'
                    ),
                    css_class='d-flex justify-content-center mt-4'
                )
            )
        )


class EmployerWithOneSponsorSignatureForm(forms.Form):
    employer_signature = forms.CharField(
        widget=forms.HiddenInput()
    )
    employer_sponsor1_signature = forms.CharField(
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column(
                            'employer_signature'
                        )
                    ),
                    Row(
                        Column(
                            HTML(
                                """
                                <h6>Employer Signature</h6>
                                <canvas
                                    id="employer-signature-pad"
                                    class=""
                                    style="border: 1px solid #d2d2d2"
                                >
                                </canvas>
                                """
                            )
                        )
                    )
                ),
                Column(
                    Row(
                        Column(
                            'employer_sponsor1_signature'
                        )
                    ),
                    Row(
                        Column(
                            HTML(
                                """
                                <h6>Sponsor Signature</h6>
                                <canvas
                                    id="sponsor-1-signature-pad"
                                    class=""
                                    style="border: 1px solid #d2d2d2"
                                >
                                </canvas>
                                """
                            )
                        )
                    ),
                ),
                css_class='form-group'
            ),
            Row(
                Column(
                    Button(
                        'Clear Signatures',
                        'Clear Signatures',
                        css_class='btn btn-xs-lg btn-outline-secondary w-25 mr-2 w-xs-100',
                        css_id='signature-form-clear-button'
                    ),
                    Button(
                        'Confirm',
                        'Confirm',
                        css_class='btn btn-xs-lg btn-primary w-25 ml-2 w-xs-100',
                        css_id='signature-form-submit-button'
                    ),
                    css_class='d-flex justify-content-center mt-4'
                )
            )
        )


class EmployerWithTwoSponsorSignatureForm(forms.Form):
    employer_signature = forms.CharField(
        widget=forms.HiddenInput()
    )
    employer_sponsor1_signature = forms.CharField(
        widget=forms.HiddenInput()
    )
    employer_sponsor2_signature = forms.CharField(
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column(
                            'employer_signature'
                        )
                    ),
                    Row(
                        Column(
                            HTML(
                                """
                                <h6>Employer Signature</h6>
                                <canvas
                                    id="employer-signature-pad"
                                    class=""
                                    style="border: 1px solid #d2d2d2"
                                >
                                </canvas>
                                """
                            )
                        )
                    )
                ),
                Column(
                    Row(
                        Column(
                            'employer_sponsor1_signature'
                        )
                    ),
                    Row(
                        Column(
                            HTML(
                                """
                                <h6>Sponsor 1 Signature</h6>
                                <canvas
                                    id="sponsor-1-signature-pad"
                                    class=""
                                    style="border: 1px solid #d2d2d2"
                                >
                                </canvas>
                                """
                            )
                        )
                    ),
                ),
                Column(
                    Row(
                        Column(
                            'employer_sponsor2_signature'
                        )
                    ),
                    Row(
                        Column(
                            HTML(
                                """
                                <h6>Sponsor 2 Signature</h6>
                                <canvas
                                    id="sponsor-2-signature-pad"
                                    class=""
                                    style="border: 1px solid #d2d2d2"
                                >
                                </canvas>
                                """
                            )
                        )
                    ),
                ),
                css_class='form-group'
            ),
            Row(
                Column(
                    Button(
                        'Clear Signatures',
                        'Clear Signatures',
                        css_class='btn btn-xs-lg btn-outline-secondary w-25 mr-2 w-xs-100',
                        css_id='signature-form-clear-button'
                    ),
                    Button(
                        'Confirm',
                        'Confirm',
                        css_class='btn btn-xs-lg btn-primary w-25 ml-2 w-xs-100',
                        css_id='signature-form-submit-button'
                    ),
                    css_class='d-flex justify-content-center mt-4'
                )
            )
        )


class EmployerWithJointApplicantSignatureForm(forms.Form):
    employer_signature = forms.CharField(
        widget=forms.HiddenInput()
    )

    joint_applicant_signature = forms.CharField(
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column(
                            'employer_signature'
                        )
                    ),
                    Row(
                        Column(
                            HTML(
                                """
                                <h6>Employer Signature</h6>
                                <canvas
                                    id="employer-signature-pad"
                                    class=""
                                    style="border: 1px solid #d2d2d2"
                                >
                                </canvas>
                                """
                            )
                        )
                    )
                ),
                Column(
                    Row(
                        Column(
                            'joint_applicant_signature'
                        )
                    ),
                    Row(
                        Column(
                            HTML(
                                """
                                <h6>Joint Applicant Signature</h6>
                                <canvas
                                    id="joint-application-signature-pad"
                                    class=""
                                    style="border: 1px solid #d2d2d2"
                                >
                                </canvas>
                                """
                            )
                        )
                    )
                ),
                css_class='form-group'
            ),
            Row(
                Column(
                    Button(
                        'Clear Signatures',
                        'Clear Signatures',
                        css_class='btn btn-xs-lg btn-outline-secondary w-25 mr-2 w-xs-100',
                        css_id='signature-form-clear-button'
                    ),
                    Button(
                        'Confirm',
                        'Confirm',
                        css_class='btn btn-xs-lg btn-primary w-25 ml-2 w-xs-100',
                        css_id='signature-form-submit-button'
                    ),
                    css_class='d-flex justify-content-center mt-4'
                )
            )
        )


class HandoverSignatureForm(forms.Form):
    agency_employee_signature = forms.CharField(
        widget=forms.HiddenInput()
    )
    employer_signature = forms.CharField(
        widget=forms.HiddenInput()
    )
    fdw_signature = forms.CharField(
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column(
                            'employer_signature'
                        )
                    ),
                    Row(
                        Column(
                            HTML(
                                """
                                <h6>Employer Signature</h6>
                                <canvas
                                    id="employer-signature-pad"
                                    class=""
                                    style="border: 1px solid #d2d2d2"
                                >
                                </canvas>
                                """
                            )
                        )
                    )
                ),
                Column(
                    Row(
                        Column(
                            'agency_employee_signature'
                        )
                    ),
                    Row(
                        Column(
                            HTML(
                                """
                                <h6>Agency Employee Signature</h6>
                                <canvas
                                    id="agency-employee-signature-pad"
                                    class=""
                                    style="border: 1px solid #d2d2d2"
                                >
                                </canvas>
                                """
                            )
                        )
                    )
                ),
                Column(
                    Row(
                        Column(
                            'fdw_signature'
                        )
                    ),
                    Row(
                        Column(
                            HTML(
                                """
                                <h6>Maid Signature</h6>
                                <canvas
                                    id="fdw-signature-pad"
                                    class=""
                                    style="border: 1px solid #d2d2d2"
                                >
                                </canvas>
                                """
                            )
                        )
                    )
                )
            ),
            Row(
                Column(
                    Button(
                        'Clear Signatures',
                        'Clear Signatures',
                        css_class='btn btn-xs-lg btn-outline-secondary w-25 mr-2 w-xs-100',
                        css_id='signature-form-clear-button'
                    ),
                    Button(
                        'Confirm',
                        'Confirm',
                        css_class='btn btn-xs-lg btn-primary w-25 ml-2 w-xs-100',
                        css_id='signature-form-submit-button'
                    ),
                    css_class='d-flex justify-content-center mt-4'
                )
            )
        )
