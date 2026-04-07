from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('student/profile/', views.student_profile, name='student_profile'),
    # path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # path('post_login_redirect/', views.post_login_redirect, name='post_login_redirect'),
]