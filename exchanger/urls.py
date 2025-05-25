"""
URL configuration for exchanger project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from ads.views import error_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ads/', include('ads.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = lambda request, exception: error_view(request, exception, status_code=400)
handler403 = lambda request, exception: error_view(request, exception, status_code=403)
handler404 = lambda request, exception: error_view(request, exception, status_code=404)
handler500 = lambda request: error_view(request, status_code=500)
