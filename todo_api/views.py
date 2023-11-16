from django.shortcuts import render
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
def listtasks(request):
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
def createTask(request):
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
def taskDetail(request, pk):
    user = request.user.id
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
def updateTask(request, pk):
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
def deleteTask(request,pk):
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





