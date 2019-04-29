from django.shortcuts import render
from rest_framework.response import Response
from .models import Roles
from .serializers import Role_Serializer,SignUpSerializer,UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

#Get all Roles
class Roles_View(APIView):
    print ('inside role class')
    def get(self,request):
        roles=Roles.objects.all()
        serializer=Role_Serializer(roles,many=True)
        print (roles)
        return Response({'Roles':serializer.data})


class GetUser(APIView):
    def get(self,request):
        user=User.objects.all()
        serializer=UserSerializer(user,many=True)
        print (user)
        return Response({'Roles':serializer.data})


#Sign Up
class SignUp(APIView):
    print ("inside register")
    def post(self,request):
        print (request.data)
        serializer=SignUpSerializer(data=request.data)
        print (serializer)
        print("validation=",serializer.is_valid())
        if serializer.is_valid(raise_exception=True):
            print("saved")
            user=serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                print ("token key=",token.key)
                return Response(json, status=status.HTTP_201_CREATED)
            return Response({"massage":'Data saved successfully', "status":status.HTTP_201_CREATED})
        return Response({"massage":'Please check fields', "status":status.HTTP_400_BAD_REQUEST})
