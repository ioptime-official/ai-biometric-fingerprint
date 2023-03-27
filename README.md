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

