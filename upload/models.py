from django.db import models
from upload.yolo import YOLO

# class Profile(models.Model):
#    name = models.CharField(max_length = 50)
#    picture = models.ImageField(upload_to = 'pictures')

#    class Meta:
#       db_table = "profile"
yolo = YOLO()
class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    style = models.CharField(max_length=30)
    img = models.CharField(max_length=500)
    top_name = models.CharField(max_length=500)
    top_url = models.URLField()
    bot_name = models.CharField(max_length=500)
    bot_url = models.URLField()
    def __str__(self):
        return str(self.pid)

class Member(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=300)
    bust_size = models.IntegerField()
    weight = models.IntegerField()
    height = models.IntegerField()
    body_type = models.IntegerField()
    age = models.IntegerField()
    def __str__(self):
        return str(self.name)