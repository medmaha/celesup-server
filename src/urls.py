from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


from django.views.generic import TemplateView

from api.urls import urlpatterns as api_url_patterns


urlpatterns = [
    path("administrator/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html")),
    # path("", include("api.urls", namespace="api")),
]


urlpatterns += api_url_patterns
