# Imports from python
from itertools import chain

# Imports from django
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Imports from foreign installed apps
from accounts.models import Employer
from agency.models import Agency, AgencyEmployee, AgencyPlan
from agency.mixins import AgencyLoginRequiredMixin, AgencyOwnerRequiredMixin
from maid.models import Maid

# Imports from local app

# Start of Views

# Template Views
class DashboardHomePage(AgencyLoginRequiredMixin, TemplateView):
    template_name = 'base/dashboard-home-page.html'

# Redirect Views

# List Views
class DashboardMaidList(AgencyLoginRequiredMixin, ListView):
    context_object_name = 'maids'
    http_method_names = ['get']
    model = Maid
    template_name = 'list/dashboard-maid-list.html'
    authority = None

    def get_authority(self):
        if self.request.user.groups.filter(name='Agency Owners').exists():
            authority = 'owner'

        if self.request.user.groups.filter(name='Agency Administrators').exists():
            authority = 'administrator'

        if self.request.user.groups.filter(name='Agency Managers').exists():
            authority = 'manager'

        if self.request.user.groups.filter(name='Agency Sales Staff').exists():
            authority = 'sales_staff'

        self.authority = authority

    def get(self, request, *args, **kwargs):
        self.get_authority()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Passes the authority to the template so that certain fields can be 
        # restricted based on who is editing the agency employee object.
        context = super().get_context_data(**kwargs)
        context.update({
            'authority': self.authority
        })
        return context

    def get_queryset(self):
        if self.authority == 'owner':
            agency = self.request.user.agency_owner.agency
        else:
            agency = self.request.user.agency_employee.agency
            
        return Maid.objects.filter(
            agency = agency
        )

class DashboardAccountList(AgencyLoginRequiredMixin, ListView):
    context_object_name = 'accounts'
    http_method_names = ['get']
    model = AgencyEmployee
    template_name = 'list/dashboard-account-list.html'
    authority = None

    def get_authority(self):
        if self.request.user.groups.filter(name='Agency Owners').exists():
            authority = 'owner'

        if self.request.user.groups.filter(name='Agency Administrators').exists():
            authority = 'administrator'

        if self.request.user.groups.filter(name='Agency Managers').exists():
            authority = 'manager'

        if self.request.user.groups.filter(name='Agency Sales Staff').exists():
            authority = 'sales_staff'

        self.authority = authority

    def get(self, request, *args, **kwargs):
        self.get_authority()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Passes the authority to the template so that certain fields can be 
        # restricted based on who is editing the agency employee object.
        context = super().get_context_data(**kwargs)
        context.update({
            'authority': self.authority
        })
        return context

    def get_queryset(self):
        if self.authority == 'owner':
            agency = self.request.user.agency_owner.agency
        else:
            agency = self.request.user.agency_employee.agency
            
        return AgencyEmployee.objects.filter(
            agency = agency
        )

class DashboardAgencyPlanList(AgencyOwnerRequiredMixin, ListView):
    context_object_name = 'plans'
    http_method_names = ['get']
    model = AgencyPlan
    template_name = 'list/dashboard-agency-plan-list.html'

# Detail Views
class DashboardAgencyDetail(AgencyLoginRequiredMixin, DetailView):
    context_object_name = 'agency'
    http_method_names = ['get']
    model = Agency
    template_name = 'detail/dashboard-agency-detail.html'

    def get_object(self):
        agency = super().get_object()

        # Checks if the user who is trying to access this view the owner or 
        # the agency's employees.
        if self.request.user == agency or self.request.user.agency == agency:
            return agency
        else:
            raise PermissionDenied()

# Create Views

# Update Views

# Delete Views
