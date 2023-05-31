# Fingerprint Matcher using OpenCV in Django

This is a web-based application that allows users to upload images of fingerprints and match them against a pre-existing database of fingerprints. The matching algorithm is implemented using OpenCV, and the web interface is built using Django.

## Installation

Clone the repository:

```sh
https://github.com/ioptime-official/ai-biometric-fingerprint
```
Navigate to the project directory:

```sh
cd ai-biometric-fingerprint
```
Install the required packages:
```sh
pip install -r requirements.txt
```
python manage.py migrate
```sh
python manage.py migrate appone
```
Finally make the migrations
```sh
python manage.py makemigrations
```
Start the development server:
```sh
python manage.py runserver
```
Navigate to http://localhost:8000 in your web browser to use the application.
## Usage
To use the application, follow these steps:

1. Navigate to the homepage of the application.
2. First Register by adding username and fingerprint
3. Click on login and upload your fingerprint to match 
4. The application will display the results of the matching process, including any matches found in the database.

## Examples
### Homepage![Screenshot from 2023-03-27 12-47-29](https://user-images.githubusercontent.com/50315486/227875382-81eeb2b7-1aa6-4af7-8dbc-fc5485a33195.png)

### Login ![Screenshot from 2023-03-27 12-47-47](https://user-images.githubusercontent.com/50315486/227875458-9125714f-51e3-4f15-8c3a-76082fe138bc.png)


