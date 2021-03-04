from django.urls import path
from . import views

urlpatterns = [
    path('good_change/', views.good_change, name="good_change"),

]
