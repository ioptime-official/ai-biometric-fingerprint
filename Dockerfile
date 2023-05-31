FROM python:3.9-slim-buster
ENV PYTHONBUFFERED 1
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get update && apt-get install -y libglib2.0-dev
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update && apt-get install -y libpq-dev
RUN apt-get install -y netcat
RUN apt-get update && apt-get install -y libglib2.0-dev
RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev
RUN apt-get update && apt-get install -y nano

WORKDIR /home/app

RUN apt-get update && apt-get install -y libglib2.0-dev


# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

RUN mkdir -p /home/app/web/
ADD ./appone /home/app/web/

RUN pip install --upgrade pip
COPY ./requirements.txt $APP_HOME
RUN pip install -r requirements.txt
# Install gunicorn
RUN pip install gunicorn

# Start the application
CMD [ "python", "manage.py","migrate"]
CMD [ "python", "manage.py","migrate" ,"appone"]
CMD [ "python", "manage.py","makemigrations"]
#CMD [ "gunicorn", "--certfile=/etc/certs/localhost.crt","--keyfile=/etc/certs/localhost.key" , "assignment1.wsgi:application", "--bind", "0.0.0.0:443" ]


# copy entrypoint-prod.sh
COPY ./entrypoint.prod.sh $APP_HOME

# copy project
COPY . $APP_HOME

# Create the 'app' user and group
RUN groupadd -r app && useradd -r -g app app

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]
