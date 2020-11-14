"""day86 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from learn import views
from rest_framework.routers import SimpleRouter
route = SimpleRouter()
route.register('book',views.Book,basename='book')
# route.register('publish',views.Publish,basename='publish')
# route.register('user',views.User,basename='user')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.Login.as_view()),
]
urlpatterns += route.urls