

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('contrib/', include('contrib.urls'))
]

@staff_member_required()
def debug(request):
    raise Exception('Debug')

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path('debug/', debug),]




