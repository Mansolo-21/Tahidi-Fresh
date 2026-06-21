from django.urls import path
from .views import home,dashboard,owner_dashboard,shopper_dashboard,rider_dashboard

urlpatterns =[
    path("",home, name="home"),
    path("dashboard",dashboard,name="dashboard"),
    path(
    "owner-dashboard/",
    owner_dashboard,
    name="owner_dashboard"
),path("shopper_dashboard/",shopper_dashboard,name="shopper_dashboard"),
    path("rider_dashboard",rider_dashboard,name="rider_dashboard")
]