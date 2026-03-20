from django.urls import path
from apps.user.views import *

app_name = 'user'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
]