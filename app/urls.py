from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='login'),
    path('register/', views.register_user, name='register'),
    path('home', views.HomeListView.as_view(), name="home"),
    path('form/', views.form, name='form'),
]
