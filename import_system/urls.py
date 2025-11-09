"""
URL configuration for import_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect
#from accounts.admin import admin_site 
from rest_framework_simplejwt.views import TokenObtainPairView
from masters.views import MyTokenObtainPairView
#from masters.views import bank_dashboard  # adjust import if needed
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('accounts/', include('accounts.urls')),
    path('', include('masters.urls')), 

    #path('leave-management/', include('leave_management.urls')),
    path('', lambda request: redirect('login')),  # Redirect root URL to login
    
    #path('', include('masters.urls')),  # Include the masters app URLs
    #('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    

    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
   # path('api/bank-dashboard/', bank_dashboard, name='bank_dashboard'),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
