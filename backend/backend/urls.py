from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ind),
    path('home/', views.home, name='home'),
    path('more/', views.more, name='more'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('security/', views.security, name='security'),
    path('notifications/', views.notifications, name='notifications'),
    path('notification/read/<int:id>/', views.mark_notification_read, name='mark_read'),
    path('notifications/clear/',views.clear_notifications,name='clear_notifications'),
]