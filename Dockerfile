FROM python:3.7-alpine

#Environment variable that you want to set
#Tells python to run in unbuffered mode which is recommended when running python within Docker containers
#It doesnt allow python to buffer the outputs
ENV PYTHONUNBUFFERED 1

#Copy directory json file to docker file and Docker image to requirements.txt
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

#install requirements in the docker image by using pip
RUN pip install -r /requirements.txt
#delete temporary requirements
RUN apk del .tmp-build-deps

#create empty folder called /app
RUN mkdir /app

#switch it as default directory
WORKDIR /app

# copy the code to docker containers
COPY ./app/ /app

# create user that going to run our application
# -D means only this user use this application
RUN adduser -D user
USER user
