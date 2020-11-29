from django.http import HttpResponse
import json
import os
import globalVal
import model

check_envDict = {}
check_envList = ['django', 'torch', 'opencv', 'tensorflow', 'numpy']

# 检查环境
def check_environment(request):
    global check_envDict
    if len(check_envDict) != len(check_envList):
        import django
        check_envDict['django'] = [django.__version__, '主环境库']
        
        import torch
        check_envDict['torch'] = [torch.__version__, '主环境库']

        import cv2
        check_envDict['opencv'] = [cv2.__version__, '闲置库']

        import tensorflow as tf
        check_envDict['tensorflow'] = [tf.__version__, '运行库']

        import numpy as np
        check_envDict['numpy'] = [np.__version__, '运行库']
    return HttpResponse(json.dumps(check_envDict))

# 检查数据集
def check_dataset(request):
    check_dataDict = {}

    if os.path.exists('./data/movie/'):
        check_dataDict['测试视频'] = len(os.listdir('./data/movie/'))

    if os.path.exists('./data/sentence_data/'):
        check_dataDict['预存文本向量集'] = len(os.listdir('./data/sentence_data/'))

    if os.path.exists('./data/video_data/'):
        check_dataDict['预存视频向量集_TALL'] = len(os.listdir('./data/video_data/TALL/'))
        check_dataDict['预存视频向量集_MAC'] = 0
        check_dataDict['预存视频向量集_A2C'] = len(os.listdir('./data/video_data/A2C'))
    print(check_dataDict)
    return HttpResponse(json.dumps(check_dataDict))

# 检查模型
def check_model(request):
    check_modelDict = {}
    try:
        print(globalVal.jShu)
        check_modelDict["skip-thoughts"] = "已预加载"
    except:
        globalVal.init()
        check_modelDict["skip-thoughts"] = "已预加载"
    
    if "TALL" in model.mesQueue.load_model_list:
        check_modelDict["TALL"] = "已装载内存"
    else:
        check_modelDict["TALL"] = "未装载内存"

    if "MAC" in model.mesQueue.load_model_list:
        check_modelDict["MAC"] = "已装载内存"
    else:
        check_modelDict["MAC"] = "未装载内存"
    
    if "A2C" in model.mesQueue.load_model_list:
        check_modelDict["A2C"] = "已装载内存"
    else:
        check_modelDict["A2C"] = "未装载内存"
    
    print(check_modelDict)
    return HttpResponse(json.dumps(check_modelDict))