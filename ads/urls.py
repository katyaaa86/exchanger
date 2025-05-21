from django.urls import path

from ads.views import AdsList


urlpatterns = [
    path('', AdsList.as_view(), name='ads_list'),
]
