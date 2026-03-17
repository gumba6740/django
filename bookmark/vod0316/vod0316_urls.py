from django.urls import path, include

urlpatterns = [
    path('books/', include("vod0316.book.urls")),
    path('movies/', include("vod0316.movie.urls")),
    path('movies2/', include("vod0316.movie2.urls")),
    path('gugu/', include("vod0316.gugu.urls")),
]