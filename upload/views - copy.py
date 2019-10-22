from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader
from django.conf import settings
import os
from upload.yolo import YOLO
from PIL import Image
import argparse
import cv2
import json
from django.views.decorators.csrf import csrf_exempt
import time
from django.views.decorators import gzip
from django.http import HttpResponseServerError
import numpy as np
import base64
import face_recognition
import upload.facerec_from_webcam_faster as face
from django.shortcuts import redirect
from upload.models import Product
from django.db import models

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
    #     f = request.FILES["imageUpload"]
    #     with open(os.path.join(settings.MEDIA_ROOT, "test.jpg"), "wb+") as destination:
    #         for chunk in f.chunks():
    #             destination.write(chunk)
    #         path = os.path.join(settings.MEDIA_URL, "test.jpg").replace("\\", "/")
    #     print(f"path: {path}")
    #     image = Image.open("." + path)
    #     if image.mode == "P":
    #         image = image.convert('RGB')
    #     print("呼叫YOLO，開始辨識")
    #     yolo = YOLO()
    #     yolo.clear_session() 
    #     r_image, result = yolo.detect_image(image)
    #     print("辨識完成，輸出檔案")
    #     yolo.clear_session()
    #     # r_image.show()
    #     path = path.replace("test.jpg", "out.jpg")
    #     r_image.save(path[1:])
    #     print(result)
    #     if len(result) != 1:
    #         top = result[1]
    #         bot = result[0]
    #     else:
    #         top, bot = result[0], result[0]
    #     return render(
    #         request, "upload/result.html", locals()
    #     )
# {"path": path, "top": top, "bot": bot}
@csrf_exempt
def result(request):
    bot = 'test'
    top = 'test'
    if request.is_ajax():
        del request.session['uid']
        msg = 'Successfully log out!'
        return HttpResponse(json.dumps(msg))

    elif request.method == "GET":
        template = loader.get_template("upload/result.html")
        context = {}
        if 'uid' not in request.session:
            return render(request,"upload/result.html",locals())
        else:
            status = 'login'
            user = request.session['uid']
            return render(request,"upload/result.html",locals())
        
    elif request.method == "POST":
        # return render(request,"upload/recommend.html")
        request.session['option'] = 'denim'
        # return redirect("/upload/recommend/")
        f = request.FILES["imageUpload"]
        with open(os.path.join(settings.MEDIA_ROOT, "test.jpg"), "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            path = os.path.join(settings.MEDIA_URL, "test.jpg").replace("\\", "/")
        print(f"path: {path}")
        image = Image.open("." + path)
        if image.mode == "P":
            image = image.convert('RGB')
        print("呼叫YOLO，開始辨識")
        yolo = YOLO()
        yolo.clear_session() 
        r_image, result = yolo.detect_image(image)
        print("辨識完成，輸出檔案")
        yolo.clear_session()
        # r_image.show()
        path = path.replace("test.jpg", "out.jpg")
        r_image.save(path[1:])
        print(result)
        if len(result) != 1:
            top = result[1]
            bot = result[0]
        else:
            top, bot = result[0], result[0]
        return render(
            request, "upload/result.html", locals()
        )

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self, count):
        ret, image = self.video.read()
        # rotated_image = np.rot90(image)
        ret, jpeg = cv2.imencode(".jpg", image)

        # path = os.path.join(settings.MEDIA_URL, f"tmp{count}.jpg").replace("\\", "/")
        # if count%3==0:
        #     cv2.imwrite(path[1:], rotated_image)
        return jpeg.tobytes()


def gen(camera):
    count = 0
    while True:
        frame = camera.get_frame(count)
        count+=1
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


@gzip.gzip_page
def livefeed(request):
    try:
        return StreamingHttpResponse(
            gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame"
        )
    except HttpResponseServerError as e:
        print("aborted")


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
        #print(path)
        name = face.detec()
        request.session['uid'] = name
        # status = 'login'
        # user = name
        return redirect("/upload/")
        # render(request,"upload/upload.html",locals())
        # return HttpResponse(f"<h1>Hello {request.session['uid']}!</h1>")

def recommend(request):

    if request.is_ajax():
        del request.session['uid']
        msg = 'Successfully log out!'
        return HttpResponse(json.dumps(msg))
    else:
        # for obj in Product.objects.all():
        #     print(obj.img)
        # template = loader.get_template("upload/recommend.html")
        # context={}
        option = request.session['option']
        print(option)
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
    

