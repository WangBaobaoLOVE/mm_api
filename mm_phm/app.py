import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.layers import Dense, Dropout, LSTM
from tensorflow.python.keras.models import Sequential, load_model
import os
import h5py     #这个包以及上面提到的包都需要安装！！！

from flask import Flask,jsonify,request,render_template,send_file

app = Flask(__name__)


@app.route('/apiv3/opendata/analyze/',methods=['GET'])
def index1():
    return send_file('help_docs/index.html')

@app.route('/apiv3/opendata/analyze/index/' ,methods=['GET'])
def index2():
    return send_file('help_docs/index.html')

@app.route('/apiv3/opendata/analyze/pumpcheck/' ,methods=['GET', 'POST'])
def pumpcheck():
    if request.method == 'GET':
        return send_file('help_docs/help_pumpcheck.html')
 
    #path1 = "pumpdata.json"
    #path2 = "pumpdata.json"
    #with open(path1, mode='r', encoding='UTF-8') as f:
        #Data1 = json.load(f)  # 将数据读入Data
    #with open(path2, mode='r', encoding='UTF-8') as f:
        #Data2 = json.load(f)
    Data1 = request.get_json()
    Data2 = Data1
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


def machinechecktrain(path1="machinedata.json", savepath='''rfmodel.m'''):

    with open(path1, mode='r', encoding='UTF-8') as f:
        Data1 = json.load(f)  # 将数据读入Data

    dim = len(Data1)  # 获取数据的维度
    key_list = Data1.keys()
    temp = []
    for i in range(dim - 1):
        temp.append(Data1.get(list(key_list)[i]))
    label = Data1.get(list(key_list)[dim - 1])
    SampleNum = len(temp[0])
    DataArray = np.mat(np.zeros((SampleNum, dim - 1)))  # 生成一个0矩阵
    for i in range(dim - 1):
        for j in range(SampleNum):
            DataArray[j, i] = temp[i][j]

    for i in range(dim - 1):
        sum = 0
        mse = 0
        t = 0
        for j in range(SampleNum):
            if DataArray[j, i] != 0:
                sum = sum + DataArray[j, i]
                t = t + 1
        aver = sum / t
        for j in range(SampleNum):
            if DataArray[j, i] == 0:
                DataArray[j, i] = aver
        for j in range(SampleNum):
            mse = mse + (DataArray[j, i] - aver) ** 2
        mse = (mse / (t - 1)) ** 0.5
        for j in range(SampleNum):
            DataArray[j, i] = (DataArray[j, i] - aver) / mse

    model = RandomForestClassifier(n_estimators=50,
                                   bootstrap=True,
                                   max_depth=None,
                                   min_samples_leaf=1
                                   )
    model.fit(DataArray, label)
    joblib.dump(model, savepath)


def machinechecktest(path2="machinetest.json", modelpath='rfmodel.m', savepath="resultm.json"):

    with open(path2, mode='r', encoding='UTF-8') as f:
        Data2 = json.load(f)

    dim = len(Data2)+1  # 获取数据的维度
    key_list = Data2.keys()
    temp = []
    for i in range(dim - 1):
        temp.append(Data2.get(list(key_list)[i]))
    SampleNum = len(temp[0])


    tempT = []
    for i in range(dim - 1):
        tempT.append(Data2.get(list(key_list)[i]))
    SampleNumT = len(tempT[0])
    DataArrayT = np.mat(np.zeros((SampleNumT, dim - 1)))  # 生成一个0矩阵
    for i in range(dim - 1):
        for j in range(SampleNumT):
            DataArrayT[j, i] = tempT[i][j]

    for i in range(dim - 1):
        sum = 0
        mse = 0
        t = 0
        for j in range(SampleNumT):
            if DataArrayT[j, i] != 0:
                sum = sum + DataArrayT[j, i]
                t = t + 1
        aver = sum / t
        for j in range(SampleNumT):
            if DataArrayT[j, i] == 0:
                DataArrayT[j, i] = aver
        for j in range(SampleNumT):
            mse = mse + (DataArrayT[j, i] - aver) ** 2
        mse = (mse / (t - 1)) ** 0.5
        for j in range(SampleNumT):
            DataArrayT[j, i] = (DataArrayT[j, i] - aver) / mse

    model = joblib.load(modelpath)
    ypred = model.predict(DataArrayT)

    result = []
    for i in range(len(ypred)):
        result.append(float(ypred[i]))

    filename = savepath
    f = open(filename, 'w')
    json.dump(result, f)
    f.close()
    return True



@app.route('/apiv3/opendata/analyze/machineRULtrain/' ,methods=['GET', 'POST'])
def machineRULtrain(savepath='lstmmodel.h5'):
    if request.method == 'GET':
        return send_file('help_docs/machineRULtrain.html')

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    #with open(path1, mode='r', encoding='UTF-8') as f:
        #Data1 = json.load(f)  # 将数据读入Data
    Data1 = request.get_json()
    dim = len(Data1)  # 获取数据的维度
    key_list = Data1.keys()
    temp = []
    for i in range(dim - 1):
        temp.append(Data1.get(list(key_list)[i]))
    label = Data1.get(list(key_list)[dim - 1])
    SampleNum = len(temp[0])
    DataArray = np.mat(np.zeros((SampleNum, dim - 1)))  # 生成一个0矩阵
    for i in range(dim - 1):
        for j in range(SampleNum):
            DataArray[j, i] = temp[i][j]

    for i in range(dim - 1):
        sum = 0
        mse = 0
        t = 0
        for j in range(SampleNum):
            if DataArray[j, i] != 0:
                sum = sum + DataArray[j, i]
                t = t + 1
        aver = sum / t
        for j in range(SampleNum):
            if DataArray[j, i] == 0:
                DataArray[j, i] = aver
        for j in range(SampleNum):
            mse = mse + (DataArray[j, i] - aver) ** 2
        mse = (mse / (t - 1)) ** 0.5
        for j in range(SampleNum):
            DataArray[j, i] = (DataArray[j, i] - aver) / mse

    TrainDataX = np.zeros((SampleNum, dim - 1))
    TrainDataY = np.zeros((SampleNum, 1))
    for i in range(SampleNum):
        TrainDataX[i] = DataArray[i]
    for i in range(SampleNum):
        TrainDataY[i] = label[i]
    TrainDataX = TrainDataX.reshape(SampleNum, 1, dim - 1)

    model = Sequential()
    model.add(LSTM(100, input_shape=(1, dim - 1)))
    model.add(Dense(30))
    model.add(Dropout(0.3))
    model.add(Dense(30))
    model.add(Dropout(0.3))
    model.add(Dense(1))

    model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    es = EarlyStopping(monitor='accuracy', patience=5)

    model.fit(TrainDataX, TrainDataY,  # TrainDataX,TrainDataY一定要是ndarry
              batch_size=512,
              epochs=50,
              callbacks=[es],
              shuffle=False)

    model.save(savepath)
    return "True"


def machineRULtest(path2="machinetest.json", modelpath='lstmmodel.h5', savepath="resultRUL.json"):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    with open(path2, mode='r', encoding='UTF-8') as f:
        Data2 = json.load(f)

    dim = len(Data2)+1  # 获取数据的维度
    key_list = Data2.keys()
    temp = []
    for i in range(dim - 1):
        temp.append(Data2.get(list(key_list)[i]))
    SampleNum = len(temp[0])

    tempT = []
    for i in range(dim - 1):
        tempT.append(Data2.get(list(key_list)[i]))
    SampleNumT = len(tempT[0])
    DataArrayT = np.mat(np.zeros((SampleNumT, dim - 1)))  # 生成一个0矩阵
    for i in range(dim - 1):
        for j in range(SampleNumT):
            DataArrayT[j, i] = tempT[i][j]

    for i in range(dim - 1):
        sum = 0
        mse = 0
        t = 0
        for j in range(SampleNumT):
            if DataArrayT[j, i] != 0:
                sum = sum + DataArrayT[j, i]
                t = t + 1
        aver = sum / t
        for j in range(SampleNumT):
            if DataArrayT[j, i] == 0:
                DataArrayT[j, i] = aver
        for j in range(SampleNumT):
            mse = mse + (DataArrayT[j, i] - aver) ** 2
        mse = (mse / (t - 1)) ** 0.5
        for j in range(SampleNumT):
            DataArrayT[j, i] = (DataArrayT[j, i] - aver) / mse

    TestDataX = np.zeros((SampleNum, dim - 1))

    for i in range(SampleNum):
        TestDataX[i] = DataArrayT[i]
    TestDataX = TestDataX.reshape(SampleNum, 1, dim - 1)

    model = load_model(modelpath)
    ypred = model.predict(TestDataX)

    result = []
    for i in range(len(ypred)):
        result.append(float(ypred[i]))

    filename = savepath
    f = open(filename, 'w')
    json.dump(result, f)
    f.close()
    return True

if __name__ == "__main__":
	app.run(port=8000)
