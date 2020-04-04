##########################################################
# Dockerfile to run a flask-based web application
# Based on an centos:8.1.1911 image
##########################################################

# Set the base image to use to centos
FROM image_base:1.0

# Set the file maintainer
MAINTAINER Wang Bobo,wbb392797665@sina.com

# Copy application source code to SRCDIR
WORKDIR /usr/src/app

# install python3 dependencies
RUN pip3 install  -i https://mirrors.aliyun.com/pypi/simple/ flask gunicorn gevent numpy sklearn tensorflow matplotlib

COPY . .

CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]



























































