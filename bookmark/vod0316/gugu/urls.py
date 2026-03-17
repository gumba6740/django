from django.urls import path
from vod0316.gugu.views import *

urlpatterns = [
    path('', gugudan),
    path('<int:number>/', gugudan2)
]