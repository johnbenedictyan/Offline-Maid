from django.contrib import admin
from .models import (
    Agency, AgencyEmployee, AgencyContactInformation, AgencyLocation,
    AgencyOperatingHours, AgencyPlan
)

# Register your models here.
admin.site.register(Agency)
admin.site.register(AgencyEmployee)
admin.site.register(AgencyContactInformation)
admin.site.register(AgencyLocation)
admin.site.register(AgencyOperatingHours)
admin.site.register(AgencyPlan)