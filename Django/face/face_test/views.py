from django.core.files.storage import default_storage
from django.shortcuts import render
from face_test.Face_Check import Eye_check
from django.views import View
from django.http import JsonResponse, HttpResponse
from face_test.models import *


# Create your views here.

def index(request):
    return render(request, 'index.html')


class FaceCheckView(View):
    def post(self, request):
        video_file = request.FILES['file']
        default_storage.save(video_file.name, video_file)

        face_json = Eye_check.face_run(self, video_file.name)

        f = face_engine()
        f.result = face_json

        f.save()
        return JsonResponse({'face_json': face_json}, status=200)


