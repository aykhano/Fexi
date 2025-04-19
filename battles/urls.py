from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('arena/', views.arena, name='arena'),
    path('start-battle/', views.start_battle, name='start_battle'),
    path('battle/<int:battle_id>/question/<int:question_num>/', views.get_question, name='get_question'),
    path('battle/<int:battle_id>/question/<int:question_num>/submit/', views.submit_answer, name='submit_answer'),
    path('battle/<int:battle_id>/complete/', views.complete_battle, name='complete_battle'),
]