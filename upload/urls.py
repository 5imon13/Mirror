from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    # path('livefeed/',views.livefeed, name='livefeed'),
    path('login/',views.login, name='login'),
    path('recommend/',views.recommend, name='recommend'),
    path('result/',views.result, name='result')
]