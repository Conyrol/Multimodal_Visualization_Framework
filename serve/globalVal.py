from queue import Queue
import nltk
from skipthoughts.skipthoughts import *
model_name = {"TALL": 0, "MAC": 0, "A2C": 0}

def init():
    global jShu
    global encoder
    global queue_skipThought_input
    global queue_skipThought_output
    jShu = 1
    print("预加载模型...")
    model = load_model()
    encoder = Encoder(model)
    print("预加载完成")

    print("创建线程消息队列...")
    queue = Queue()
    queue_skipThought_input = Queue()
    queue_skipThought_output = Queue()
    print("创建完成")