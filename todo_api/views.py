from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Task
from .serializers import TaskSerializer,TaskUpdateSerializer
from rest_framework import status,mixins,generics
from rest_framework.exceptions import NotFound
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import AuthorOrReadOnly,IsOwnerReadOnly


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def listtasks(request:Request)->Response:
    """
    Retrieve a list of task associated with logged in user

    Args:
    - request: Request object from rest_framework.request

    Returns:
    -Response containing a list of tasks belonging to the logged-in user
    -If no tasks are found returns a message indicating no tasks exist
    
    """
    tasks=Task.objects.order_by('id')
    user=request.user.id
    filter_tasks=tasks.filter(user=user)
    if tasks:

        serializer=TaskSerializer(instance=filter_tasks,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    else:
        return Response(data={"message":"No Tasks Created"},status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def createTask(request:Request)->Response:
    """
    Creates a new task for logged-in user

    Args:
    - request: Request object from rest_framework.request

    Response:
    -Response containing details of the new task
    -if issues in the posting body,returns a message indicating errors
    
    """
    data=request.data
    user=request.user
    data['user']=user.id
    serializer=TaskSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        response={
            "message":"Task Created",
            "data":serializer.data
        }
        return Response(data=response,status=status.HTTP_201_CREATED)
    
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def taskDetail(request:Request, pk:str)->Response:
    """
    Retrives details of a specific task of the logged in user

    Args:
    -request: Request object from rest_framework.request
    -pk:primary key of a particular task og type string

    Response:
    -Response containing details of the task
    -If the Task does not exist,response will be a message indicating this issue
    -If the user does not have permission,response will be a message indicating this issue

    """
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        raise NotFound(detail="Task Not found", code=status.HTTP_404_NOT_FOUND)
    
    permission_checker = IsOwnerReadOnly()
    has_permission = permission_checker.has_object_permission(request, None, task)

    if not has_permission:
        return Response(
            {"message": "You don't have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )
    else:
        serializer = TaskSerializer(instance=task)
        response = {
            "Task": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(["PUT"])
def updateTask(request:Request, pk:str)->Response:
    """
    Update a specific task of logged-in user

    Args:
    -request: Request object from rest_framework.request
    -pk:primary key of a particular task og type string

    Response:
    -Response containing updated details of the task
    -If the Task does not exist,response will be a message indicating this issue
    -If the user does not have permission,response will be a message indicating this issue

    """
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        raise NotFound(detail="Task not found", code=status.HTTP_404_NOT_FOUND)

    if not AuthorOrReadOnly().has_object_permission(request, None, task):
        return Response(
            {"message": "You don't have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = TaskUpdateSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()
        response = {
            "message": "Task Updated",
            "Task": serializer.data
        }
        return Response(data=response, status=status.HTTP_202_ACCEPTED)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def deleteTask(request:Request,pk:str)->Response:
    """
    Delete a specific task of logged-in user

    Args:
    -request: Request object from rest_framework.request
    -pk:primary key of a particular task og type string

    Response:
    -Response message saying the task is deleted
    -If the Task does not exist,response will be a message indicating this issue
    -If the user does not have permission,response will be a message indicating this issue

    """
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        raise NotFound(detail="Task not found", code=status.HTTP_404_NOT_FOUND)

    if not AuthorOrReadOnly().has_object_permission(request, None, task):
        return Response(
            {"message": "You don't have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )
        
    task.delete()
    return Response(data={"Task Deleted"},status=status.HTTP_200_OK)





