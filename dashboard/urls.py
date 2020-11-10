# Imports from django
from django.urls import include, path

# Imports from foreign installed apps

# Imports from local app

## Redirect Views

## List Views
from .views import DashboardMaidList, DashboardAccountList

## Detail Views

## Create Views

## Template Views
from .views import DashboardHomePage

## Update Views

## Delete Views

# Start of Urls

urlpatterns = [
    path(
        'view/',
        include([
            path(
                'maids',
                DashboardMaidList.as_view(),
                name='dashboard_maid_list'
            ),
            path(
                'accounts',
                DashboardAccountList.as_view(),
                name='dashboard_account_list'
            )
        ])
    ),
    path(
        '',
        DashboardHomePage.as_view(),
        name='dashboard_home'
    )
]
