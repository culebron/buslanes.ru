FROM python:3.8
MAINTAINER Dmitri Lebedev <dl@peshemove.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	build-essential \
	libspatialindex-dev \
	libgdal-dev \
	libgeos-dev \
	locales \
	python3-pip \
	python3-dev \
	python3-setuptools \
	proj-bin

RUN pip3 install wheel
COPY requirements.txt /tmp/requirements.txt
RUN ldconfig && pip3 install -U -r /tmp/requirements.txt
RUN ldconfig && pip3 install -U ipdb

RUN mkdir /calc

RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

RUN echo "cd calc && python3 main.py" > /make-rating.sh
RUN echo "cd calc && python3.8 render.py html/index.template.html build/bus-lanes.geojson build/bus-lanes.csv build/index.html" > /render.sh

