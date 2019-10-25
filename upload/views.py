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
import pandas as pd
import xgboost
from upload.Size import predictSize

@csrf_exempt
def index(request):
    template = loader.get_template("upload/index.html")
    context = {}
    return HttpResponse(template.render(context, request))

@csrf_exempt
def upload(request):
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

        if 'upload_mode' in request.POST:
            f = request.FILES["imageUpload"]
        # print(request.POST['canvasData'])
            with open(os.path.join(settings.MEDIA_ROOT, "test.jpg"), "wb+") as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
                path = os.path.join(settings.MEDIA_URL, "test.jpg").replace("\\", "/")
            print(f"path: {path}")
            
            
        else:
            image = request.POST['canvasData'].split(',')[1]
            imgdata = base64.b64decode(image)
            path = os.path.join(settings.MEDIA_URL, "test.jpg").replace("\\", "/")
            with open(path[1:], 'wb') as f:
                f.write(imgdata)
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
        if len(result) > 0:
            for item in result:
                if item['type'] == 'top':
                    top = item
                elif item['type'] == 'bot':
                    bot = item
                else:
                    full = item
            # top = result[1]
            # bot = result[0]
            print('GooleNet 開始分類風格')
            style_type,percent = style_model.predict(style_path)
            percent = round(percent*100, 2)
            if style_type == 'denim':
                style_type = '單寧風'
            elif style_type == 'business':
                style_type = '商務風'
            elif style_type == 'dress':
                style_type = '洋裝'
            elif style_type == 'sport':
                style_type = '運動風'
            else:
                style_type = '其他'

        else:
            top, bot = "",""
            style_type = "辨識不出服飾，無法判斷風格"
        
        if 'uid' not in request.session:
            return render(request, "upload/result.html", locals())
        else:
            status = 'login'
            user = request.session['uid']
            return render(request,"upload/result.html",locals())
        # return render(
        #     request, "upload/result.html", locals()
        # )

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
        if name=='Unknown':
            return redirect("/upload/upload/")
        else:
            request.session['uid'] = name
            return redirect("/upload/upload/")

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

def predict(request):
    if request.is_ajax():
        reqDict = request.POST.dict()
        age = reqDict['Age']
        height = reqDict['Height']
        weight = reqDict['Weight']
        bustsize = reqDict['BustSize']
        bodytype = reqDict['BodyType']
        resultSize = predictSize(bustsize,weight,bodytype,height,age)    
        return HttpResponse(json.dumps(resultSize))
    elif request.method == 'GET':
        if 'uid' not in request.session:
            return render(request, "upload/predict.html", locals())
        else:
            status = 'login'
            user = request.session['uid']
            return render(request,"upload/predict.html",locals())
