##########################################################
# Dockerfile to run a flask-based web application
# Based on an centos:8.1.1911 image
# Please name the image to env_image_base image
##########################################################

# Set the base image to use to centos
FROM centos:8.1.1911

# Set the file maintainer
MAINTAINER Wang Bobo,wbb392797665@sina.com

# install python3
RUN yum -y install wget \
    && yum -y install gcc automake autoconf libtool make \
    && yum -y install gcc gcc-c++ \ 
    && wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz \
    && tar -xvf Python-3.6.3.tgz \
    && rm -f Python-3.6.3.tgz \
    && yum -y install zlib zlib-devel \
    && yum -y install epel-release \
    && yum -y install openssl \
    && yum -y install openssl-devel \
    && cd Python-3.6.3 && ./configure \
    && make \
    && make install

# install python3-pip tool 
RUN yum -y install python3-pip


























































































