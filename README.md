# PHM SERVER

[中文版](./README_zh.md)

## Overview

This server was written for phm server of maomeng. 

The basic functionality of this server is that maomeng using API supported by the phm server can get the result of analyzing their data.

## Requirement

For local deployment, the requirements are listed as follows:

- OS: Ubuntu 16.04+ (大部分主流linux系统,能够安装运行docker即可)
- python, version 3.6.1+
- dependencies: please view [requirements.txt](mm_phm/requirements.txt)

However, we recommend you to use docker to deploy the server, with requirements:

- docker, version 18.09.7+

Note:The above deployment environment has been tested, but we can not guarantee whether other environments can run normally. 

## Directory tree

![](./images/mm_api_tree.png)

The above files are used directly in the README for explanation, so the directory tree is given here for user comparison.

## Build env using docker
We recommend you to build docker image and then run the server.

#### Step1. CentOS8.1+python3.6
```
cd image_base/env_image_base
sudo docker build --tag env_image_base:1.0 .
```

#### Step2. Install dependencies
```
cd image_base/lib_image_base
sudo docker build --tag lib_image_base:1.0 .
```

#### Step3. App image
```
cd mm_phm
sudo docker build --tag mm_phm:1.0 .
```

The reason why the application image is established in three steps is because the pulling of the CentOS base image and the installation of python3 are more time-consuming, and the third-party dependency may increase later. The most important thing is to facilitate rapid development.

## Usage

#### Mode 1: Pseudo-terminal interactive mode
```
sudo docker run -it -p 8000:8000 --name test1 mm_phm:1.0
```

#### Mode 2: Background mode (recommended mode)
```
sudo docker run -d -p 8000:8000 --name test1 mm_phm:1.0
```

Enter the above command (Method 1 or Method 2)directly in the command line and press Enter to start the application service.

## API Specifications

The server will run a HTTP service on 8000 port by default, with RESTful API:

```
http://127.0.0.1:8000/apiv3/opendata/analyze/pumpcheck , method = ['GET', 'POST']
```

For request, if the method is `GET`, the server will return the API document (`html` format).

For request, if the method is `POST`, the server will return the results after analyzing data (`json` format). You firstly need to insert machincal data in request body, with json format:


## Other Information

This project is not a production level server, only being built for phm server of maomeng.

 **Copyright by Wang Bobo, wbb392797665@sina.com. Please do not use it in commercial aspects.**