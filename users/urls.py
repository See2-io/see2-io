from django.urls import path

from . import views

urlpatterns = [
    path('', views.my_profile, name='my_profile'),
    path('my_profile/', views.my_profile, name='my_profile'),
    # path('<int:pk>/', views.DetailView.as_view(), name='profile'),
]
