from django.http import HttpResponse
from django.http import FileResponse
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
import json
import re
import os

def readJson(path):
    with open(path, 'r+') as f:
        content = f.read()
    return json.loads(content)

# 文件切分
def file_iterator(file_name, chunk_size = 8192, offset = 0, length = None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data

# 视频传输 (流媒体 or 非流媒体)
def get_movie_data(request):
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)

    video_name = request.GET.get('name', -1)
    path = './data/movie/{}'.format(video_name)
    print(path)
    if not os.path.exists(path):
        return HttpResponse(-1)
    size = os.path.getsize(path)

    content_type = 'application/octet-stream'
    if range_match:             # 流媒体传输
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = first_byte + 1024 * 1024 * 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(file_iterator(path, offset = first_byte, length = length), status=206, content_type = content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:                       # 非流媒体传输
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type = content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp

# 测试接口
def test(request):
    this = 'all fine!'
    return HttpResponse(this)

# 获取 movie 列表
def get_movie_list(request):
    movie_list = os.listdir('./data/movie/')
    return HttpResponse(json.dumps({'list': movie_list}))

# 获取可视化数据
def get_analysis_data(request):
    model_name = request.GET.get('name', -1)
    allData = {}
    data = {}
    data_5 = {}
    data_7 = {}
    if model_name == "TALL_C3D":
        dataList = readJson('./data/analysis_data/TALL.json')["list"]
        data_x = []
        data_y = []
        name = ["Loss", "loss_align", "loss_reg"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"Loss": i['Loss'], "loss_align": i['loss_align'], "loss_reg": i['loss_reg']})
        data['data_x'] = data_x
        data['name_x'] = 'Epoch'
        data['name_y'] = 'Loss'
        data['data_y'] = data_y
        data['name'] = name
        data['color'] = ['#8AE09F', '#FA6F53', '#636363']

        dataList = readJson('./data/analysis_data/TALL_IOU0.5.json')["list"]
        data_x = []
        data_y = []
        name = ["R@1", "R@5"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"R@1": i['R@1'], "R@5": i['R@5']})
        data_5['data_x'] = data_x
        data_5['name_x'] = 'Epoch'
        data_5['name_y'] = 'IOU0.5_accuracy'
        data_5['data_y'] = data_y
        data_5['name'] = name
        data_5['color'] = ['#8AE09F', '#FA6F53']

        dataList = readJson('./data/analysis_data/TALL_IOU0.7.json')["list"]
        data_x = []
        data_y = []
        name = ["R@1", "R@5"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"R@1": i['R@1'], "R@5": i['R@5']})
        data_7['data_x'] = data_x
        data_7['name_x'] = 'Epoch'
        data_7['name_y'] = 'IOU0.7_accuracy'
        data_7['data_y'] = data_y
        data_7['name'] = name
        data_7['color'] = ['#8AE09F', '#FA6F53']

    if model_name == "MAC_C3D":
        dataList = readJson('./data/analysis_data/MAC.json')["list"]
        data_x = []
        data_y = []
        name = ["Loss", "loss_align", "loss_reg"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"Loss": i['Loss'], "loss_align": i['loss_align'], "loss_reg": i['loss_reg']})
        data['data_x'] = data_x
        data['name_x'] = 'Epoch'
        data['name_y'] = 'Loss'
        data['data_y'] = data_y
        data['name'] = name
        data['color'] = ['#8AE09F', '#FA6F53', '#636363']

        dataList = readJson('./data/analysis_data/MAC_IOU0.5.json')["list"]
        data_x = []
        data_y = []
        name = ["R@1", "R@5"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"R@1": i['R@1'], "R@5": i['R@5']})
        data_5['data_x'] = data_x
        data_5['name_x'] = 'Epoch'
        data_5['name_y'] = 'IOU0.5_accuracy'
        data_5['data_y'] = data_y
        data_5['name'] = name
        data_5['color'] = ['#8AE09F', '#FA6F53']

        dataList = readJson('./data/analysis_data/MAC_IOU0.7.json')["list"]
        data_x = []
        data_y = []
        name = ["R@1", "R@5"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"R@1": i['R@1'], "R@5": i['R@5']})
        data_7['data_x'] = data_x
        data_7['name_x'] = 'Epoch'
        data_7['name_y'] = 'IOU0.7_accuracy'
        data_7['data_y'] = data_y
        data_7['name'] = name
        data_7['color'] = ['#8AE09F', '#FA6F53']
    
    if model_name == "A2C":
        dataList = readJson('./data/analysis_data/A2C.json')["list"]
        data_x = []
        data_y = []
        name = ["Loss", "value_loss", "iou_loss", "location_loss"]
        for i in dataList:
            data_x.append(i['Epoch:'])
            data_y.append({"Loss": i['loss:'], "value_loss": i['value_loss:'], "iou_loss": i['iou_loss:'], "location_loss": i['location_loss:']})
        data['data_x'] = data_x
        data['name_x'] = 'Epoch'
        data['name_y'] = 'Loss'
        data['data_y'] = data_y
        data['name'] = name
        data['color'] = ['#8AE09F', '#FA6F53', '#636363', 'blue']

        dataList = readJson('./data/analysis_data/A2C_IOU0.5.json')["list"]
        data_x = []
        data_y = []
        name = ["R@1"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"R@1": i['R@1']})
        data_5['data_x'] = data_x
        data_5['name_x'] = 'Epoch'
        data_5['name_y'] = 'IOU0.5_accuracy'
        data_5['data_y'] = data_y
        data_5['name'] = name
        data_5['color'] = ['#8AE09F', '#FA6F53']

        dataList = readJson('./data/analysis_data/A2C_IOU0.7.json')["list"]
        data_x = []
        data_y = []
        name = ["R@1"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"R@1": i['R@1']})
        data_7['data_x'] = data_x
        data_7['name_x'] = 'Epoch'
        data_7['name_y'] = 'IOU0.7_accuracy'
        data_7['data_y'] = data_y
        data_7['name'] = name
        data_7['color'] = ['#8AE09F', '#FA6F53']

    if model_name == "TALL_I3D":
        dataList = readJson('./data/analysis_data/I3DTALL.json')["list"]
        data_x = []
        data_y = []
        name = ["Loss", "loss_align", "loss_reg"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"Loss": i['Loss'], "loss_align": i['loss_align'], "loss_reg": i['loss_reg']})
        data['data_x'] = data_x
        data['name_x'] = 'Epoch'
        data['name_y'] = 'Loss'
        data['data_y'] = data_y
        data['name'] = name
        data['color'] = ['#8AE09F', '#FA6F53', '#636363']

        dataList = readJson('./data/analysis_data/I3DTALL_IOU0.5.json')["list"]
        data_x = []
        data_y = []
        name = ["R@1", "R@5"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"R@1": i['R@1'], "R@5": i['R@5']})
        data_5['data_x'] = data_x
        data_5['name_x'] = 'Epoch'
        data_5['name_y'] = 'IOU0.5_accuracy'
        data_5['data_y'] = data_y
        data_5['name'] = name
        data_5['color'] = ['#8AE09F', '#FA6F53']

        dataList = readJson('./data/analysis_data/I3DTALL_IOU0.7.json')["list"]
        data_x = []
        data_y = []
        name = ["R@1", "R@5"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"R@1": i['R@1'], "R@5": i['R@5']})
        data_7['data_x'] = data_x
        data_7['name_x'] = 'Epoch'
        data_7['name_y'] = 'IOU0.7_accuracy'
        data_7['data_y'] = data_y
        data_7['name'] = name
        data_7['color'] = ['#8AE09F', '#FA6F53']

    if model_name == "MAC_I3D":
        dataList = readJson('./data/analysis_data/I3DMAC.json')["list"]
        data_x = []
        data_y = []
        name = ["Loss", "loss_align", "loss_reg"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"Loss": i['Loss'], "loss_align": i['loss_align'], "loss_reg": i['loss_reg']})
        data['data_x'] = data_x
        data['name_x'] = 'Epoch'
        data['name_y'] = 'Loss'
        data['data_y'] = data_y
        data['name'] = name
        data['color'] = ['#8AE09F', '#FA6F53', '#636363']

        dataList = readJson('./data/analysis_data/I3DMAC_IOU0.5.json')["list"]
        data_x = []
        data_y = []
        name = ["R@1", "R@5"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"R@1": i['R@1'], "R@5": i['R@5']})
        data_5['data_x'] = data_x
        data_5['name_x'] = 'Epoch'
        data_5['name_y'] = 'IOU0.5_accuracy'
        data_5['data_y'] = data_y
        data_5['name'] = name
        data_5['color'] = ['#8AE09F', '#FA6F53']

        dataList = readJson('./data/analysis_data/I3DMAC_IOU0.7.json')["list"]
        data_x = []
        data_y = []
        name = ["R@1", "R@5"]
        for i in dataList:
            data_x.append(i['Epoch'])
            data_y.append({"R@1": i['R@1'], "R@5": i['R@5']})
        data_7['data_x'] = data_x
        data_7['name_x'] = 'Epoch'
        data_7['name_y'] = 'IOU0.7_accuracy'
        data_7['data_y'] = data_y
        data_7['name'] = name
        data_7['color'] = ['#8AE09F', '#FA6F53']

    return HttpResponse(json.dumps({'data': data, 'data_5': data_5, 'data_7': data_7}))