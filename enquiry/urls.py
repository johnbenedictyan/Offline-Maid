# Imports from django
from django.urls import include, path

# Imports from foreign installed apps

# Imports from local app

## Redirect Views
from .views import DeactivateGeneralEnquiryView, ToggleApproveEnquiryView

## Template Views 
from .views import SuccessfulEnquiryView

## List Views
from .views import EnquiryListView

## Detail Views

## Create Views
from .views import GeneralEnquiryView

## Update Views

## Delete Views

# Start of Urls

urlpatterns = [
    path(
        'general/',
        GeneralEnquiryView.as_view(),
        name='general_enquiry'
    ),
    path(
        'all/',
        EnquiryListView.as_view(),
        name='enquiry_list'
    ),
    path(
        'deactive/<int:pk>/',
        DeactivateGeneralEnquiryView.as_view(),
        name='deactivate_enquiry'
    ),
    path(
        'toggle-approve/<int:pk>/',
        ToggleApproveEnquiryView.as_view(),
        name='toggle_approve_enquiry'
    ),
    path(
        'success/',
        SuccessfulEnquiryView.as_view(),
        name='successful_enquiry'
    )
]
