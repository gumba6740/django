from django.shortcuts import render
from django.http import HttpResponse, Http404

from bookmark.models import Bookmark


def bookmark_list(request):
    return HttpResponse("<h1>북마크 리스트 페이지입니다</h1>")

def bookmark_list2(request):
    bookmarks = Bookmark.objects.all()
    context = {
        'bookmarks': bookmarks,

    }
    return render(request, 'bookmark_list.html', context)

def bookmark_detail(request, pk):
    try:
        bookmark = Bookmark.objects.get(pk=pk)
    except:
        raise Http404

    context = {
        'bookmark': bookmark,
    }
    return render(request, 'bookmark_detail.html', context=context)