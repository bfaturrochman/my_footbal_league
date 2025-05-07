from django.urls import path
from . import views

urlpatterns = [
    path('', views.standings_view, name='standings'),
    path('add-team/', views.add_team_view, name='add_team'),
    path('add-match/', views.add_match_view, name='add_match'),
    path('register/', views.register_view, name='register'),
    path('reset-confirm/', views.reset_confirm_view, name='reset_confirm'),
    path('reset-all/', views.reset_all_view, name='reset_all'),
]
