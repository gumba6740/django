from django.urls import path
from apps.users.views import *

app_name = 'users'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
]