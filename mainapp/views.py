#python
import json
import cv2
import numpy as np
from PIL import Image
import base64 
import io
#django
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import User

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView)

from .serializers import UserSerializer,UserSerializerGet

class getUsers(ListAPIView):
    serializer_class = UserSerializerGet

    def get_queryset(self):
        return User.objects.all()

class createUser(APIView):
    parser_classes = [MultiPartParser]
    def post(self,request,format=None):
        nombre= request.data['nombre']
        apellido= request.data['apellido']
        email=request.data['email']
        file_obj = request.data['firma']
       
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def hello(request):
    users= [user.nombre for user in User.objects.all()]
    return Response(users)


def getImage(id_user):
    user = User.objects.get(id=id_user)
    print("usuario",user)
    return user.firma.url
    



class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        print(request.data)
        id_user=request.data['user']
        file_obj = request.data['firma']
        
        firma_user= getImage(id_user)
        firma_original="."+str(firma_user)
        
        # convertir la imagen que recibimos
        imgdata = base64.b64decode(str(file_obj))
        img = Image.open(io.BytesIO(imgdata))
        img = img.convert('RGB')
        # img=Image.open(file_obj).convert('RGB')
        template=cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        original = cv2.imread(firma_original)
        #resizing images
        template = cv2.resize(template,(528,152))
        #cv2.imshow("template image", template)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        template.shape #row.columns
        original = cv2.resize(original,(528,152))
        #cv2.imshow("original image", original)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        #ORB Detector
        orb = cv2.ORB_create()

        original = cv2.Canny(original, 50, 200)
        template = cv2.Canny(template, 50, 200)

        # key points and descriptor calculation
        kp1, desc_1 = orb.detectAndCompute(template, None)
        kp2, desc_2 = orb.detectAndCompute(original, None)

        #creating matches
        matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)
        matches_1 = matcher.knnMatch(desc_1, desc_2, 2)
        len(matches_1)

        result = cv2.drawMatchesKnn(original, kp1 , template, kp2, matches_1, None)
        #cv2.imshow("result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        #distance similarity
        good_points = []
        for m,n in matches_1:
            if m.distance < 0.8* n.distance:
                good_points.append(m)
        len(good_points)

        result = cv2.drawMatches(original, kp1 , template, kp2, good_points, None)
        #cv2.imshow("result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        #que tanto coinciden las firmas

        #res=5
        res=(len(kp1)/len(good_points))
        print(res)
        #calculating ratio
        print("How good is the match : ",res)
        # ...
        if res>11 or res<1:
            return Response({"0"})
        else:
            return Response({"1"})
