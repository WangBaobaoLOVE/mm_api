##########################################################
# Dockerfile to run a flask-based web application
# Based on an lib_image_base:1.0 image
##########################################################

# Set the base image to use to centos
FROM lib_image_base:1.0

# Set the file maintainer
MAINTAINER Wang Bobo,wbb392797665@sina.com

# Copy application source code to SRCDIR
WORKDIR /usr/src/app

COPY . .

CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]



























































