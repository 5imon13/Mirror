from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators import gzip
from django.http import HttpResponseServerError
from django.shortcuts import redirect
from django.db import models

import os
import argparse
import cv2
import json
import time
from PIL import Image
import numpy as np
import base64

from upload.models import Product
import upload.facerec_from_webcam_faster as face
import upload.label_image as style_model
from upload.yolo import YOLO
import face_recognition

global count
@csrf_exempt
def index(request):
    if request.is_ajax():
        del request.session['uid']
        msg = 'Successfully log out!'
        return HttpResponse(json.dumps(msg))

    elif request.method == "GET":
        template = loader.get_template("upload/upload.html")
        context = {}
        if 'uid' not in request.session:
            return HttpResponse(template.render(context, request))
        else:
            status = 'login'
            user = request.session['uid']
            return render(request,"upload/upload.html",locals())
    # elif request.method == "POST":

@csrf_exempt
def result(request):
    # bot = 'test'
    # top = 'test'
    request.session['option'] = 'denim'

    if request.is_ajax():
        del request.session['uid']
        msg = 'Successfully log out!'
        return HttpResponse(json.dumps(msg))

    elif request.method == "GET":
        if 'uid' not in request.session:
            return render(request,"upload/result.html",locals())
        else:
            status = 'login'
            user = request.session['uid']
            return render(request,"upload/result.html",locals())
        
    elif request.method == "POST":
        request.session['option'] = 'denim'
        f = request.FILES["imageUpload"]
        with open(os.path.join(settings.MEDIA_ROOT, "test.jpg"), "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            path = os.path.join(settings.MEDIA_URL, "test.jpg").replace("\\", "/")
        print(f"path: {path}")
        style_path = "."+path
        image = Image.open("." + path)
        if image.mode == "P":
            image = image.convert('RGB')
        print("呼叫YOLO，開始辨識")
        yolo = YOLO()
        yolo.clear_session() 
        r_image, result = yolo.detect_image(image)
        print("辨識完成，輸出檔案")
        yolo.clear_session()
        path = path.replace("test.jpg", "out.jpg")
        r_image = r_image.convert('RGB')
        r_image.save(path[1:])
        print(result)
        if len(result) > 1:
            top = result[1]
            bot = result[0]
        elif len(result) == 1:
            top, bot = result[0], result[0]
        else:
            top, bot = "",""
        print('GooleNet 開始分類風格')
        style_type,percent =style_model.predict(style_path)
        percent = round(percent*100, 2)
        return render(
            request, "upload/result.html", locals()
        )

@csrf_exempt
def login(request):
    if request.method == "GET":
        template = loader.get_template("upload/login.html")
        context = {}
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        img = request.POST['canvasData'].split(',')[1]
        imgdata = base64.b64decode(img)
        path = os.path.join(settings.MEDIA_URL, "head.jpg").replace("\\", "/")
        with open(path[1:], 'wb') as f:
            f.write(imgdata)
        name = face.detec()
        request.session['uid'] = name
        return redirect("/upload/")

def recommend(request):
    if request.is_ajax():
        del request.session['uid']
        msg = 'Successfully log out!'
        return HttpResponse(json.dumps(msg))
    else:
        try :
            option = request.POST['select_style']
        except:
            option = 'denim'
        request.session['option'] = option        
        # print(option)
        style = Product.objects.filter(style=option)
        path = []
        topURL = []
        botURL = []
        for item in style:
            path.append(item.img)
            topURL.append(item.top_url)
            botURL.append(item.bot_url)
        topURL = json.dumps(topURL)
        botURL = json.dumps(botURL)
        if 'uid' not in request.session:
            return render(request, "upload/recommend.html", locals())
        else:
            status = 'login'
            user = request.session['uid']
            return render(request,"upload/recommend.html",locals())