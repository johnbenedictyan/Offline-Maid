import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_postcode(value):
    err_msg = _('%(value)s is not a valid Singapore post code')

    # Basic length validation, if failed then no need to run regex check
    if len(value)!= 6:
        raise ValidationError(
            err_msg,
            params={'value': value},
        )
    
    # Must be all numerical digits
    if not re.match(r'^[0-9]{6}$',value):
        raise ValidationError(
            err_msg,
            params={'value': value},
        )
