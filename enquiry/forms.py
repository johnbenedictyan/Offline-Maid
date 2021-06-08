# Imports from django
from django import forms
from django.utils.translation import ugettext_lazy as _

# Imports from foreign installed apps
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV3
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Submit, Row, Column, Field
from maid.models import MaidResponsibility, MaidLanguage

# Imports from local apps
from .fields import MaidResponsibilityChoiceField
from .models import GeneralEnquiry, ShortlistedEnquiry

# Start of Forms

# Forms that inherit from inbuilt Django forms

# Model Forms

class GeneralEnquiryForm(forms.ModelForm):
    maid_responsibility = MaidResponsibilityChoiceField(
        queryset=MaidResponsibility.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    languages_spoken = forms.ModelMultipleChoiceField(
        queryset=MaidLanguage.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
    
    consent = forms.BooleanField(
        label="""
            By submitting this enquiry form, I consent to the collection, 
            use and disclosure of my personal data by Online Maid Pte Ltd to
            agencies that are listed on this platform.
        """
    )

    # captcha = ReCaptchaField(
    #     widget=ReCaptchaV3
    # )

    class Meta:
        model = GeneralEnquiry
        exclude = ['potential_employer', 'last_modified']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Name'
                }
            ),
            'mobile_number': forms.TextInput(
                attrs={
                    'placeholder': 'Mobile Number'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Email Address'
                }
            ),
            'no_of_family_members': forms.NumberInput(
                attrs={
                    'placeholder': 'Number of Family Members'
                }
            ),
            'no_of_below_5': forms.NumberInput(
                attrs={
                    'placeholder': 'Number of Children below 5'
                }
            ),
            'no_of_babies': forms.NumberInput(
                attrs={
                    'placeholder': 'Number of Babies'
                }
            ),
            'remarks': forms.Textarea(
                attrs={
                    'rows': 8,
                    'cols': 15
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'name',
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
                    'email',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'property_type',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'no_of_family_members',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'no_of_below_5',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    HTML(
                        '<h5>Employer Requirments</h5>'
                    )
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'maid_nationality',
                    css_class='form-group col-md-6'
                ),
                Column(
                    'maid_type',
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Field(
                        'maid_responsibility',
                        template='widgets/custom_multi_choice_field.html'
                    ),
                    css_class='form-group'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Field(
                        'languages_spoken',
                        template='widgets/custom_multi_choice_field.html'
                    ),
                    css_class='form-group'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'remarks',
                    css_class='form-group col'
                ),
                css_class='form-row'
            ),
            # Row(
            #     Column(
            #         Field(
            #             'captcha',
            #             type='hidden'
            #         ),
            #         css_class='form-group col'
            #     ),
            #     css_class='form-row'
            # ),
            Row(
                Column(
                    'consent',
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
        
class ShortlistedEnquiryForm(forms.ModelForm):
    consent = forms.BooleanField(
        label="""
            By submitting this enquiry form, I consent to the collection, 
            use and disclosure of my personal data by Online Maid Pte Ltd to
            agencies that are listed on this platform.
        """
    )

    class Meta:
        model = ShortlistedEnquiry
        exclude = ['potential_employer', 'maids', 'last_modified']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    HTML(
                        '<h1>Enquiry Form</h1>'
                    )
                )
            ),
            Row(
                Column(
                    'remarks',
                    css_class='form-group'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'consent',
                    css_class='form-group col'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit',
                        'Submit',
                        css_class="btn btn-primary w-25"
                    ),
                    css_class='form-group col text-center'
                ),
                css_class='form-row'
            )
        )

# Generic Forms (forms.Form)