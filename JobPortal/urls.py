from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('login/',loginUser,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('registerrecruiter/',registerRecruiter,name='registerrecruiter'),
    path('registercandidate/',registerCandidate,name='registercandidate'),
    path('apply/',applyPage,name='apply'),
    path('post/',PostPage,name='post'),
]