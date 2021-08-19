from django.urls import path
from django.contrib import auth
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/', auth.views.LoginView.as_view(template_name='authn/login.html'), name="login"),
    url(r'^logout/', auth.views.LogoutView.as_view(), name="logout"),
    url(r'^password_change/done/', auth.views.PasswordChangeDoneView.as_view(template_name='authn/password_change_done.html'), name="password_change_done"),
    url(r'^password_change/', auth.views.PasswordChangeView.as_view(template_name='authn/password_change_form.html'), name="password_change"),
    url(r'^password_reset/', auth. views.PasswordResetView.as_view(template_name='authn/password_reset_form.html'), name="password_reset"),
    url(r'^password_reset/done/', auth.views.PasswordResetDoneView.as_view(template_name='authn/password_reset_done.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth.views.PasswordResetConfirmView.as_view(template_name='authn/password_reset_confirm.html'), name="password_reset_confirm"),
    url(r'reset/done/', auth.views.PasswordResetCompleteView.as_view(template_name='authn/password_reset_complete.html'), name="password_reset_complete"),
    url(r'register/', views.RegisterView.as_view(), name="register")
]
