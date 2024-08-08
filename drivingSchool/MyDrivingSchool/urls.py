from django.urls import path 
from . import views

# app_name = 'MyDrivingSchool'

urlpatterns = [
    path('', views.index, name='index'), # /home
    # path('add_profil/', views.add_profil, name = 'add_profil'),
    # path('delete_profil/', views.delete_profil, name= 'delete_profil'),
    # path('register/', views.register, name = 'register'),
    path('add_users_to_planning/', views.add_users_planning, name='add_planning'),
    path('planning/', views.show_rdv, name="planning"),
    path('change_status/', views.change_user_group, name='group'),

    path('<str:user_name>/', views.show, name='show') # /username
    # path('<int:user_id>/', views.show, name='show') # /user_id
]