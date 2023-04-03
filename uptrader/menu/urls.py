from django.urls import path, re_path

from menu import views

urlpatterns = [
    path('', views.TestView.as_view(), name="general"),
]