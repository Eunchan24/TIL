from django.urls import path
from voice.views import Sound_Check_Class

urlpatterns = [
    path('', Sound_Check_Class.as_view())
]
