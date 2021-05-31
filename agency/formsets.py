# Imports from django
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

# Imports from foreign installed apps
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field

# Imports from local apps
from .forms import AgencyBranchForm
from .models import Agency, AgencyBranch

# Start of Formsets

AgencyBranchFormSet = inlineformset_factory(
    parent_model=Agency,
    form=AgencyBranchForm,
    model=AgencyBranch,
    extra=1,
    min_num=1,
    max_num=10
)

class AgencyBranchFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Row(
                Column(
                    Row(
                        Column(
                            Field(
                                'DELETE'
                            ),
                            css_class='col-12 text-right'
                        )
                    ),
                    Row(
                        Column(
                            'name',
                            css_class='col-md-6'
                        ),
                        Column(
                            'address_1',
                            css_class='col-md-6'
                        ),
                        Column(
                            'address_2',
                            css_class='col-md-6'
                        ),
                        Column(
                            'postal_code',
                            css_class='col-md-6'
                        ),
                        Column(
                            'email',
                            css_class='col-md-6'
                        ),
                        Column(
                            'office_number',
                            css_class='col-md-6'
                        ),
                        Column(
                            'mobile_number',
                            css_class='col-md-6'
                        ),
                        Column(
                            'main_branch',
                            css_class='col-md-6'
                        )
                    )
                ),
                css_class='form-group',
            )
        )
        self.render_required_fields = True