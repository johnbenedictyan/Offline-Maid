# Imports from django
from django.urls import include, path

# Imports from foreign installed apps

# Imports from local app

## Form Views
from .views import MaidCreateFormView, MaidExperienceUpdate

## Redirect Views
from .views import MaidTogglePublished, MaidToggleFeatured

## List Views
from .views import MaidList

## Detail Views
from .views import MaidDetail, PdfMaidBiodataView

## Create Views
# from .views import MaidEmploymentHistoryFormSetView

## Update Views
from .views import (
#     MaidInfantChildCareUpdate, MaidElderlyCareUpdate, MaidDisabledCareUpdate,
#     MaidGeneralHouseworkUpdate, MaidCookingUpdate,
    MaidLoanTransactionUpdate
)

## Delete Views
from .views import (
    MaidDelete
)

## Generic Views
from .views import MaidProfileView, FeaturedMaidListView

# Start of Urls

urlpatterns = [
    path(
        'create/',
        include([
            path(
                '',
                MaidCreateFormView.as_view(),
                name='maid_create'
            ),
        ])
    ),
    path(
        'delete/',
        include([
            path(
                '<int:pk>/',
                MaidDelete.as_view(),
                name='maid_delete'
            ),
        ])
    ),
    path(
        'update/<int:pk>/',
        include([
            # path(
            #     '',
            #     MaidUpdate.as_view(),
            #     name='maid_update'
            # ),
            path(
                'experience/',
                MaidExperienceUpdate.as_view(),
                name='maid_care_details_update'
            ),
            # path(
            #     'employment/',
            #     MaidEmploymentHistoryFormSetView.as_view(),
            #     name='maid_employment_formset'
            # ),
            path(
                'aft/<int:loan_transaction_pk>/',
                MaidLoanTransactionUpdate.as_view(),
                name='maid_loan_transaction_update'
            ),
            # path(
            #     'icc/',
            #     MaidInfantChildCareUpdate.as_view(),
            #     name='maid_infant_child_care_update'
            # ),
            # path(
            #     'ec/',
            #     MaidElderlyCareUpdate.as_view(),
            #     name='maid_elderly_care_update'
            # ),
            # path(
            #     'dc/',
            #     MaidDisabledCareUpdate.as_view(),
            #     name='maid_disabled_care_update'
            # ),
            # path(
            #     'gh/',
            #     MaidGeneralHouseworkUpdate.as_view(),
            #     name='maid_general_housework_update'
            # ),
            # path(
            #     'c/',
            #     MaidCookingUpdate.as_view(),
            #     name='maid_cooking_update'
            # )
        ])
    ),
    path(
        'view/',
        include([
            path(
                '',
                MaidList.as_view(),
                name='maid_list'
            ),
            path(
                'featured/',
                FeaturedMaidListView.as_view(),
                name='featured_maid_list'
            ),
            path(
                '<int:pk>/',
                include([
                    path(
                        '',
                        MaidDetail.as_view(),
                        name='maid_detail'
                    ),
                    path(
                        'profile/',
                        MaidProfileView.as_view(),
                        name='maid_profile'
                    ),
                    path(
                        'biodata/pdf/',
                        PdfMaidBiodataView.as_view(),
                        name='maid_biodata_pdf'
                    ),
                ])
            )
        ])
    ),
    path(
        'toggle/<int:pk>/',
        include([
            path(
                'published/',
                MaidTogglePublished.as_view(),
                name='maid_toggle_published'
            ),
            path(
                'featured/',
                MaidToggleFeatured.as_view(),
                name='maid_toggle_featured'
            )
        ])
    )
]
