from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('authentication.urls')),
    url(r'', include('baseshop.urls')),
]
