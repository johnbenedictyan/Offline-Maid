# Imports from django
from django.urls import include, path

# Imports from foreign installed apps

# Imports from local app

## Redirect Views

## List Views
from .views import (
    DashboardMaidList, DashboardAccountList, DashboardAgencyPlanList,
    DashboardEnquiriesList, DashboardAgencyBranchList
)

## Detail Views
from .views import DashboardAgencyDetail, DashboardMaidDetail

## Form Views
from .views import DashboardMaidCreation, DashboardAgencyUpdate

## Create Views
from .views import (
    DashboardMaidInformationCreate, DashboardMaidLanguageSpokenCreate,
    DashboardMaidFHPDRCreate,
    DashboardMaidExperienceCreate, DashboardMaidOtherRemarksCreate,
    DashboardAgencyEmployeeCreate
)

## Template Views
from .views import DashboardHomePage

## Update Views
from .views import (
    DashboardAgencyInformationUpdate, DashboardAgencyOpeningHoursUpdate,
    DashboardMaidInformationUpdate, DashboardMaidLanguageSpokenUpdate,
    DashboardMaidFHPDRUpdate, DashboardMaidExperienceUpdate,
    DashboardMaidOtherRemarksUpdate, DashboardAgencyEmployeeUpdate
)

## Delete Views

## Generic Views
from .views import DashboardDataProviderView

# Start of Urls

urlpatterns = [
    path(
        'data/',
        DashboardDataProviderView.as_view(),
        name='dashboard_data_provider'
    ),
    path(
        'view/',
        include([
            path(
                'maids/',
                include([
                    path(
                        '',
                        DashboardMaidList.as_view(),
                        name='dashboard_maid_list'
                    ),
                    path(
                        '<int:pk>/',
                        DashboardMaidDetail.as_view(),
                        name='dashboard_maid_detail'
                    )
                ])
            ),
            path(
                'accounts',
                DashboardAccountList.as_view(),
                name='dashboard_account_list'
            ),
            path(
                'agency-details',
                DashboardAgencyDetail.as_view(),
                name='dashboard_agency_detail'
            ),
            path(
                'agency-plans',
                DashboardAgencyPlanList.as_view(),
                name='dashboard_agency_plan_list'
            ),
            path(
                'enquiries',
                DashboardEnquiriesList.as_view(),
                name='dashboard_enquiries_list'
            ),
            path(
                'branches',
                DashboardAgencyBranchList.as_view(),
                name='dashboard_branches_list'
            )
        ])
    ),
    path(
        'create/',
        include([
            path(
                'maid/',
                include([
                    path(
                        'information',
                        DashboardMaidInformationCreate.as_view(),
                        name='dashboard_maid_information_create'
                    ),
                    path(
                        '<int:pk>/',
                        include([
                            path(
                                'language-spoken',
                                DashboardMaidLanguageSpokenCreate.as_view(),
                                name='dashboard_maid_language_spoken_create'
                            ),
                            path(
                                'food-handling-dietary-restriction',
                                DashboardMaidFHPDRCreate.as_view(),
                                name='dashboard_maid_fhpdr_create'
                            ),
                            path(
                                'experience',
                                DashboardMaidExperienceCreate.as_view(),
                                name='dashboard_maid_experience_create'
                            ),
                            path(
                                'other-remarks',
                                DashboardMaidOtherRemarksCreate.as_view(),
                                name='dashboard_maid_other_remarks_create'
                            )
                        ])
                    )
                ])
            ),
            path(
                'employee',
                DashboardAgencyEmployeeCreate.as_view(),
                name='dashboard_employee_create'
            )
        ])
    ),
    path(
        'update/',
        include([
            path(
                'agency',
                DashboardAgencyUpdate.as_view(),
                name='dashboard_agency_update'
            ),
            path(
                'agency-information',
                DashboardAgencyInformationUpdate.as_view(),
                name='dashboard_agency_information_update'
            ),
            path(
                'agency-opening-hours',
                DashboardAgencyOpeningHoursUpdate.as_view(),
                name='dashboard_agency_opening_hours_update'
            ),
            path(
                'agency-employee/<int:pk>',
                DashboardAgencyEmployeeUpdate.as_view(),
                name='dashboard_agency_employee_update'
            ),
            path(
                'maid/<int:pk>/',
                include([
                    path(
                        'information',
                        DashboardMaidInformationCreate.as_view(),
                        name='dashboard_maid_information_update'
                    ),
                    path(
                        'language-spoken',
                        DashboardMaidLanguageSpokenCreate.as_view(),
                        name='dashboard_maid_language_spoken_update'
                    ),
                    path(
                        'food-handling-dietary-restriction',
                        DashboardMaidFHPDRCreate.as_view(),
                        name='dashboard_maid_fhpdr_update'
                    ),
                    path(
                        'experience',
                        DashboardMaidExperienceCreate.as_view(),
                        name='dashboard_maid_experience_update'
                    ),
                    path(
                        'other-remarks',
                        DashboardMaidOtherRemarksCreate.as_view(),
                        name='dashboard_maid_other_remarks_update'
                    )
                ])
            )
        ])
    ),
    path(
        '',
        DashboardHomePage.as_view(),
        name='dashboard_home'
    )
]
