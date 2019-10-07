from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
import os
from yolo import YOLO
from PIL import Image
import argparse



def index(request):
    if request.method == "GET":
        template = loader.get_template('upload/upload.html')
        context = {}
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        f = request.FILES['imageUpload']
        with open(os.path.join(settings.MEDIA_ROOT, 'test.png'), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            path = os.path.join(settings.MEDIA_URL, 'test.png').replace('\\','/')
        print(f'path: {path}')

        image = Image.open('.'+path)
        yolo = YOLO()
        r_image = yolo.detect_image(image)
        r_image.save(f"{path}123", "JPEG")
        # print(f'd:{destination}')
        return render(request,'upload/result.html', {'path':path})

def upload_img(request):
    #upload image
    return None

def analysis(request):
    #analyze user upload img and post(AJAX) it with bounding box 
    return None