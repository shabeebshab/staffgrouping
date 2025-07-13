
from django.urls import path
from . import views

urlpatterns = [
    path('', views.paste_view, name='paste'),
    path('groups/', views.group_view, name='groups'),
    path('remove/<int:member_id>/', views.remove_staff, name='remove_staff'),

    
 
]
