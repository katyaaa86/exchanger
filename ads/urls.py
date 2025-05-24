from django.urls import path

from ads.views import (
    AdCreateView,
    AdDeleteView,
    AdDetailView,
    AdsListView,
    AdUpdateView,
    ExchangeProposalStatusUpdateView,
    ReceivedProposalsListView,
    SentProposalsListView,
    UserAdsListView,
)


urlpatterns = [
    path('', AdsListView.as_view(), name='ads_list'),
    path('<int:pk>', AdDetailView.as_view(), name='ad_detail'),
    path('my/', UserAdsListView.as_view(), name='user_ads_list'),
    path('create/', AdCreateView.as_view(), name='ad_create'),
    path('<int:pk>/update', AdUpdateView.as_view(), name='ad_update'),
    path('<int:pk>/delete', AdDeleteView.as_view(), name='ad_delete'),
    path('proposals/sent', SentProposalsListView.as_view(), name='sent_proposals_list'),
    path('proposals/received', ReceivedProposalsListView.as_view(), name='receive_proposals_list'),
    path(
        'proposals/<int:pk>/status',
        ExchangeProposalStatusUpdateView.as_view(),
        name='proposal_status_update',
    ),
]
