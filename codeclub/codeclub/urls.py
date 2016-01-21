from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views


admin.autodiscover()

urlpatterns = [
    url(r'', include('accounts.urls')),
    url(r'', include('challenges.urls')),

    url(r'^tagauks/', include(admin.site.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    url(r'^(?P<url>.*)$', views.flatpage),
]
