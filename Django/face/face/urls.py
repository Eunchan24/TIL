from django.contrib import admin
from django.urls import path, include
from face_test.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('face/', include('face_test.urls')),
    path('voice/',include('voice.urls'))
]
