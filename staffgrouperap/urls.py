
from django.urls import path
from . import views

urlpatterns = [
    path('', views.paste_view, name='paste'),
    path('groups/', views.group_view, name='groups'),
    
 
]
