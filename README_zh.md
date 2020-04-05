# 故障预测与健康管理服务

[英文版](./README.md)

## 概览

该服务主要是为茂盟提供phm服务。

该服务的基本功能是通过使用phm服务提供的API接口,茂猛可以直接获得其设备数据分析的结果。

## 要求

对于本地部署，要求列出如下:

- 操作系统: Ubuntu 16.04+ (大部分主流linux系统,能够安装运行docker即可)
- 编程语言: python, 版本3.6.1+
- 第三方依赖: 见[requirements.txt](mm_phm/requirements.txt)


但是，我们建议您使用docker来部署服务器，具体要求如下：

-docker，版本18.09.7+

注意：以上部署环境已经过测试，但是我们不能保证其他环境是否可以正常运行。

## 目录树

![](./images/mm_api_tree.png)

以上文件直接在README文件中用于进行说明，因此此处给出了目录树以供您对照。

## 使用docker建立运行环境

我们建议您构建docker镜像，然后运行该服务。

#### Step1. 搭建CentOS8.1+python3.6的镜像
```
cd image_base/env_image_base
sudo docker build --tag env_image_base:1.0 .
```

#### Step2. 安装第三方依赖
```
cd image_base/lib_image_base
sudo docker build --tag lib_image_base:1.0 .
```

#### Step3. 生成应用镜像
```
cd mm_phm
sudo docker build --tag mm_phm:1.0 .
```

分三步建立应用镜像的原因是因为CentOS基本镜像的拉取和python3的安装比较耗时，并且第三方依赖以后可能也会增加。最重要的是便于快速发展。

## 启动

#### 模式 1: 伪终端交互模式
```
sudo docker run -it -p 8000:8000 --name test1 mm_phm:1.0
```

#### 模式 2: 后台 (推荐模式)
```
sudo docker run -d -p 8000:8000 --name test1 mm_phm:1.0
```

直接在命令行中输入以上命令（模式1或模式2），然后按`Enter`键启动应用程序服务

## API规范

默认情况下，服务将在8000端口上运行HTTP服务, 并使用RESTful API：

```
http://127.0.0.1:8000/apiv3/opendata/analyze/pumpcheck，Method= ['GET'，'POST']
```

对于请求，如果方法为`GET`，则服务将返回API文档（`HTML`格式）。

对于请求，如果方法是`POST`，则服务将在分析数据后返回结果（`json`格式）。当然，您首先需要在请求`body`中插入`json`格式的机械设备数据

##其他信息

该服务暂时还处于测试阶段,暂不能用于实际生产运营当中，并且仅是为茂盟的phm服务构建。


 **Copyright by Wang Bobo, wbb392797665@sina.com.请不要用于商业用途.**