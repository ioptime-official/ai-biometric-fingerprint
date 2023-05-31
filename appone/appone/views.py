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
import threading
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from functools import partial
import time
import io
from django.http import HttpResponse
import datetime
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
import logging


import time

def index(request):
    start_time = time.time()
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        print("Before valid----------------------------")
        if form.is_valid():
            name_text = form.cleaned_data['name']
            # Check if the name already exists in the database
            existing_file = FileUpload.objects.filter(name_text=name_text).first()
            if existing_file:
                # If the name already exists, create a message to display to the user
                message = f"The name '{name_text}' already exists with the image '{existing_file.image.name}'. Please enter a different name."
                # Render the form with the message
                form.add_error('name', message)
            else:
                image = form.cleaned_data['image']
                sample = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
                database_images = FileUpload.objects.all()
                for database_image in database_images:
                    database_image_name = database_image.name_text
                    # decode the database image and convert it to grayscale
                    fp_image  = cv2.imdecode(np.fromstring(database_image.image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

                    orb = cv2.ORB_create()
                    kp_1, desc_1 = orb.detectAndCompute(sample, None)
                    kp_2, desc_2 = orb.detectAndCompute(fp_image, None)


                    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                    matches = bf.match(desc_1,desc_2)

                    good_points = []
                    for m in matches:
                        if m.distance < 20:
                            good_points.append(m)

                    # Define how similar they are
                    number_keypoints = 0
                    if len(kp_1) <= len(kp_2):
                        number_keypoints = len(kp_1)
                    else:
                        number_keypoints = len(kp_2)
                    if (len(good_points) / number_keypoints)>0.30:
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

        end_time = time.time()
        print(f"Time taken by index function: {end_time - start_time} seconds")

    else:
        form = RegistrationForm()
    return render(request, 'appone/index.html', {'form': form})


def match(request):
    return render(request, 'appone/match.html')




#########################################THIS IS FOR MATCHING###############################################


########################ORB#########################################
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from django.http import JsonResponse
from django.shortcuts import render
from .forms import LoginForm
from .models import FileUpload
import time


def matching(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']

            # Check if the name already exists in the database
            sample = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
            name = UploadMatch(image=image)
            name.save()

            database_images = FileUpload.objects.all()

            start_time = time.time()

            # def match_image(database_image):
            #     database_image_name = database_image.name_text
            #     # decode the database image and convert it to grayscale
            #     fp_image  = cv2.imdecode(np.fromstring(database_image.image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

            #     orb = cv2.ORB_create()
            #     kp_1, desc_1 = orb.detectAndCompute(sample, None)
            #     kp_2, desc_2 = orb.detectAndCompute(fp_image, None)

            #     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            #     matches = bf.match(desc_1,desc_2)

            #     good_points = []
            #     for m in matches:
            #         if m.distance < 50:
            #             good_points.append(m)

            #     # Define how similar they are
            #     number_keypoints = 0
            #     if len(kp_1) <= len(kp_2):
            #         number_keypoints = len(kp_1)
            #     else:
            #         number_keypoints = len(kp_2)
            #     if (len(good_points) / number_keypoints)>0.60:
            #         print("username---->>",database_image.name_text)
                    
            #         data = {'message': 'Matched!', 'Username' : database_image.name_text}
            #         return data      

            #     else:
            #         data = {'message': 'Not Matched!'}
            #         return data 

            def match_image(database_image):
                database_image_name = database_image.name_text
                # decode the database image and convert it to grayscale
                fp_image  = cv2.imdecode(np.fromstring(database_image.image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

                # create AKAZE object
                akaze = cv2.AKAZE_create()

                # detect and compute keypoints and descriptors using AKAZE
                kp_1, desc_1 = akaze.detectAndCompute(sample, None)
                kp_2, desc_2 = akaze.detectAndCompute(fp_image, None)

                # create BFMatcher object and match descriptors
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(desc_1,desc_2)

                # filter good matches based on distance
                good_points = []
                for m in matches:
                    if m.distance < 90:
                        good_points.append(m)

                # calculate similarity score and return result
                number_keypoints = min(len(kp_1), len(kp_2))
                similarity_score = len(good_points) / number_keypoints
                print("similarity ratio------------------------->>>>>>>>>>>>", similarity_score)
                if similarity_score > 0.10:
                    print("username---->>",database_image.name_text)
                    data = {'message': 'User Matched!', 'Username' : database_image.name_text}
                else:
                    data = {'message': 'Not Matched!'}
                return data

            # def match_image(database_image):
            #     database_image_name = database_image.name_text
            #     # decode the database image and convert it to grayscale
            #     fp_image = cv2.imdecode(np.fromstring(database_image.image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

            #     # create SIFT object
            #     # sift = cv2.xfeatures2d.SIFT_create()
            #     sift = cv2.xfeatures2d.SIFT_create()


            #     # detect and compute keypoints and descriptors using SIFT
            #     kp_1, desc_1 = sift.detectAndCompute(sample, None)
            #     kp_2, desc_2 = sift.detectAndCompute(fp_image, None)

            #     # create BFMatcher object and match descriptors
            #     bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
            #     matches = bf.match(desc_1, desc_2)

            #     # filter good matches based on distance
            #     good_points = []
            #     for m in matches:
            #         if m.distance < 90:
            #             good_points.append(m)

            #     # calculate similarity score and return result
            #     number_keypoints = min(len(kp_1), len(kp_2))
            #     similarity_score = len(good_points) / number_keypoints
            #     print("similarity ratio------------------------->>>>>>>>>>>>", similarity_score)
            #     if similarity_score > 0.10:
            #         print("username---->>",database_image.name_text)
            #         data = {'message': 'Matched!', 'Username' : database_image.name_text}
            #     else:
            #         data = {'message': 'Not Matched!'}
            #     return data



            with ThreadPoolExecutor(max_workers=1) as executor:
                results = list(executor.map(match_image, database_images))

            end_time = time.time()
            total_processing_time = end_time - start_time
            print(f"Total processing time: {total_processing_time:.2f} seconds")

            for result in results:
                if result['message'] == 'Matched!':
                    return JsonResponse(result)
            
            return JsonResponse({'message': 'Not Matched'})

            
    else:
        form = LoginForm()
    return render(request, 'appone/matching.html', {'form': form})



########################################################################API#########################################################################

#Built APIs 

# API for Getting All User with their fingerprints + Adding new User
    # @api_view(['GET','POST'])
    # def FingerSerializer(request):
    #     if request.method == 'GET':
    #         temp = FileUpload.objects.all()
    #         serializer = FingerprintSerializer(temp, many=True)
    #         return JsonResponse({'FingerprintS':serializer.data,"STATUS":'Pass'})
    # # before adding new user check is same file exist or not
    #     if request.method == 'POST':
    #         serializer = FingerprintSerializer(data=request.data)
    #         if serializer.is_valid():
    #             image = serializer.validated_data['image']

    #             # Check if the name already exists in the database
    #             sample = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

    #             database_images = FileUpload.objects.all()
    #             for database_image in database_images:
    #                 database_image_name = database_image.image.name
    #                 # decode the database image and convert it to grayscale
    #                 fp_image  = cv2.imdecode(np.fromstring(database_image.image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

    #                 # Compute ORB keypoints and descriptors for both images
    #                 orb = cv2.ORB_create()
    #                 kp_1, desc_1 = orb.detectAndCompute(sample, None)
    #                 kp_2, desc_2 = orb.detectAndCompute(fp_image, None)

    #                 # Use BF MATCHER matcher to find matches between descriptors
    #                 bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    #                 matches = bf.match(desc_1,desc_2)

    #                 # Filter matches using the Lowe's ratio test
    #                 good_points = []
    #                 for m in matches:
    #                     if m.distance < 50:
    #                         good_points.append(m)

    #                 # Compute the ratio of good matches to total keypoints
    #                 number_keypoints = min(len(kp_1), len(kp_2))
    #                 if number_keypoints > 0:
    #                     similarity_ratio = len(good_points) / number_keypoints
    #                 else:
    #                     similarity_ratio = 0

    #                 print("similarity ratio------------------------->>>>>>>>>>>>", similarity_ratio)
    #                 # If similarity ratio is above a threshold, return a match
    #                 if similarity_ratio > 0.30:
    #                     data = {"IsSuccess":False,'message':'image already exist please chose different file','Image name':database_image_name,"Username":database_image.name_text}
    #                     return JsonResponse(data,status=409)


    #             # If no match was found, return a failure response
    #             serializer.save()
    #             return Response(serializer.data , status=status.HTTP_201_CREATED)

    #         else:
    #             data = {'message': 'Invalid form data.'}
#             return JsonResponse(data)



@api_view(['GET', 'POST'])
def FingerSerializer(request):
    if request.method == 'GET':
        temp = FileUpload.objects.all()
        serializer = FingerprintSerializer(temp, many=True)
        return JsonResponse({'FingerprintS':serializer.data, "STATUS":'Pass'})

    if request.method == 'POST':
        serializer = FingerprintSerializer(data=request.data)
        if serializer.is_valid():
            # Get the username associated with the images
            name_text = serializer.validated_data['name_text']
            # Check if the name already exists in the database
            existing_file = FileUpload.objects.filter(name_text=name_text).first()
            if existing_file:
                # If the name already exists, create a message to display to the user
                message = f"The name '{name_text}' already exists with the image '{existing_file.image.name}'. Please enter a different name."
                # Render the form with the message
                data = {'message': 'name already exists.'}
                return JsonResponse(data)

            else:
                # Check if all three images have been uploaded
                images_uploaded = []
                for i in range(3):
                    image_field_name = f'image{i}'
                    if image_field_name in request.FILES:
                        images_uploaded.append(request.FILES[image_field_name])
                    else:
                        data = {"IsSuccess": False, 'message': 'Please upload all three images.'}
                        return JsonResponse(data, status=400)

                # Save the images for the new user
                for i, image_file in enumerate(images_uploaded):
                    sample = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

                    # Check if the image already exists in the database
                    database_images = FileUpload.objects.all()
                    for database_image in database_images:
                        database_image_name = database_image.image.name
                        #fp_image = cv2.imdecode(np.fromstring(database_image.image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

                        # Compute ORB keypoints and descriptors for both images
                        #orb = cv2.ORB_create()
                        #kp_1, desc_1 = orb.detectAndCompute(sample, None)
                        #kp_2, desc_2 = orb.detectAndCompute(fp_image, None)

                        # Use BF MATCHER matcher to find matches between descriptors
                        #bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                        #matches = bf.match(desc_1,desc_2)

                        # Filter matches using the Lowe's ratio test
                        #good_points = []
                        #for m in matches:
                        #    if m.distance < 50:
                        #        good_points.append(m)

                        # Compute the ratio of good matches to total keypoints
                        #number_keypoints = min(len(kp_1), len(kp_2))
                        #if number_keypoints > 0:
                        #    similarity_ratio = len(good_points) / number_keypoints
                        #else:
                        #    similarity_ratio = 0

                        #print("similarity ratio------------------------->>>>>>>>>>>>", similarity_ratio)
                        # If similarity ratio is above a threshold, return a match
                        #if similarity_ratio > 0.30:
                        #    data = {"IsSuccess": False, 'message': f'image {i} already exists for user {database_image_name}', "Image name": database_image_name}
                        #    return JsonResponse(data, status=409)

                    # Save the image to the database
                    FileUpload.objects.create(image=image_file, name_text=name_text)

                data = {'name_text': name_text, 'image': " "}
                return JsonResponse(data)
        else:
            data = {'message': 'Invalid form data.'}
            return JsonResponse(data)


# @api_view(['GET', 'POST'])
# def FingerSerializer(request):
#     if request.method == 'GET':
#         temp = FileUpload.objects.all(
#         serializer = FingerprintSerializer(temp, many=True)
#         return JsonResponse({'FingerprintS':serializer.data, "STATUS":'Pass'})

#     if request.method == 'POST':
#         serializer = FingerprintSerializer(data=request.data)
#         if serializer.is_valid():
#             # Get the username associated with the images
#             name_text = serializer.validated_data['name_text']

#             # Check if all three images have been uploaded
#             images_uploaded = []
#             for i in range(3):
#                 image_field_name = f'image{i}'
#                 if image_field_name in request.FILES:
#                     images_uploaded.append(request.FILES[image_field_name])
#                 else:
#                     data = {"IsSuccess": False, 'message': 'Please upload all three images.'}
#                     return JsonResponse(data, status=400)

#             # Save the images for the new user
#             saved_image = None
#             for i, image_file in enumerate(images_uploaded):
#                 sample = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

#                 # Check if the image already exists in the database
#                 database_images = FileUpload.objects.all()
#                 for database_image in database_images:
#                     database_image_name = database_image.image.name
#                     fp_image = cv2.imdecode(np.fromstring(database_image.image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

#                     # Compute ORB keypoints and descriptors for both images
#                     orb = cv2.ORB_create()
#                     kp_1, desc_1 = orb.detectAndCompute(sample, None)
#                     kp_2, desc_2 = orb.detectAndCompute(fp_image, None)

#                     # Use BF MATCHER matcher to find matches between descriptors
#                     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
#                     matches = bf.match(desc_1,desc_2)

#                     # Filter matches using the Lowe's ratio test
#                     good_points = []
#                     for m in matches:
#                         if m.distance < 50:
#                             good_points.append(m)

#                     # Compute the ratio of good matches to total keypoints
#                     number_keypoints = min(len(kp_1), len(kp_2))
#                     if number_keypoints > 0:
#                         similarity_ratio = len(good_points) / number_keypoints
#                     else:
#                         similarity_ratio = 0

#                     print("similarity ratio------------------------->>>>>>>>>>>>", similarity_ratio)
#                     # If similarity ratio is above a threshold, return a match
#                     if similarity_ratio > 0.30:
#                         data = {"IsSuccess": False, 'message': f'image {i} already exists for user {database_image_name}', "Image name": database_image_name}
#                         return JsonResponse(data, status=409)

#                 # Save the image to the database and update saved_image
#                 saved_image = FileUpload.objects.create(image=image_file, name_text=name_text)
#                 break  # Exit loop after saving first image

#             # Return the saved image in the response
#             data = {'name_text': saved_image.name_text, 'image': saved_image.image.url}
#             return JsonResponse(data)
#         else:
#             data = {'message': 'Invalid form data.'}
#             return JsonResponse(data)


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
            name = UploadMatch(image=image)
            name.save()


            database_images = FileUpload.objects.all()


            logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

            def match_image(database_image):
                database_image_name = database_image.name_text
                # decode the database image and convert it to grayscale
                fp_image  = cv2.imdecode(np.fromstring(database_image.image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

                # create AKAZE object
                akaze = cv2.AKAZE_create()

                # detect and compute keypoints and descriptors using AKAZE
                kp_1, desc_1 = akaze.detectAndCompute(sample, None)
                kp_2, desc_2 = akaze.detectAndCompute(fp_image, None)

                # create BFMatcher object and match descriptors
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(desc_1,desc_2)

                # filter good matches based on distance
                good_points = []
                for m in matches:
                    if m.distance < 90:
                        good_points.append(m)

                # calculate similarity score and log the result
                number_keypoints = min(len(kp_1), len(kp_2))
                similarity_score = len(good_points) / number_keypoints
                logging.info(f"Similarity score for {database_image_name}: {similarity_score}")

                # return the result
                if similarity_score > 0.10:
                    logging.info(f"Matched username: {database_image.name_text}")
                    data = {'message': 'Matched!', 'Username' : database_image.name_text}
                else:
                    data = {'message': 'Not Matched!'}

                # log that the function is done
                logging.info(f"Finished matching for {database_image_name}")


                return data
            logging.info(f"END LOG-------------------------------------------------------------")



            num_cores = os.cpu_count()
            print(f"Number of available threads: {num_cores}")

            with ThreadPoolExecutor(max_workers=num_cores) as executor:
                results = list(executor.map(match_image, database_images))

            for result in results:
                if result['message'] == 'Matched!':
                    return JsonResponse(result)
            
            return JsonResponse({'message': 'Not Matched!'})

        else:
            data = {'message': 'Invalid form data.'}
            return JsonResponse(data)

# #API fro deleting User by Username
# @api_view(['GET'])
# def delete_fp(request, name):

#     try:
#         fingerprint =  FileUpload.objects.get(name_text=name)
#     except FileUpload.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         fingerprint.delete()
#         data = {'message': 'Delete Sucessfuly'}
#         return JsonResponse(data)
# API for deleting all images of a user by username
@api_view(['GET'])
def delete_fp(request, name):
    try:
        fingerprints = FileUpload.objects.filter(name_text=name)
    except FileUpload.DoesNotExist:
        data = {'message': 'User Not found'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        num_deleted, _ = fingerprints.delete()
        if num_deleted > 0:
            data = {'message': f"All {num_deleted} images for user {name} deleted successfully"}
            return JsonResponse(data)
        else:
            data = {'message': f"No images found for user {name}"}
            return JsonResponse(data)

