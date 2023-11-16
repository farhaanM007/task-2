from .views import listtasks,createTask,updateTask,taskDetail,deleteTask
from django.urls import path

urlpatterns=[
    path('tasklist/',listtasks,name="todolist"),
    path('create/',createTask,name="create-task"),
    path('update/<str:pk>/',updateTask,name="udapte-task"),
    path('task/<str:pk>/',taskDetail,name="task-detail"),
    path('delete/<str:pk>/',deleteTask,name="delete-task"),

]