FROM ubuntu:17.04
MAINTAINER Dmitri Lebedev <dl@peshemove.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
	&& apt-get install -y --force-yes --no-install-recommends \
	libspatialindex-dev \
	libgdal-dev \
	libgeos-dev \
	python3-pip \
	python3-dev \
	python3-setuptools \
	unzip \
	wget


RUN ldconfig && pip3 install -U \
	argh \
	decorator \
	fastkml \
	geojson \
	geopandas \
	Jinja2 \
	lxml \
	polyline \
	rtree \
	shapely

RUN mkdir /calculator /aqtash
COPY calculator /calculator
COPY aqtash /aqtash

RUN apt-get install -y locales
RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

RUN echo "cd calculator && python3 main.py" > /make-rating.sh
