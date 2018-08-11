from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from export_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('export_app.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
