from rest_framework.decorators import APIView
from django.contrib.auth import authenticate
from rest_framework import status,generics
from rest_framework.response import Response
from .serializers import SignupSerializer
from .models import User
from rest_framework.decorators import authentication_classes, permission_classes
from  .tokens import create_jwt_pair_for_user
from rest_framework.permissions import IsAuthenticated

@authentication_classes([])
@permission_classes([])
class SignupView(generics.GenericAPIView):

    serializer_class=SignupSerializer

    def post(self,request):

        data=request.data
        serializer=self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response={
                "message":"User added Successfully",
                "data":serializer.data
            }

            return Response(data=response,status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([])
@permission_classes([])
class LoginView(APIView):

    def post(self,request):
        email=request.data.get("email")
        password=request.data.get("password")

        user=authenticate(email=email,password=password)

        if user is not None:
            tokens=create_jwt_pair_for_user(user)
            response={
                "message":"login is successful",
                "tokens":tokens
            }

            return Response(data=response,status=status.HTTP_200_OK)
        
        else:
            return Response(data={"message":"Invalid User"})


