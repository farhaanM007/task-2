from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model=Task
        fields=['id','title','content','completion_status','user']

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'content', 'completion_status']
        read_only_fields = ['user']  # Exclude 'user' from writable fields




