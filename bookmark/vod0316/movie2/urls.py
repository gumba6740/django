from django.urls import path
from vod0316.movie2.views import *

urlpatterns = [
    path('', movies),
    path('<int:index>', movie_detail)
]