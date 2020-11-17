# Imports from django
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _

# Imports from foreign installed apps
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

# Imports from local apps
from .models import (
    Agency, AgencyEmployee, AgencyBranch, AgencyOperatingHours, AgencyPlan,
    AgencyAdministrator
)

# Start of Forms

# Forms that inherit from inbuilt Django forms

# Model Forms
class AgencyCreationForm(forms.ModelForm):
    email = forms.CharField(
        label=_('Email Address'),
        required=True,
        max_length=255
    )

    password = forms.CharField(
        label=_('Password'),
        required=True,
        max_length=255,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = Agency
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'email',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'password',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'name',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'license_number',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'company_email',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'sales_email',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'uen',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'website_uri',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit',
                        'Create',
                        css_class="btn btn-primary w-50"
                    ),
                    css_class='form-group col-12 text-center'
                ),
                css_class='form-row'
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        UserModel = get_user_model()
        try:
            UserModel.objects.get(
                email=email
            )
        except UserModel.DoesNotExist:
            pass
        else:
            msg = _('This email is taken')
            self.add_error('email', msg)

        if validate_password(password):
            msg = _('This password does not meet our requirements')
            self.add_error('password', msg)

        return cleaned_data

    def save(self, *args, **kwargs):
        cleaned_data = super().clean()
        try:
            new_user = get_user_model().objects.create_user(
                email=cleaned_data.get('email'),
                password=cleaned_data.get('password'),
                role='A'
            )
        except Exception as e:
            pass
        else:
            agency_group = Group.objects.get(
                name='Agencies'
            ) 
            agency_group.user_set.add(
                new_user
            )
            self.instance.user = new_user
            return super().save(*args, **kwargs)

class AgencyEmployeeCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label=_('Email Address'),
        required=True
    )

    password = forms.CharField(
        label=_('Password'),
        required=True,
        max_length=255,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = AgencyEmployee
        exclude = ['agency','user']

    def __init__(self, *args, **kwargs):
        # Limit the choices of the foreign key branch to just the branches
        # under the current agency
        agency_id = kwargs.pop('agency_id')
        super().__init__(*args, **kwargs)
        self.fields['branch'].queryset = AgencyBranch.objects.filter(
            agency = Agency.objects.get(
                pk = agency_id
            )
        )
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'email',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'password',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'first_name',
                    css_class='form-group col-md-4'
                ),
                Column(
                    'last_name',
                    css_class='form-group col-md-4'
                ),
                Column(
                    'contact_number',
                    css_class='form-group col-md-4'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'ea_personnel_number',
                    css_class='form-group col-md-4'
                ),
                Column(
                    'branch',
                    css_class='form-group col-md-4'
                ),
                Column(
                    'role',
                    css_class='form-group col-md-4'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit',
                        'Submit',
                        css_class="btn btn-primary w-50"
                    ),
                    css_class='form-group col-12 text-center'
                ),
                css_class='form-row'
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(
                email=email
            )
        except UserModel.DoesNotExist:
            pass
        else:
            if hasattr(user, 'agency'):
                msg = _('This user is already part of an agency')
            else:
                msg = _('This email is taken by an employer')
            self.add_error('email', msg)

        if validate_password(password):
            msg = _('This password does not meet our requirements')
            self.add_error('password', msg)
            
        return cleaned_data

    def save(self, *args, **kwargs):
        # There is a cleaner way to write this save method
        cleaned_data = self.cleaned_data
        try:
            new_user = get_user_model().objects.create_user(
                email=cleaned_data.get('email'),
                password=cleaned_data.get('password'),
                role='AE'
            )
        except Exception as e:
            pass
        else:
            agency_employee_group = Group.objects.get(
                name='Agency Employees'
            ) 
            agency_employee_group.user_set.add(
                new_user
            )

            self.instance.user = new_user
            self.instance.first_name = cleaned_data.get('first_name')
            self.instance.last_name = cleaned_data.get('last_name')
            self.instance.contact_number = cleaned_data.get(
                'contact_number'
            )
            self.instance.ea_personnel_number = cleaned_data.get(
                'ea_personnel_number'
            )
            self.instance.branch = cleaned_data.get('branch')

            return super().save(*args, **kwargs)

class AgencyAdministratorCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label=_('Email Address'),
        required=True
    )

    password = forms.CharField(
        label=_('Password'),
        required=True,
        max_length=255,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = AgencyAdministrator
        exclude = ['agency','user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'email',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'password',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'first_name',
                    css_class='form-group col-md-4'
                ),
                Column(
                    'last_name',
                    css_class='form-group col-md-4'
                ),
                Column(
                    'contact_number',
                    css_class='form-group col-md-4'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'ea_personnel_number',
                    css_class='form-group col'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit',
                        'Submit',
                        css_class="btn btn-primary w-50"
                    ),
                    css_class='form-group col-12 text-center'
                ),
                css_class='form-row'
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(
                email=email
            )
        except UserModel.DoesNotExist:
            pass
        else:
            if hasattr(user, 'agency'):
                msg = _('This user is already part of an agency')
            else:
                msg = _('This email is taken by an employer')
            self.add_error('email', msg)

        if validate_password(password):
            msg = _('This password does not meet our requirements')
            self.add_error('password', msg)
            
        return cleaned_data

    def save(self, *args, **kwargs):
        # There is a cleaner way to write this save method
        cleaned_data = self.cleaned_data
        try:
            new_user = get_user_model().objects.create_user(
                email=cleaned_data.get('email'),
                password=cleaned_data.get('password'),
                role='AA'
            )
        except Exception as e:
            pass
        else:
            agency_employee_group = Group.objects.get(
                name='Agency Administrators'
            ) 
            agency_employee_group.user_set.add(
                new_user
            )

            self.instance.user = new_user
            self.instance.first_name = cleaned_data.get('first_name')
            self.instance.last_name = cleaned_data.get('last_name')
            self.instance.contact_number = cleaned_data.get(
                'contact_number'
            )
            self.instance.ea_personnel_number = cleaned_data.get(
                'ea_personnel_number'
            )

            return super().save(*args, **kwargs)

class AgencyBranchForm(forms.ModelForm):
    class Meta:
        model = AgencyBranch
        exclude = ['agency']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'name',
                    css_class='form-group col'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'address_1',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'address_2',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'postal_code',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'area',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'office_number',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'mobile_number',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit',
                        'Submit',
                        css_class="btn btn-primary w-50"
                    ),
                    css_class='form-group col-12 text-center'
                ),
                css_class='form-row'
            )
        )

class AgencyOperatingHoursForm(forms.ModelForm):
    class Meta:
        model = AgencyOperatingHours
        exclude = ['agency']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'operating_type',
                    css_class='form-group col'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'monday',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'tuesday',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'wednesday',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'thursday',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'friday',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'saturday',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'sunday',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'public_holiday',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit',
                        'Submit',
                        css_class="btn btn-primary w-50"
                    ),
                    css_class='form-group col-12 text-center'
                ),
                css_class='form-row'
            )
        )

class AgencyPlanForm(forms.ModelForm):
    class Meta:
        model = AgencyPlan
        exclude = ['agency']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'choice',
                    css_class='form-group col'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit',
                        'Purchase',
                        css_class="btn btn-primary w-50"
                    ),
                    css_class='form-group col-12 text-center'
                ),
                css_class='form-row'
            )
        )

# Generic Forms (forms.Form)