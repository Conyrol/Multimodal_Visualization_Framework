import threading
import globalVal
import time
from skipthoughts.skipthoughts import *

class skipThoughts_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        while(1):
            time.sleep(1)
            if globalVal.queue_skipThought_input.qsize() != 0:
                sentence = globalVal.queue_skipThought_input.get()
                vectors = globalVal.encoder.encode([sentence])
                print(vectors)