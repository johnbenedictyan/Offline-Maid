# Imports from python

# Imports from django
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy

# Imports from other apps
from onlinemaid.constants import (
    AUTHORITY_GROUPS, AG_OWNERS, AG_ADMINS, AG_MANAGERS, AG_SALES, P_EMPLOYERS
)
from onlinemaid.mixins import (
    AccessMixin, LoginRequiredMixin, SuperUserRequiredMixin, GroupRequiredMixin
)
from maid.models import Maid

# Imports from within the app
from .constants import AgencyEmployeeRoleChoices
from .models import (
    Agency, AgencyEmployee, AgencyBranch, AgencyPlan, AgencyOwner
)

# Utiliy Classes and Functions

# Start of Mixins

class OnlineMaidStaffRequiredMixin(SuperUserRequiredMixin):
    login_url = reverse_lazy('sign_in')
    permission_denied_message = '''You are required to login as a member of 
                                Online Maid Pte Ltd to perform this action'''

class AgencyLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('agency_sign_in')

    def dispatch(self, request, *args, **kwargs):
        ## Superuser should not have the permssion to access agency views.
        ## It will also mess up the get authority mixin
        if request.user.is_superuser:
            return self.handle_no_permission(request)

        return super(AgencyLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)

    # This mixin is the base mixin if we want the user to login in using the 
    # agency log in page rather than the log in page for the potential 
    # employers.

class AgencyOwnerRequiredMixin(GroupRequiredMixin):
    group_required = u"Agency Owners"
    login_url = reverse_lazy('agency_sign_in')
    permission_denied_message = '''You are required to login using an Agency
                                owners account to perform this action'''
                                
class AgencyAdministratorRequiredMixin(GroupRequiredMixin):
    group_required = u"Agency Administrators"
    login_url = reverse_lazy('agency_sign_in')
    permission_denied_message = '''You are required to login using an Agency
                                administrator account to perform this 
                                action'''

class AgencyManagerRequiredMixin(GroupRequiredMixin):
    group_required = u"Agency Managers"
    login_url = reverse_lazy('agency_sign_in')
    permission_denied_message = '''You are required to login using an Agency
                                managers account to perform this action'''

class AgencyAdminTeamRequiredMixin(GroupRequiredMixin):
    group_required = [u"Agency Owners", u"Agency Administrators"]
    login_url = reverse_lazy('agency_sign_in')
    permission_denied_message = '''You are required to login using either
                                an Agency owner or administrator account 
                                to perform this action'''

class AgencySalesTeamRequiredMixin(GroupRequiredMixin):
    group_required = [
        u"Agency Administrators",
        u"Agency Managers",
        u"Agency Sales Team"
    ]
    login_url = reverse_lazy('agency_sign_in')
    permission_denied_message = '''You are required to login using either
                                an Agency administrator, manager or sales staff
                                account to perform this action'''

class SpecificAgencyOwnerRequiredMixin(AgencyOwnerRequiredMixin):
    check_type = None
    check_model_dict = {
        'employee': AgencyEmployee,
        'branch': AgencyBranch,
        'plan': AgencyPlan
    }
    permission_denied_message = '''You are required to login using the specific
                                Agency owner account to perform this action'''

    def dispatch(self, request, *args, **kwargs):
        self.request = request

        res = super(SpecificAgencyOwnerRequiredMixin, self).dispatch(
            request, *args, **kwargs)

        error_msg = None

        if self.check_type is None:
            error_msg = 'set'
        if self.check_type not in self.check_model_dict:
            error_msg = 'a key in the check_model_dict'

        if error_msg:
            raise ImproperlyConfigured(
                '{0} requires the "check_type" attribute to be '
                '{1}.'.format(self.__class__.__name__, error_msg)
            )

        check_model = self.check_model_dict[self.check_type]

        try:
            check_model.objects.get(
                pk = self.kwargs.get(
                    self.pk_url_kwarg
                ),
                agency = self.request.user.agency_owner.agency
            )
        except check_model.DoesNotExist:
            return self.handle_no_permission(request)

        return res

class SpecificAgencyEmployeeLoginRequiredMixin(AgencyLoginRequiredMixin):
    permission_denied_message = '''You are required to login using this
                                employee's or Agency owner account to
                                perform this action'''
                            
    def dispatch(self, request, *args, **kwargs):
        self.request = request

        res = super(SpecificAgencyEmployeeLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)

            
        if self.request.user.pk != self.kwargs.get(self.pk_url_kwarg):
            ae = AgencyEmployee.objects.get(
                pk = self.kwargs.get(
                    self.pk_url_kwarg
                )
            )
            if self.request.user.groups.filter(name='Agency Owners').exists():
                if ae.agency != self.request.user.agency_owner.agency:
                    return self.handle_no_permission(request)

            elif self.request.user.groups.filter(
                name='Agency Administrators'
            ).exists():
                if ae.agency != self.request.user.agency_employee.agency:
                    return self.handle_no_permission(request)

            else:
                return self.handle_no_permission(request)

        return res

class GetAuthorityMixin:
    def get_authority(self):
        authority = agency_id = ''
        for auth_name in AUTHORITY_GROUPS:
            if self.request.user.groups.filter(name=auth_name).exists():
                authority = auth_name
                if authority == AG_OWNERS:
                    agency_id = self.request.user.agency_owner.agency.pk
                elif authority != P_EMPLOYERS:
                    agency_id = self.request.user.agency_employee.agency.pk

        return {
            'authority': authority,
            'agency_id': agency_id
        }

    def get(self, request, *args, **kwargs):
        if not self.authority and self.authority != '':
            raise ImproperlyConfigured(
                '{0} is missing the authority attribute'
                .format(self.__class__.__name__)
            )
        if not self.agency_id and self.agency_id != '':
            raise ImproperlyConfigured(
                '{0} is missing the agency_id attribute'
                .format(self.__class__.__name__)
            )
        self.authority = self.get_authority()['authority']
        self.agency_id = self.get_authority()['agency_id']
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.authority and self.authority != '':
            raise ImproperlyConfigured(
                '{0} is missing the authority attribute'
                .format(self.__class__.__name__)
            )
        if not self.agency_id and self.agency_id != '':
            raise ImproperlyConfigured(
                '{0} is missing the agency_id attribute'
                .format(self.__class__.__name__)
            )
        self.authority = self.get_authority()['authority']
        self.agency_id = self.get_authority()['agency_id']
        return super().post(request, *args, **kwargs)

class PermissionsMixin:
    MAID = 'Maid'
    checkee_models_dict = {
        MAID: Maid,
    }
    use_strict_hierachy = True 
    # This means that agency owners can view a route whose checker is below it
    # i.e. Admins, managers, sales staff

    def get_models(self):
        checker_model = self.checker_model
        checkee_model = self.checkee_model

        if not checker_model:
            raise ImproperlyConfigured(
                '{0} is missing the checker_model attribute'
                .format(self.__class__.__name__)
            )

        if not checkee_model:
            raise ImproperlyConfigured(
                '{0} is missing the checkee_model attribute'
                .format(self.__class__.__name__)
            )
        
        return {
            'checker': checker_model,
            'checkee': checkee_model
        }

    def pre_check(self, agency_id):
        hierachy = [P_EMPLOYERS, SALES_STAFF, AG_MANAGERS, AG_ADMINS, AG_OWNERS]
        if not (self.authority and self.agency_id):
            raise ImproperlyConfigured(
                '{0} must come after the GetAuthorityMixin'
                .format(self.__class__.__name__)
            )
        authority = self.authority
        checker_model = self.checker_model

        if self.use_strict_hierachy:
            use_strict_hierachy = self.use_strict_hierachy
        
        if agency_id:
            if self.agency_id != agency_id:
                raise PermissionDenied

        if use_strict_hierachy == True:
            if hierachy.index(authority) < hierachy.index(checker_model):
                raise PermissionDenied
        else:
            if authority != checker_model:
                raise PermissionDenied

    def check(self):
        self.pre_check()

    def dispatch(self, request, *args, **kwargs):
        self.check()
        return super().dispatch(request, *args, **kwargs)