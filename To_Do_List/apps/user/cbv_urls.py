from django.urls import path
from apps.user.cbvs import *


app_name = 'cbv_user'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]