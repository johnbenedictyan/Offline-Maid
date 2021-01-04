# Imports from django
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _

# Imports from foreign installed apps
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Hidden
from onlinemaid.constants import (
    AG_OWNERS, AG_ADMINS, AG_MANAGERS, AG_SALES, P_EMPLOYERS
)

# Imports from local apps
from .managers import CustomUserManager
from .models import Employer, User

# Start of Forms

# Forms that inherit from inbuilt Django forms
class SignInForm(AuthenticationForm):
    # This is done because the success_url in the loginview does not seem
    # to override the default settings.login_redirect_url which is
    # accounts.profile

    # Will need to see if this affects the next url when passed in from a 
    # mixin like login required

    # We cannot have it to be a static redirect, the next url must take
    # precedence
    redirect_named_url = 'home'

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'username',
                    css_class='form-group col-12'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'password',
                    css_class='form-group col-12'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Hidden(
                        'next',
                        f"{{% url '{self.redirect_named_url}' %}}"
                    )
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit',
                        'Sign In',
                        css_class="btn btn-primary w-50"
                    ),
                    css_class='form-group col-12 text-center'
                ),
                css_class='form-row'
            ),
        )

class AgencySignInForm(AuthenticationForm):
    # This is done because the success_url in the loginview does not seem
    # to override the default settings.login_redirect_url which is
    # accounts.profile

    # Will need to see if this affects the next url when passed in from a 
    # mixin like login required

    # We cannot have it to be a static redirect, the next url must take
    # precedence
    redirect_named_url = 'dashboard_home'

    agency_license_number = forms.CharField(
        label=_('Agency License Number'),
        required=True,
        max_length=255,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'agency_license_number',
                    css_class='form-group col-12'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'username',
                    css_class='form-group col-12'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'password',
                    css_class='form-group col-12'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Hidden(
                        'next',
                        f"{{% url '{self.redirect_named_url}' %}}"
                    )
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit',
                        'Sign In',
                        css_class="btn btn-primary w-50"
                    ),
                    css_class='form-group col-12 text-center'
                ),
                css_class='form-row'
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        user = get_user_model().objects.get(
            email = cleaned_data.get('username')
        )

        if user.groups.filter(name=P_EMPLOYERS).exists():
            self.add_error(
                'username',
                ValidationError(
                    _('Invalid Agency Staff Email'),
                    code='invalid-signin'
                )
            )

        if user.groups.filter(name=AG_OWNERS).exists():
            agency = user.agency_owner.agency
        else:
            agency = user.agency_employee.agency

        if agency.license_number != cleaned_data.get('agency_license_number'):
            self.add_error(
                'agency_license_number',
                ValidationError(
                    _('Invalid Agency License Number'),
                    code='invalid-signin'
                )
            )
        return cleaned_data

# Model Forms
class EmployerCreationForm(forms.ModelForm):
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
        model = Employer
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
                    'first_name',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'last_name',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'contact_number',
                    css_class='form-group col'
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
                password=cleaned_data.get('password')
            )
        except Exception as e:
            pass
        else:
            potential_employer_group = Group.objects.get(
                name='Potential Employers'
            ) 
            potential_employer_group.user_set.add(
                new_user
            )
            self.instance.user = new_user
            return super().save(*args, **kwargs)

# Generic Forms (forms.Form)