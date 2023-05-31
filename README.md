# Django Fingerprint Matching Docker EC2 Instance Deployment



## Project Overview
The  Fingerprint  Authentication  System  for  user  identification  and  verification.  This  project  leverages 
OpenCV,  AKAZE  algorithm,  Django,  and  Docker  to  create  a  reliable  fingerprint  scanner  that  captures 
fingerprints, saves them to a database, and performs real-time matching for user login. The system is 
accessible through an Android app, which communicates with the server using APIs.
##  Technologies and Algorithms
Here are some examples of technologies and algorithms that can be mentioned:
##### 1. Fingerprint Scanner and Image Processing: 
The image processing and fingerprint scanning module is implemented using Python, leveraging 
libraries such as OpenCV and AKAZE.
##### 2. Backend Development and API Integration:
The server-side development, including handling user authentication, managing the database, 
and  exposing  APIs,  is  accomplished  using  Python  with  the  Django  web  framework.  Django 
provides a robust and efficient environment for web development and API integration. Django 
Rest framework is used to build APIs.
##### 3. Database Management:
The database management is implemented using SQL (Structured Query Language), which is a 
standard language for managing relational databases. Specifically, PostgreSQL is used with Django 
app.
##### 4. Deployment and Containerization:
The project utilizes Docker along with Django, Nginx, and Gunicorn for implementation. Docker 
allows for containerization, while Django serves as the web framework, Nginx handles the web 
server functionality, and Gunicorn acts as the application server. This combination provides a 
scalable and efficient environment for deploying the fingerprint authentication system.
## Frameworks & Libraries
- OpenCV
- AKAZE Algorithm
- Django 
- Django REST Framework (DRF)
- Nginx
- Gunicorn
- PostgreSQL
- Amazon  AWS  EC2  Instance

## Installation

This Project needs the following requirements to run

```sh
gunicorn==20.0.4
psycopg2-binary==2.8.5
asgiref==3.6.0
Django==3.2.18
djangorestframework==3.14.0
numpy==1.21.6
opencv-contrib-python==4.7.0.72
Pillow==9.4.0
pytz==2022.7.1
sqlparse==0.4.3
typing_extensions==4.5.0
```

All these Requirements will be installed automaticaly using the docker image you just need Docker to be preinstalled

In order to run the docker container run the following commands


For production environments...
```sh
sudo docker-compose -f docker-compose.yml up --build
sudo docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
```
It can be tested in the configured public IP which is https://3.144.253.41

If the public address need to be changed the, first new ssl certificate should be created in config/nginx/certs/ and common name should be the public IP or Domain name 
Following Command can be used to create ssl certificates
```sh
openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out localhost.crt -keyout localhost.key
```
- The address and domain name should also be changed in the "ALLOWED_HOSTS" "CSRF_TRUSTED_ORIGINS"
- The index.html, match.html and matching.html url should also be changed accordingly
- Also change the server name in the nginx configuration

## References
https://medium.com/@cloudcleric/deploying-a-django-application-in-docker-with-nginx-beeed45bebb8
https://github.com/soumilshah1995/Deploy-Docker-Container-on-AWS
https://github.com/elabdesunil/django-postgresql-gunicorn-nginx-dockerized
https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
