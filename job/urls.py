from django.urls import path , include
from .import views

urlpatterns = [
    path('jobs/', views.job_list, name='job_list'),
    path('<int:id>', views.job_detail, name='job_detail'),
]