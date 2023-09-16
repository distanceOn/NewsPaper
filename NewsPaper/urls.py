"""
URL configuration for NewsPaper project.

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
from django.urls import include, path
from news import views
from allauth.account.views import LoginView, LogoutView, SignupView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
    path('news/search/', views.news_search, name='news_search'),
    path('news/add/', views.PostCreateView.as_view(), name='add_post'),
    path('news/<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('news/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
    path('accounts/', include('allauth.urls')),

]
