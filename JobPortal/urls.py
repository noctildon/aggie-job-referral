from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('',home,name='home'),
    path('login/',loginUser,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('registerrecruiter/',registerRecruiter,name='registerrecruiter'),
    path('registercandidate/',registerCandidate,name='registercandidate'),
    path('post/',PostPage,name='post'),
    path('hrapplicants/', hrApplicants, name='hrapplicants'),
    path('resumes/', pdf_view, name='pdfview'),
    path('hrapplicants/resumes', pdf_view, name='pdfview'),
    path('hrapplicants/edit', Edit, name='edit'),
    path('requestref/', RequestPage, name='requestref'),
    path('dashboard/', Dashboard, name='dashboard'),
    path('changepwd/', ChangePwd, name='changepwd'),

    # Password reset by email
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset_done',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
]