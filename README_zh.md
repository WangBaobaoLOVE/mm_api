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

- docker，版本18.09.7+

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

分三步建立应用镜像的原因是因为CentOS基本镜像的拉取和python3的安装比较耗时，并且第三方依赖以后可能也会增加。最重要的是便于快速开发。

## 启动

#### 模式 1: 伪终端交互模式
```
sudo docker run -it -p 8000:8000 --name test1 mm_phm:1.0
```

#### 模式 2: 后台模式(推荐模式)
```
sudo docker run -d -p 8000:8000 --name test1 mm_phm:1.0
```

直接在命令行中输入以上命令（模式1或模式2），然后按`Enter`键启动应用程序服务

## API规范

默认情况下，服务将在8000端口上运行HTTP服务, 并使用RESTful API：

```
http://127.0.0.1:8000/apiv3/opendata/analyze/*****，Methods= ['GET'，'POST']
```

对于请求，如果方法为`GET`，则服务将返回API文档（`HTML`格式）。

对于请求，如果方法是`POST`，则服务将在分析数据后返回结果（`json`格式）。当然，您首先需要在请求`body`中插入`json`格式的机械设备数据

**目前PHM服务所提供的API主要分为三个部分：**

1. 水泵的异常点判断（三次多项式线性拟合）
2. 设备的故障点判断（随机森林分类）
3. 设备的剩余使用寿命（RUL）预测（LSTM回归）

**您可以通过如下方法来或获知所提供的API及其调用方法:**

```
http://127.0.0.1:8000/apiv3/opendata/analyze/
```

```
http://127.0.0.1:8000/apiv3/opendata/analyze/index
```

**以设备的剩余使用寿命（RUL）预测（LSTM回归)的API规范为例说明:**

- **`GET`方法获得API说明文档**

```
http://127.0.0.1:8000/apiv3/opendata/analyze/machineRULtrain/
```

- **`POST` 方法获得建模结果**

```
http://127.0.0.1:8000/apiv3/opendata/analyze/machineRULtrain/
```
在`request`的`body`提交的`json`格式文件举例如下:

```
{
	"temperature":[31,36,37,27],
	"power":[891,784,0,1025],
	"label":[0,0,1,0]
}
```
上面的数据中，代表第一个时刻设备的温度为31，功率为891，0代表当前时刻机器的剩余寿命为0个机器周期，第二个时刻设备的温度为36，功率为784，当前时刻机器的剩余寿命为0个机器周期，以此类推。

**Note :***该API是建立设备故障模型,并不是利用模型分析数据,所以其不返回建模结果,而是返回`布尔类型`表明是否建模成功*.`True`表示建模成功,其保存模型的`h5`文件会保存在容器中;`False`表示建模失败

```
True or False
```

##其他信息

该服务暂时还处于测试阶段,暂不能用于实际生产运营当中，并且仅是为茂盟的phm服务构建。


 **Copyright by Wang Bobo, wbb392797665@sina.com.请不要用于商业用途.**