from django.urls import path
from bookmark.views import *

urlpatterns = [
    path('bookmark/', bookmark_list),
    path('bookmark2/', bookmark_list2),
    path('bookmark2/<int:pk>/', bookmark_detail),

]