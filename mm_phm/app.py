import json
import numpy as np
from flask import Flask,jsonify,request,render_template,send_file

app = Flask(__name__)

@app.route('/apiv3/opendata/analyze/pumpcheck' ,methods=['GET', 'POST'])
def pumpcheck():
    if request.method == 'GET':
        return send_file('help_docs/help_pumpcheck.html')
 
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
