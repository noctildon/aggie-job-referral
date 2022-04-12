from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('login/',loginUser,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('registerrecruiter/',registerRecruiter,name='registerrecruiter'),
    path('registercandidate/',registerCandidate,name='registercandidate'),
    path('post/',PostPage,name='post'),
    path('hrapplicants/', hrApplicants, name='hrapplicants'),
    path('hrapplicants/resumes', pdf_view, name='pdfview'),
    path('hrapplicants/edit', Edit, name='edit'),
    path('requestref/', RequestPage, name='requestref'),
]