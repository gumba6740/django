from django.http import Http404
from django.shortcuts import render

movie_list = [
    {'title': '파묘', 'director': '장재현'},
    {'title': '웡카', 'director': '폴 킹'},
    {'title': '듄: 파트 2', 'director': '드니 빌뇌브'},
    {'title': '시민덕희', 'director': '박영주'},

]

def movies(request):

    return render(request, 'movie2_movies.html', {'movie_list': movie_list})


def movie_detail(request, index):

    if index > len(movie_list) - 1:
        raise Http404

    movie = movie_list[index]


    return render(request, 'movie2_movie_detail.html', {'movie': movie})