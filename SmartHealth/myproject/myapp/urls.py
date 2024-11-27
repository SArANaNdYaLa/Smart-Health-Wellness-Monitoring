from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('features/', views.features, name='features'),
    path('healthinsights/', views.healthinsights, name='healthinsights'),
    path('wellnesstracking/', views.wellnesstracking, name='wellnesstracking'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('visualizations/', views.visualizations, name='visualizations'),
    path('set_goals/', views.set_goals, name='set_goals'),
    path('goals/', views.goals_page, name='goals_page'),
]