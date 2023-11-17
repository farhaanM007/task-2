from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class Task(models.Model):
    """
    Model for tasks in the todo app
    
    """

    title=models.CharField(max_length=30)
    content=models.TextField()
    completion_status=models.BooleanField(default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
