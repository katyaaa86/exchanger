from django.urls import path

from ads.views import AdDetail, AdsList


urlpatterns = [
    path('', AdsList.as_view(), name='ads_list'),
    path('<int:pk>', AdDetail.as_view(), name='ad_detail'),
]
