from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('livefeed/',views.livefeed, name='livefeed'),
    path('login/',views.login, name='login')
]