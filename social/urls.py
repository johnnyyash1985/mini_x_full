from django.urls import path
from . import views

urlpatterns = [
    path('follow/<str:username>/', views.follow_toggle, name='follow_toggle'),
]
