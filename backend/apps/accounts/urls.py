from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views.auth import LoginView, LogoutView, ProfileView, RegisterView
from .views.email_verification import ResendVerificationView, VerifyEmailView
from .views.password_reset import ForgotPasswordView, PasswordResetConfirmView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("password/forgot/", ForgotPasswordView.as_view(), name="password_forgot"),
    path("password/reset/", PasswordResetConfirmView.as_view(), name="password_reset"),
    path("email/verify/", VerifyEmailView.as_view(), name="email_verify"),
    path("email/resend-verification/", ResendVerificationView.as_view(), name="email_resend_verification"),
]
