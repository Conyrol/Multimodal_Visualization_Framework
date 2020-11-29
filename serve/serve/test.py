from django.http import HttpResponse
from django.http import FileResponse
import model
import json
import time

def readJson(path):
    with open(path, 'r+') as f:
        content = f.read()
    return json.loads(content)

# 获取视频预测切片
def get_video_cut(request):
    model_name = request.GET.get('model', -1)
    video_name = request.GET.get('video_name', -1)
    sentence = request.GET.get('sentence', -1)
    if video_name != -1 and sentence != -1 and model_name == "TALL":
        model.run_model(model_name, sentence, video_name)
        while(model.mesQueue.tallQueue_output.qsize() == 0):
            time.sleep(1)
        betList = model.mesQueue.tallQueue_output.get()

    if video_name != -1 and sentence != -1 and model_name == "MAC":
        model.run_model(model_name, sentence, video_name)
        while(model.mesQueue.tallQueue_output.qsize() == 0):
            time.sleep(1)
        betList = model.mesQueue.tallQueue_output.get()

    if video_name != -1 and sentence != -1 and model_name == "A2C":
        model.run_model(model_name, sentence, video_name)
        while(model.mesQueue.a2cQueue_output.qsize() == 0):
            time.sleep(1)
        betList = model.mesQueue.a2cQueue_output.get()
    
    return HttpResponse(json.dumps({'list': betList}))

def get_video_showData(request):
    data1 = {}
    dataDict = readJson('./data/show_data/video_data.json')
    data1['data'] = dataDict['list']
    data1['data_x'] = dataDict['name']
    data1['name'] = '帧率'

    data2 = {}
    dataDict = readJson('./data/show_data/video_data2.json')
    data2['data'] = dataDict['list']
    data2['data_x'] = dataDict['name']
    data2['name'] = '秒数'

    return HttpResponse(json.dumps({'data1': data1, 'data2': data2}))


def get_text_showData(request):
    data1 = {}
    dataDict = readJson('./data/show_data/text_data.json')
    data1['data'] = dataDict['list']
    data1['data_x'] = dataDict['name']
    data1['name'] = '长度'

    return HttpResponse(json.dumps({'data1': data1}))