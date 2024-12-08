from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('index/', views.index, name='index'),
    path('manage/', views.manage, name='manage'),
    path('measure/', views.measure, name = 'measure'),
    path('minimize/', views.minimize, name='minimize'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('users/', views.fetch_users, name='fetch_users'),
    path('welcome/', views.welcome, name='welcome'),
    path('more-info/', views.more_info, name='more-info'),
    path('register/', views.register, name='register'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset-confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('add_activity/', views.add_activity, name='add_activity'),
    path('delete_activity/<int:id>/', views.delete_activity, name='delete_activity'),
    path('manage/<str:sub_category>/', views.manage_activity, name='manage_activity'),
    path('steps_to_minimize/<str:sub_category_name>/<str:case>/', views.steps_to_minimize, name='steps_to_minimize'),
]
