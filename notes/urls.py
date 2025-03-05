# notes/urls.py
from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('create/', views.note_create, name='note_create'),
    path('<int:pk>/update/', views.note_update, name='note_update'),
    path('<int:pk>/delete/', views.note_delete, name='note_delete'),
]