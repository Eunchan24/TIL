from django.urls import path
from face_test.views import FaceCheckView

urlpatterns = [
    path('', FaceCheckView.as_view())
]
