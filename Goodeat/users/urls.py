from django.contrib.auth.views import LogoutView

from users.views import *
from django.urls import path


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]