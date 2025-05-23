from django.urls import path

from ads.views import AdCreateView, AdDeleteView, AdDetail, AdsList, AdUpdateView, UserAdsList


urlpatterns = [
    path('', AdsList.as_view(), name='ads_list'),
    path('<int:pk>', AdDetail.as_view(), name='ad_detail'),
    path('my/', UserAdsList.as_view(), name='user_ads_list'),
    path('create/', AdCreateView.as_view(), name='ad_create'),
    path('<int:pk>/update', AdUpdateView.as_view(), name='ad_update'),
    path('<int:pk>/delete', AdDeleteView.as_view(), name='ad_delete'),
]
