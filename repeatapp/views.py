from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import login,authenticate

from .serializers import RegisterSerializer,LoginSerializer
from .models import User

from rest_framework.permissions import AllowAny
#generates token.
from repeatproj import settings
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
import jwt



# Create your views here.
class RegisterView(APIView):
    permission_class=[AllowAny,]
    def post(self,request):
        try:
            user=User.objects.get(email=request.data['email'])    #returns mail that is to be entered.
            return Response({"data":None,"message":"Email Already Exist"},status=status.HTTP_400_BAD_REQUEST)
        except:
            data=request.data.copy()         #returns queryset of given object(user) which is to be registred.
            # print(data)
            data['email']=request.data['email'].lower()      #return a (dictionary)queryset and Lower case of email field.
            serializer=RegisterSerializer(data=data)         #returns all fields of serializers with data that are filled by user.
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_class=[AllowAny,]

    def post(self,request):
        if "email" in request.data and "password" in request.data:
            email=request.data['email']
            # print(email)
            email=email.lower()
            password=request.data['password']
            # print(password)
            try:
                user=User.objects.get(email=email)
                # print(user)
            except User.DoesNotExist:
                return Response({"data":None,"message":"user does not exist"},status=status.HTTP_BAD_REQUEST)
            if user.check_password(password):
                login(request,user)
                serializer=LoginSerializer(user)
                # print(serializer)
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                # print(token)
                user_details=serializer.data
                print(user_details)
                user_details['token']=token
                # print(user_details)
                return Response(
                    {"data":user_details,
                     "code":status.HTTP_200_OK,
                      "message":"Login Successfully",},
                      status=status.HTTP_200_OK
                ) 
        else:
            return Response({"data":None,
                              "code":status.HTTP_400_BAD_REQUEST,
                               "message":"invalid credentials",},
                               status=status.HTTP_400_BAD_REQUEST)
            


        