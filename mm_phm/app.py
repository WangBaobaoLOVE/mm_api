import json
import numpy as np
from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/apiv3/opendata/analyze/pumpcheck')
def pumpcheck():
    """
这是对水泵的状态信息进行异常点判断，用的是三次多项式拟合的方法

输入:	path1:训练集的json文件的路径
path2:输入的需要判断的json文件的路径
其中：输入的数据是同一台水泵不同时刻的马达电流和温度两个参数，其中json文件必须满足[a,b,c,d,.....]，
数据的个数必须是偶数个，马达电流在前，温度在后

举例： json [1,2,3,4,5,5,4,3,2,1]，
前面的12345代表了5个时刻的马达电流，后面的54321代表了5个时刻的温度
代表第一个时刻的马达电流和温度分别为第一位1和第六位的5
第二个时刻的马达电流和温度分别为第二位的2和第7位的4，依次类推

输出是保存在同一根目录下的result.json，代表了不同时刻水泵的状态情况，1代表可能存在潜在的故障，0代表正常
如   输出的result为 [0,0,1,0,0]  代表第三个时刻可能存在异常，其他时刻正常

    :param path1:训练集的json文件的路径
    :param path2:输入的需要判断的json文件的路径
    :return: 如果成功运行，会返回True值
    """
    path1 = "pumpdata.json"
    path2 = "pumpdata.json"
    with open(path1, mode='r', encoding='UTF-8') as f:
        Data1 = json.load(f)  # 将数据读入Data
    with open(path2, mode='r', encoding='UTF-8') as f:
        Data2 = json.load(f)

    DataNum1 = len(Data1) / 2  # DataNum是样本个数的一半
    DataNum1 = int(DataNum1)  # 转为整数
    DataNum2 = len(Data2) / 2  # DataNum是样本个数的一半
    DataNum2 = int(DataNum2)

    DataArray = np.mat(np.zeros((2, DataNum1)))  # 生成一个0矩阵
    for i in range(DataNum1):
        DataArray[0, i] = Data1[i]
        DataArray[1, i] = Data1[i + DataNum1]  # 将数据导入

    DataArrayT = np.mat(np.zeros((2, DataNum2)))  # 生成一个0矩阵
    for i in range(DataNum2):
        DataArrayT[0, i] = Data2[i]
        DataArrayT[1, i] = Data2[i + DataNum2]  # 将数据导入

    DataArray = DataArray.T[np.lexsort(DataArray[::-1, :])]
    DataArray = np.reshape(DataArray, (DataNum1, 2))
    DataArray = DataArray.T

    for i in range(DataNum1):
        DataArray[1, i] = DataArray[1, i] / DataArray[0, i]
        DataArray[1, i] = DataArray[1, i] * 1000 / 380 / (3 ** 0.5)

    for i in range(DataNum2):
        DataArrayT[1, i] = DataArrayT[1, i] / DataArrayT[0, i]
        DataArrayT[1, i] = DataArrayT[1, i] * 1000 / 380 / (3 ** 0.5)

    x = []
    y = []
    xT = []
    yT = []
    for i in range(DataNum1):
        x.append(DataArray[0, i])
    for i in range(DataNum1):
        y.append(DataArray[1, i])
    for i in range(DataNum2):
        xT.append(DataArrayT[0, i])
    for i in range(DataNum2):
        yT.append(DataArrayT[1, i])

    p = np.poly1d(np.polyfit(x, y, 3))

    yP = p(x)  # 训练集的预测结果
    yPT = p(xT)
    sum = 0

    for i in range(DataNum1):
        sum = sum + (yP[i] - y[i]) ** 2
    mse = (sum / (DataNum1 - 1)) ** 2

    result = []
    for i in range(DataNum2):
        if (abs(yPT[i] - yT[i])) > (3 * mse):
            result.append(1)
        else:
            result.append(0)

    filename = "result.json"
    f = open(filename, 'w')
    json.dump(result, f)
    # f.close()
    return jsonify(result)

if __name__ == "__main__":
	app.run(port=8000)
