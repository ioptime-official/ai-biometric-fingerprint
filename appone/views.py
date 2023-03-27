from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from appone.models import FileUpload,UploadMatch
from django.shortcuts import render
from .forms import RegistrationForm
from .forms import LoginForm
from django.http import JsonResponse
from .serializers import FingerprintSerializer, MatchSerializer
# from .models import UserProfile
import cv2
import os
import numpy as np
import io
from django.http import HttpResponse
import datetime
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status


def index(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        print("Before valid----------------------------")
        if form.is_valid():
            name_text = form.cleaned_data['name']
        
            print("------name---",name_text)
            # Check if the name already exists in the database
            existing_file = FileUpload.objects.filter(name_text=name_text).first()
            if existing_file:
                # If the name already exists, create a message to display to the user
                message = f"The name '{name_text}' already exists with the image '{existing_file.image.name}'. Please enter a different name."
                # Render the form with the message
                form.add_error('name', message)
            else:
                image = form.cleaned_data['image']
                print("-----image---",image)
                sample = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
                database_images = FileUpload.objects.all()
                for database_image in database_images:
                    database_image_name = database_image.name_text
                    # decode the database image and convert it to grayscale
                    fp_image  = cv2.imdecode(np.fromstring(database_image.image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

                    sift = cv2.SIFT_create()
                    kp_1, desc_1 = sift.detectAndCompute(sample, None)
                    kp_2, desc_2 = sift.detectAndCompute(fp_image, None)

                    index_params = dict(algorithm=0, trees=5)
                    search_params = dict()
                    flann = cv2.FlannBasedMatcher(index_params, search_params)
                    matches = flann.knnMatch(desc_1, desc_2, k=2)

                    good_points = []
                    for m, n in matches:
                        if m.distance < 0.6*n.distance:
                            good_points.append(m)

                    # Define how similar they are
                    number_keypoints = 0
                    if len(kp_1) <= len(kp_2):
                        number_keypoints = len(kp_1)
                    else:
                        number_keypoints = len(kp_2)
                    if (len(good_points) / number_keypoints)>0.97:
                        # If the uploaded image matches with an image in the database, create a message to display to the user
                        message = f"The fingerprint '{image.name}' matches with the fingerprint of '{database_image_name}'. Please enter a different fingerprint."
                        # Render the form with the message
                        form.add_error('image', message)
                        break
                else:
                    name = FileUpload(name_text=name_text, image=image)
                    name.save()
                    #JSON Response
                    data = {'message': 'Registered!', 'Username' : name_text}
                    return JsonResponse(data)             
    else:
        form = RegistrationForm()
    return render(request, 'appone/index.html', {'form': form})


def match(request):
    return render(request, 'appone/match.html')




#########################################THIS IS FOR MATCHING###############################################

def matching(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            # name_text = form.cleaned_data['name']
            image = form.cleaned_data['image']

            # Check if the name already exists in the database
            sample = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

            database_images = FileUpload.objects.all()
            for database_image in database_images:
                database_image_name = database_image.name_text
                # decode the database image and convert it to grayscale
                fp_image  = cv2.imdecode(np.fromstring(database_image.image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

                # if sample.shape == fp_image.shape:
                #     print("The images have same size and channels")
                #     difference = cv2.subtract(sample, fp_image)
                    # b, g, r = cv2.split(difference)
                    # if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    #     print("The images are completely Equal")
                    # else:
                    #     print("The images are NOT equal")

                # sift = cv2.xfeatures2d.SIFT_create()
                sift = cv2.SIFT_create()
                kp_1, desc_1 = sift.detectAndCompute(sample, None)
                kp_2, desc_2 = sift.detectAndCompute(fp_image, None)

                index_params = dict(algorithm=0, trees=5)
                search_params = dict()
                flann = cv2.FlannBasedMatcher(index_params, search_params)
                matches = flann.knnMatch(desc_1, desc_2, k=2)

                good_points = []
                for m, n in matches:
                    if m.distance < 0.6*n.distance:
                        good_points.append(m)

                # Define how similar they are
                number_keypoints = 0
                if len(kp_1) <= len(kp_2):
                    number_keypoints = len(kp_1)
                else:
                    number_keypoints = len(kp_2)
                if (len(good_points) / number_keypoints)>0.97:
                    # print("Keypoints 1ST Image: " + str(len(kp_1)))
                    # print("Keypoints 2ND Image: " + str(len(kp_2)))
                    # print("GOOD Matches:", len(good_points))
                    # print("How good it's the match: ", len(good_points) / number_keypoints * 100)
                    print("username---->>",database_image.name_text)
                    
                    data = {'message': 'Matched!', 'Username' : database_image.name_text}
                    return JsonResponse(data)      

            else:
                data = {'message': 'Not Matched!'}
                return JsonResponse(data)  
    else:
        form = LoginForm()
    return render(request, 'appone/matching.html', {'form': form})

########################################################################API#########################################################################

#Built APIs 

#API for Getting All User with their fingerprints + Adding new User
@api_view(['GET','POST'])
def FingerSerializer(request):
    if request.method == 'GET':
        temp = FileUpload.objects.all()
        serializer = FingerprintSerializer(temp, many=True)
        return JsonResponse({'FingerprintS':serializer.data,"STATUS":'Pass'})
# before adding new user check is same file exist or not
    if request.method == 'POST':
        serializer = FingerprintSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']

            # Check if the name already exists in the database
            sample = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

            database_images = FileUpload.objects.all()
            for database_image in database_images:
                database_image_name = database_image.image.name
                # decode the database image and convert it to grayscale
                fp_image  = cv2.imdecode(np.fromstring(database_image.image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

                # Compute SIFT keypoints and descriptors for both images
                sift = cv2.SIFT_create()
                kp_1, desc_1 = sift.detectAndCompute(sample, None)
                kp_2, desc_2 = sift.detectAndCompute(fp_image, None)

                # Use FLANN matcher to find matches between descriptors
                index_params = dict(algorithm=0, trees=5)
                search_params = dict()
                flann = cv2.FlannBasedMatcher(index_params, search_params)
                matches = flann.knnMatch(desc_1, desc_2, k=2)

                # Filter matches using the Lowe's ratio test
                good_points = []
                for m, n in matches:
                    if m.distance < 0.6 * n.distance:
                        good_points.append(m)

                # Compute the ratio of good matches to total keypoints
                number_keypoints = min(len(kp_1), len(kp_2))
                if number_keypoints > 0:
                    similarity_ratio = len(good_points) / number_keypoints
                else:
                    similarity_ratio = 0

                # If similarity ratio is above a threshold, return a match
                if similarity_ratio > 0.97:
                    data = {'message':'image already exist please chose different file','Image name':database_image_name}
                    return JsonResponse(data)

            # If no match was found, return a failure response
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)

        else:
            data = {'message': 'Invalid form data.'}
            return JsonResponse(data)

#API for Matching Fingerprints
@api_view(['GET', 'POST'])
def finger_serializer(request):
    if request.method == 'GET':
        # retrieve all objects from FileUpload model and serialize them
        temp = FileUpload.objects.all()
        serializer = MatchSerializer(temp, many=True)
        return JsonResponse({'FingerprintS': serializer.data, "STATUS": 'Pass'})

    elif request.method == 'POST':
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            # name_text = form.cleaned_data['name']
            image = serializer.validated_data['image']

            # Check if the name already exists in the database
            sample = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

            database_images = FileUpload.objects.all()
            for database_image in database_images:
                database_image_name = database_image.name_text
                # decode the database image and convert it to grayscale
                fp_image  = cv2.imdecode(np.fromstring(database_image.image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

                # Compute SIFT keypoints and descriptors for both images
                sift = cv2.SIFT_create()
                kp_1, desc_1 = sift.detectAndCompute(sample, None)
                kp_2, desc_2 = sift.detectAndCompute(fp_image, None)

                # Use FLANN matcher to find matches between descriptors
                index_params = dict(algorithm=0, trees=5)
                search_params = dict()
                flann = cv2.FlannBasedMatcher(index_params, search_params)
                matches = flann.knnMatch(desc_1, desc_2, k=2)

                # Filter matches using the Lowe's ratio test
                good_points = []
                for m, n in matches:
                    if m.distance < 0.6 * n.distance:
                        good_points.append(m)

                # Compute the ratio of good matches to total keypoints
                number_keypoints = min(len(kp_1), len(kp_2))
                if number_keypoints > 0:
                    similarity_ratio = len(good_points) / number_keypoints
                else:
                    similarity_ratio = 0

                # If similarity ratio is above a threshold, return a match
                if similarity_ratio > 0.97:
                    data = {'message': 'Matched!', 'Username': database_image.name_text}
                    return JsonResponse(data)

            # If no match was found, return a failure response
            data = {'message': 'No match found.'}
            return JsonResponse(data)

        else:
            data = {'message': 'Invalid form data.'}
            return JsonResponse(data)

#API fro deleting User by Username
@api_view(['GET'])
def delete_fp(request, name):

    try:
        fingerprint =  FileUpload.objects.get(name_text=name)
    except FileUpload.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        fingerprint.delete()
        data = {'message': 'Delete Sucessfuly'}
        return JsonResponse(data)