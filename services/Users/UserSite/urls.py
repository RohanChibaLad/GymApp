"""
URL configuration for UserSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from UserApp.views import get_CSRF_token  # Importing the view to get CSRF token
from UserApp.views import user  # Importing the user view to handle user actions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_csrf_token/', get_CSRF_token, name='get_csrf_token'),
    path('user/', user, name='user'),  # URL for user actions
]
