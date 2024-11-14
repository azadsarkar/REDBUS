# urls.py
from django.urls import path, include
from .views import (
    CustomerRegistration,
    UserLogin,
    user_log_out,
    desh_bord,
    home,
    contact,
    UserUpdateView,
    UpdateTemplateView,
    UserDeleteViews,
)
from django.contrib.auth import views as auth_views
from bus_managment import views as bus_managment

app_name = ""
urlpatterns = [
    # path('accounts/login/',UserLogin.as_view(), name='login'),
    path("home/", home, name="home"),
    path("signup/", CustomerRegistration.as_view(), name="signup"),
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", user_log_out, name="user_logout"),
    path("dashbord/", bus_managment.home, name="deshbord"),
    path("contact/", contact, name="contact"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
    path("updateTemplatevie/", UpdateTemplateView.as_view(), name="templateView"),
    path("userdelete/<int:pk>/", UserDeleteViews.as_view(), name="deleteview"),
    path(
        "change_password/",
        auth_views.PasswordChangeView.as_view(
            template_name="account/change_password.html", success_url="/"
        ),
        name="change_password",
    ),
    path(
        "forgate_password/",
        auth_views.PasswordResetView.as_view(
            template_name="account_reset_pass/reset_password1.html",
            success_url="/reset_password_sent/",
        ),
        name="forgate_password",
    ),
    
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account_reset_pass/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account_reset_pass/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account_reset_pass/password_reset.html"
        ),
        name="password_reset_complete",
    ),
]
