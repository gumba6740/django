from django.http import HttpResponse, Http404

movie_list = [
    {'title': '파묘', 'director': '장재현'},
    {'title': '웡카', 'director': '폴 킹'},
    {'title': '듄: 파트 2', 'director': '드니 빌뇌브'},
    {'title': '시민덕희', 'director': '박영주'},

]

def movies(request):
    movie_titles = [movie['title'] for movie in movie_list]
    response_text = ''
    # response_text = '<br>'.join(movie_titles)
    for i, movie in enumerate(movie_titles):
        response_text += f'<h1><a href="/movies/{i}">{movie}</a></h1><br>'


    return HttpResponse(response_text)


def movie_detail(request, index):

    if index > len(movie_list) - 1:
        raise Http404

    movie = movie_list[index]
    response_text = f'<h1>{movie["title"]}</h1> <p>감독: {movie["director"]}</p>'

    return HttpResponse(response_text)