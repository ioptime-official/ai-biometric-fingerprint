FROM python:3.9-slim-buster
ENV PYTHONBUFFERED 1
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get update && apt-get install -y libglib2.0-dev
RUN mkdir /code
ADD ./appone /code
WORKDIR /code

RUN pip install --trusted-host pypy.org --trusted-host files.pythonhosted.org -r requirements.txt
# Install gunicorn
RUN pip install gunicorn

# Start the application
CMD [ "python", "manage.py","migrate"]
CMD [ "python", "manage.py","migrate" ,"appone"]
CMD [ "python", "manage.py","makemigrations"]
CMD [ "gunicorn", "--certfile=/etc/certs/localhost.crt","--keyfile=/etc/certs/localhost.key" , "assignment1.wsgi:application", "--bind", "0.0.0.0:443" ]

