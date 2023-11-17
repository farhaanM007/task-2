from django.db import models
from django.db.models import Model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

class CustomUserManager(BaseUserManager):
    def create_user(self,email:str,password:str,**extra_fields)->Model:
        """
        Creates and saves a regular user 

        Args:
        -email:Email address of user of type string
        -password:password of user og type string
        -**extrs_field:Additional fields

        Returns:
        -Model instance of the created user

        """
        email=self.normalize_email(email)

        user=self.model(email=email,**extra_fields)

        user.set_passwor(password)

        user.save()

        return user
    
    def create_superuser(self,email:str,password:str,**extra_fields)->Model:
        """
        Creates and saves a superuser

        Args:
        - email: Email address of the superuser of type string.
        - password: Password for the superuser of type string.
        - **extra_fields: Additional fields.

        Returns:
        - Model: Instance of the created superuser.

        """
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("is_staff should be true")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("is_superuser should be true")
        
        return self.create_user(password=password,email=email,**extra_fields)


class User(AbstractUser):
    """
    Custom user model that uses email as a unique identifier for authentication

    """

    email=models.CharField(max_length=50,unique=True)
    username=models.CharField(max_length=20)

    objects=CustomUserManager()

    USERNAME_FIELD="email"

    REQUIRED_FIELDS=["username"]

    def __str__(self) -> str:
        return self.username


