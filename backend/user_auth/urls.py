from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('password-forget/', views.PasswordForget.as_view(), name='password-forget'),
    path('password-forget/<uuid:token>/', views.PasswordReset.as_view(), name='password-reset'),
]
