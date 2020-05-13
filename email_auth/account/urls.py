from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name='account'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('<pk>/verify/<token>/', views.UserVerificationView.as_view(), name='verify'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
]
