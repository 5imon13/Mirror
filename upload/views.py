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


@csrf_exempt
def index(request):
    if request.is_ajax():
        result = {}

        cap = cv2.VideoCapture(0)
        time.sleep(2)
        while True:
            # 從攝影機擷取一張影像
            ret, frame = cap.read()
            # 顯示圖片
            # cv2.imshow('frame', frame)
            path = os.path.join(settings.MEDIA_URL, "uuu.jpg").replace("\\", "/")
            cv2.imwrite(path[1:], frame)
            # 若按下 q 鍵則離開迴圈
            break
        cap.release()
        result["path"] = path
        # 關閉所有 OpenCV 視窗

        cv2.destroyAllWindows()
        print(path)
        return HttpResponse(json.dumps(result))

    elif request.method == "GET":
        template = loader.get_template("upload/upload.html")
        context = {}
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        f = request.FILES["imageUpload"]
        with open(os.path.join(settings.MEDIA_ROOT, "test.jpg"), "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            path = os.path.join(settings.MEDIA_URL, "test.jpg").replace("\\", "/")
        print(f"path: {path}")
        image = Image.open("." + path)
        print("呼叫YOLO，開始辨識")
        yolo = YOLO()
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
            request, "upload/result.html", {"path": path, "top": top, "bot": bot}
        )


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, image = self.video.read()
        # rotated_image = np.rot90(image)
        ret, jpeg = cv2.imencode(".jpg", image)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
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
        # return render(request,"upload/upload.html")
        return HttpResponse("hello")

