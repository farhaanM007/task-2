from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        email=self.normalize_email(email)

        user=self.model(email=email,**extra_fields)

        user.set_passwor(password)

        user.save()

        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("is_staff should be true")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("is_superuser should be true")
        
        return self.create_user(password=password,email=email,**extra_fields)


class User(AbstractUser):
    email=models.CharField(max_length=50,unique=True)
    username=models.CharField(max_length=20)

    objects=CustomUserManager()

    USERNAME_FIELD="email"

    REQUIRED_FIELDS=["username"]

    def __str__(self) -> str:
        return self.username


