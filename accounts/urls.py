from django.urls import path
from . import views
from masters.views import MyTokenObtainPairView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


urlpatterns = [

    # 🔐 Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),

    # 🔑 JWT Token
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 🔒 Change Password
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/change_password.html',
            success_url=reverse_lazy('password_change_done')
        ),
        name='change_password'
    ),

    path(
        'change-password/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/change_password_done.html'
        ),
        name='password_change_done'
    ),
]
