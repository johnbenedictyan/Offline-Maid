from typing import Any, Dict, Optional

from django.http.request import HttpRequest as req

from accounts.models import PotentialEmployer
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse as res
from django.http.response import HttpResponseBase as RESBASE
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import RedirectView
from enquiry.forms import ShortlistedEnquiryForm
from enquiry.models import ShortlistedEnquiry
from maid.models import Maid




class AddTo(RedirectView):
    pattern_name = 'maid_list'

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        current_shortlist = self.request.session.get('shortlist', [])
        try:
            selected_maid = Maid.objects.get(
                pk=kwargs.get('pk')
            )
        except Maid.DoesNotExist:
            messages.error(
                self.request,
                'This maid does not exist'
            )
        else:
            if not selected_maid.is_published:
                messages.error(
                    self.request,
                    'This maid cannot be shortlisted at the moment'
                )
            elif selected_maid.pk in current_shortlist:
                messages.error(
                    self.request,
                    'This maid is already in your shortlist'
                )
            else:
                current_shortlist.append(
                    selected_maid.pk
                )
                self.request.session['shortlist'] = current_shortlist
        kwargs.pop('pk')
        return super().get_redirect_url(*args, **kwargs)


class RemoveFrom(RedirectView):
    pattern_name = 'maid_list'

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        current_shortlist = self.request.session.get('shortlist', [])
        try:
            selected_maid = Maid.objects.get(
                pk=kwargs.get('pk')
            )
        except Maid.DoesNotExist:
            messages.error(
                self.request,
                'This maid does not exist'
            )
        else:
            if selected_maid.pk not in current_shortlist:
                messages.error(
                    self.request,
                    'This maid is not in your shortlist'
                )
            else:
                current_shortlist.remove(
                    selected_maid.pk
                )
                self.request.session['shortlist'] = current_shortlist
        kwargs.pop('pk')
        return super().get_redirect_url(*args, **kwargs)


class ViewShortlist(CreateView):
    form_class = ShortlistedEnquiryForm
    http_method_names = ['get', 'post']
    model = ShortlistedEnquiry
    success_url = reverse_lazy('successful_enquiry')
    template_name = "shortlist.html"
    current_shortlist = []

    def dispatch(self, request: req, *args: Any, **kwargs: Any) -> RESBASE:
        self.current_shortlist = self.request.session.get('shortlist', [])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'shortlist': Maid.objects.filter(
                pk__in=self.current_shortlist
            )
        })
        return context

    def form_valid(self, form) -> res:
        form.instance.potential_employer = PotentialEmployer.objects.get(
            user=self.request.user
        )
        super().form_valid(form)
        for maid_pk in self.current_shortlist:
            self.object.maids.add(
                Maid.objects.get(
                    pk=maid_pk
                )
            )
            self.object.save()
        self.request.session['shortlist'] = []
        return HttpResponseRedirect(self.get_success_url())
