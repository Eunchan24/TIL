from django.core.files.storage import default_storage
from django.shortcuts import render
from voice.Voice_Check import Sound_Check_Class
from django.views import View
from django.http import JsonResponse, HttpResponse
from voice.models import *
# Create your views here.

def index(request):
    return  render((request, 'index.html')

class VoiceCheckView(View):
    def post(self, request):
        # 음성파일 받아야함
        audio_file = request.FILES['file']
        default_storage.save(audio_file.name, audio_file)

        voice_json = Sound_Check_Class.voice_run(self, audio_file.name)

        v = voice_engion()
        v.result = voice_json

        v.save

        return JsonResponse({'voice_json': voice_json}, ststus=200)