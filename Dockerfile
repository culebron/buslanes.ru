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
	lxml \
	polyline \
	rtree \
	shapely

RUN mkdir /calculator
COPY calculator /calculator
RUN echo "cd calculator && make results/rating.csv" > /make-rating.sh
