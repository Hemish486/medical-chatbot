"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    admin_chat_history_view,
    chatbot,
    chat_history_view,
    delete_chat_history_view,
    export_chat_history_view,
    logout_view,
    privacy_notice_view,
    resend_verification_view,
    signup_view,
    verify_email_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', chatbot, name='chatbot'),
    path('signup/', signup_view, name='signup'),
    path('privacy/', privacy_notice_view, name='privacy_notice'),
    path('verify-email/<uidb64>/<token>/', verify_email_view, name='verify_email'),
    path('resend-verification/', resend_verification_view, name='resend_verification'),
    path('history/', chat_history_view, name='history'),
    path('history/export/', export_chat_history_view, name='history_export'),
    path('history/delete/', delete_chat_history_view, name='history_delete'),
    path('history/all/', admin_chat_history_view, name='history_all'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login',
    ),
    path('logout/', logout_view, name='logout'),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete',
    ),
]
