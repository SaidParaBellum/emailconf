from django.urls import path

from my_app.views import ForgotPasswordView, ProfileView, RegisterView, LoginView, CodeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('send_code/', CodeView.as_view(), name='send_code'),
]