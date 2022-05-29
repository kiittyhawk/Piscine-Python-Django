from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('articles/', views.Articles.as_view(), name='articles'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.logout_Us, name='logout'),
    path('articles/<slug:pk>/', views.Detail.as_view(), name='articles_detail'),
    path('favourites/', views.Favourites.as_view(), name='favourites'),
    path('publish/', views.CreateArticle.as_view(), name='publish'),
]