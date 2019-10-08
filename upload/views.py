from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
import os
from upload.yolo import YOLO
from PIL import Image
import argparse




def index(request):
    if request.method == "GET":
        template = loader.get_template('upload/upload.html')
        context = {}
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        f = request.FILES['imageUpload']
        with open(os.path.join(settings.MEDIA_ROOT, 'test.jpg'), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            path = os.path.join(settings.MEDIA_URL, 'test.jpg').replace('\\','/')
        print(f'path: {path}')
        image = Image.open('.'+path)
        print('呼叫YOLO，開始辨識')
        yolo = YOLO()
        r_image, result= yolo.detect_image(image)
        print('辨識完成，輸出檔案')
        yolo.clear_session()
        #r_image.show()
        path  = path.replace('test.jpg','out.jpg')
        r_image.save(path[1:])
        print(result)
        if(len(result)!=1):
            top = result[1]
            bot = result[0]
        else:
            top, bot = result[0], result[0]
        return render(request,'upload/result.html', {'path':path, 'top':top, 'bot':bot})

def upload_img(request):
    #upload image
    return None

def analysis(request):
    #analyze user upload img and post(AJAX) it with bounding box 
    return None