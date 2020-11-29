import threading
import time
import globalVal
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
from queue import Queue
import torchvision
import numpy as np
import pickle
import os

from model_TALL import TALL
from model_A2C import A2C

class mesQueue():
    tallQueue_input = Queue()
    tallQueue_output = Queue()

    a2cQueue_input = Queue()
    a2cQueue_output = Queue()
    load_model_list = []
    runTALL = 1
    runA2C = 1

def determine_range_test(action, current_offset, ten_unit, num_units):
    abnormal_done = False
    update_offset = np.zeros(2, dtype=np.float32)
    update_offset_norm = np.zeros(2, dtype=np.float32)

    current_offset_start = int(current_offset[0][0])
    current_offset_end = int(current_offset[0][1])
    interval = current_offset_end - current_offset_start

    ten_unit = int(ten_unit)

    if action == 0:
        current_offset_start = current_offset_start + ten_unit
        current_offset_end = current_offset_end + ten_unit
    elif action == 1:
        current_offset_start = current_offset_start - ten_unit
        current_offset_end = current_offset_end - ten_unit
    elif action == 2:
        current_offset_start = current_offset_start + ten_unit
    elif action == 3:
        current_offset_start = current_offset_start - ten_unit
    elif action == 4:
        current_offset_end = current_offset_end + ten_unit
    elif action == 5:
        current_offset_end = current_offset_end - ten_unit

    if current_offset_start < 0:
        current_offset_start = 0
        if current_offset_end < 0:
            abnormal_done = True

    if current_offset_end > num_units:
        current_offset_end = num_units
        if current_offset_start > num_units:
            abnormal_done = True

    if current_offset_end <= current_offset_start:
        abnormal_done = True

    current_offset_start_norm = current_offset_start / float(num_units - 1)
    current_offset_end_norm = current_offset_end / float(num_units - 1)

    update_offset_norm[0] = current_offset_start_norm
    update_offset_norm[1] = current_offset_end_norm

    update_offset[0] = current_offset_start
    update_offset[1] = current_offset_end

    update_offset = torch.from_numpy(update_offset)
    update_offset = update_offset.unsqueeze(0)

    update_offset_norm = torch.from_numpy(update_offset_norm)
    update_offset_norm = update_offset_norm.unsqueeze(0)

    return current_offset_start, current_offset_end, update_offset, update_offset_norm, abnormal_done

def sortKey(elem):
    return elem[2]

def read_sentence_featmaps(sentence):
    sentence_check = sentence.replace(' ', '').replace('.', '').replace('a', '').replace('the', '')
    data_path = "./data/sentence_data/"
    if sentence_check + ".pkl" not in os.listdir(data_path):
        vectors = globalVal.encoder.encode([sentence])
        data = vectors[0]
    else:
        with open(data_path + sentence_check + ".pkl", 'rb') as f:
            data = pickle.load(f, encoding = 'iso-8859-1')
    return data

def read_video_featmaps(video_name):
    data_path = "./data/video_data/TALL/"
    if video_name + ".pkl" not in os.listdir(data_path):
        return -1
    with open(data_path + video_name + ".pkl", 'rb') as f:
        data = pickle.load(f, encoding = 'iso-8859-1')
    return data

def read_video_featmaps2(video_name):
    data_path = "./data/video_data/A2C/"
    if video_name + ".pkl" not in os.listdir(data_path):
        return -1
    with open(data_path + video_name + ".pkl", 'rb') as f:
        data = pickle.load(f, encoding = 'iso-8859-1')
    print(len(data))
    return data

class TALL_thread(threading.Thread):
    def __init__(self, model_name):
        threading.Thread.__init__(self)
        self.model_name = model_name
        
    def run(self):
        try:
            net = TALL()
            checkpoint = torch.load('./model/{}/model/best_R5_IOU5_model.t7'.format(self.model_name), map_location = 'cpu')
            net.load_state_dict(checkpoint['net'])
        except: return
        while(mesQueue.runTALL):
            time.sleep(1)
            if mesQueue.tallQueue_input.qsize() != 0:
                all_data_list = []
                betList = mesQueue.tallQueue_input.get()
                sentence = betList[0]
                video_name = betList[1]

                test_featmaps = read_video_featmaps(video_name)
                if test_featmaps == -1:
                    print('without video data')
                    continue

                sent_vec = read_sentence_featmaps(sentence)
                sent_vec = np.reshape(sent_vec, [1, sent_vec.shape[0]])  # 1,4800
                sent_vec = torch.from_numpy(sent_vec)
            
                for i in test_featmaps:
                    featmap = i[1]
                    featmap = np.reshape(featmap, [1, featmap.shape[0]])
                    featmap = torch.from_numpy(featmap)
                    visual_clip_name = i[0]
                    start = float(visual_clip_name.split("_")[1])
                    end = float(visual_clip_name.split("_")[2].split("_")[0])
                    outputs = net(featmap, sent_vec)
                    reg_end = end + outputs[2]
                    reg_start = start + outputs[1]
                    all_data_list.append([reg_start.item(), reg_end.item(), outputs[0].item()])
                mesQueue.tallQueue_output.put(sorted(all_data_list, key = sortKey, reverse = True)[:5])

class MAC_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        pass

class A2C_thread(threading.Thread):
    def __init__(self, model_name):
        threading.Thread.__init__(self)
        self.model_name = model_name
    
    def run(self):
        try:
            net = A2C()
            checkpoint = torch.load('./model/{}/model/best_R1_IOU5_model.t7'.format(self.model_name), map_location = 'cpu')
            net.load_state_dict(checkpoint['net'])
        except:
            return
        
        while(mesQueue.runA2C):
            time.sleep(1)
            if mesQueue.a2cQueue_input.qsize() != 0:
                all_data_list = []
                betList = mesQueue.a2cQueue_input.get()
                sentence = betList[0]
                video_name = betList[1]

                movie_clip_sentences, global_feature, original_feats, initial_feature, initial_offset, initial_offset_norm, ten_unit, num_units = read_video_featmaps2(video_name)
                global_feature = torch.from_numpy(global_feature).unsqueeze(0)
                original_feats = torch.from_numpy(original_feats).unsqueeze(0)
                initial_feature = torch.from_numpy(initial_feature).unsqueeze(0)
                initial_offset = torch.from_numpy(initial_offset).unsqueeze(0)
                initial_offset_norm = torch.from_numpy(initial_offset_norm).unsqueeze(0)
                ten_unit = torch.from_numpy(ten_unit).unsqueeze(0)
                num_units = torch.from_numpy(num_units).unsqueeze(0)

                print(sentence)
                sent_vec = read_sentence_featmaps(sentence)
                sent_vec = np.reshape(sent_vec, [1, sent_vec.shape[0]])  # 1,4800
                sent_vec = torch.from_numpy(sent_vec)
            
                for step in range(10):
                    if step == 0:
                        hidden_state = torch.zeros(1, 1024)
                        current_feature = initial_feature
                        current_offset = initial_offset
                        current_offset_norm = initial_offset_norm

                    hidden_state, logit, value, tIoU, location = net(global_feature, current_feature, sent_vec, current_offset_norm, hidden_state)

                    prob = F.softmax(logit, dim = 1)
                    action = prob.max(1, keepdim=True)[1].data.numpy()[0, 0]
                    current_offset_start, current_offset_end, current_offset, current_offset_norm, abnormal_done = determine_range_test(action,current_offset, ten_unit, num_units)

                    if not abnormal_done:
                        current_feature = original_feats[0][(current_offset_start):(current_offset_end + 1)]
                        current_feature = torch.mean(current_feature, dim=0)
                        current_feature = current_feature.unsqueeze(0)

                    if action == 6 or abnormal_done == True:
                        break
                mesQueue.a2cQueue_output.put([[current_offset_start * 16, current_offset_end * 16]])


def run_model(model_name, sentence, video_name):
    global load_model_list
    global TALL_thread
    global A2C_thread

    if model_name in mesQueue.load_model_list:
        if model_name == "TALL":
            mesQueue.tallQueue_input.put([sentence, video_name])
        if model_name == "A2C":
            mesQueue.a2cQueue_input.put([sentence, video_name])
    else: 
        if model_name == "TALL":
            TALL_thread = TALL_thread(model_name)
            TALL_thread.start()
            mesQueue.tallQueue_input.put([sentence, video_name])
            mesQueue.load_model_list.append(model_name)

        if model_name == "A2C":
            A2C_thread = A2C_thread(model_name)
            A2C_thread.start()
            mesQueue.a2cQueue_input.put([sentence, video_name])
            mesQueue.load_model_list.append(model_name)