from django.http import HttpResponse



def index(request):
    return HttpResponse('hello')


def book_list(request):
    book_text = ''

    for i in range(0, 10):
        book_text += f'book {i}<br>'

    return HttpResponse(book_text)


def book(request, num):
    book_text = f'book {num}번 페이지입니다'
    return HttpResponse(book_text)


def language(request, lang):
    return HttpResponse(f'<h1>{lang} 언어 페이지입니다</h1>')