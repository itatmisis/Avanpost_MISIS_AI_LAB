FROM ubuntu:18.04
COPY . /app

RUN apt-get -y update
RUN apt update
RUN apt-get upgrade -y python
RUN apt-get install -y python3-pip
RUN apt install  -y unzip
RUN apt install -y wget
RUN  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN wget https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip 

RUN unzip chromedriver_linux64.zip


RUN pip3 install -r app/requirements.txt


EXPOSE 8000

WORKDIR /app
CMD ["python", "app/server.py"]