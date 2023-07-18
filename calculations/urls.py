from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("one-sample/", views.one_sample, name="one-sample"),
    path("two-sample/", views.two_sample, name="two-sample")

]