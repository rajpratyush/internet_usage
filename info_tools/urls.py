from django.urls import path

from info_tools import views

urlpatterns = [

    path('analytics/', views.analytics, name="analytics"),
    path('user/search/', views.search, name="search"),

]
