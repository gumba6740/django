from restaurants.views import *
from django.urls import path
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)

urlpatterns = [

] + router.urls
