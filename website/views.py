# Django Imports
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

# Project Apps Imports
from agency.mixins import OMStaffRequiredMixin
from agency.models import Agency
from enquiry.models import GeneralEnquiry
from payment.models import SubscriptionProduct
from maid.filters import MiniMaidFilter

# Start of Views


class BaseTemplateView(TemplateView):
    http_method_names = ['get']


class HomeView(BaseTemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data()
        kwargs.update({
            'filter': MiniMaidFilter()
        })
        return kwargs


class AboutUsView(BaseTemplateView):
    template_name = 'about-us.html'


class ContactUsView(BaseTemplateView):
    template_name = 'contact-us.html'


class TermsAndConditionsAgencyView(BaseTemplateView):
    template_name = 'terms-and-conditions-agency.html'


class TermsAndConditionsUserView(BaseTemplateView):
    template_name = 'terms-and-conditions-user.html'


class PrivacyPolicyView(BaseTemplateView):
    template_name = 'privacy-policy.html'


class HowItWorksView(BaseTemplateView):
    template_name = 'how-it-works.html'


class FAQView(BaseTemplateView):
    template_name = 'faq.html'


class UsefulLinksView(BaseTemplateView):
    template_name = 'useful-links.html'


class Error403View(BaseTemplateView):
    template_name = '403.html'


class Error404View(BaseTemplateView):
    template_name = '404.html'


class Error500View(BaseTemplateView):
    template_name = '500.html'


class RobotsTxt(BaseTemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'


class SitemapView(BaseTemplateView):
    template_name = 'sitemap.xml'


class AdminPanelView(OMStaffRequiredMixin, ListView):
    http_method_names = ['get']
    template_name = 'admin-panel.html'
    model = Agency
    paginate_by = 50
    context_object_name = 'agencies'
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'subscription_products': SubscriptionProduct.objects.all()
        })
        return context


class AdminPanelEnquiryListView(OMStaffRequiredMixin, ListView):
    http_method_names = ['get']
    template_name = 'admin-panel-enquiries.html'
    model = GeneralEnquiry
    paginate_by = 50
    context_object_name = 'enquiries'
