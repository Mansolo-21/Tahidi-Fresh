from django.urls import path
from .views import(create_request,request_list,assign_workers,request_detail,update_status)
urlpatterns = [
    path("new/",create_request,name="create_request"),
    path("my-requests/",request_list,name="request_list"),
    path("assign/<int:pk>/",assign_workers,name="assign_workers"),
    path("request/<int:pk>/",request_detail,name="request_detail"),
    path("request/<int:pk>/status/<str:status>/",update_status,name="update_status"),
]