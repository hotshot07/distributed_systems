FROM ubuntu:18.04
COPY main.py ./
RUN apt-get update && apt-get install -y python3 python3-pip vim
RUN pip3 install --upgrade pip
RUN pip3 install Flask requests
