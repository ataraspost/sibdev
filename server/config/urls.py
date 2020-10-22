

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('contrib/', include('contrib.urls'))
]

def debug(request):
    from user.tasks import send_email_precedent
    send_email_precedent()
    raise Exception(debug())

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path('debug/', debug),]




