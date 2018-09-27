FROM python:3.6

RUN apt-get update && apt-get upgrade
RUN apt-get install \
        python-pip \
        git

RUN pip install -r requirements.txt