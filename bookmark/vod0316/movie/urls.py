from django.urls import path
from vod0316.movie.views import *

urlpatterns = [
    path('', movies),
    path('<int:index>', movie_detail)
]