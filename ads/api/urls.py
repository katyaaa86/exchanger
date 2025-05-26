from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from ads.api import views


router = DefaultRouter()
router.register('ads', views.AdViewSet, basename='ad')
router.register('proposals', views.ProposalViewSet, basename='exchangeproposal')
urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path('', include(router.urls)),
]
