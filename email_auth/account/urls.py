from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from account.views import signupView, UserVerificationView

app_name='account'

urlpatterns = [
    path('signup/', views.signupView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<pk>/verify/<token>/', UserVerificationView.as_view()),
]
