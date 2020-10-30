# Imports from django
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Imports from foreign installed apps

# Imports from local app
from .forms import EmployerCreationForm
from .models import Employer
from .mixins import EmployerVerifiedMixin

# Start of Views

## Template Views

## Redirect Views

## Detail Views
    
## Create Views
class EmployerCreate(CreateView):
    context_object_name = 'employer'
    form_class = EmployerCreationForm
    http_method_names = ['get','post']
    model = Employer
    template_name = 'employer-create.html'
    success_url = reverse_lazy('')

## Update Views
class EmployerUpdate(LoginRequiredMixin, EmployerVerifiedMixin, UpdateView):
    context_object_name = 'employer'
    form_class = EmployerCreationForm
    http_method_names = ['get','post']
    model = Employer
    template_name = 'employer-update.html'
    success_url = reverse_lazy('')

    def get_object(self, queryset=None):
        return Employer.objects.get(
            pk = self.request.user.pk
        )

## Delete Views
class EmployerDelete(LoginRequiredMixin, EmployerVerifiedMixin, DeleteView):
    context_object_name = 'employer'
    http_method_names = ['get','post']
    model = Employer
    template_name = 'employer-delete.html'
    success_url = reverse_lazy('')

    def get_object(self, queryset=None):
        return Employer.objects.get(
            pk = self.request.user.pk
        )
