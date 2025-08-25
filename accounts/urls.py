from django.urls import path
from . import views
#from accounts.views import signup
#from accounts.views import approve_users

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Login route
    path('logout/', views.logout_view, name='logout'),  # Logout route
    path('', views.home, name='home'),  # Home page route after login   

    #path('api-login/', views.api_login_view, name='api_login'),

   
        
]
