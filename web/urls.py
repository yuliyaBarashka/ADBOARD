from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('ads/', views.ad_list, name='ad-list'),
    path('ads/create/', views.ad_create, name='ad-create'),
    path('ads/<int:pk>/', views.ad_detail, name='ad-detail'),
    path('ads/<int:pk>/edit/', views.ad_update, name='ad-update'),
    path('ads/<int:pk>/delete/', views.ad_delete, name='ad-delete'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
