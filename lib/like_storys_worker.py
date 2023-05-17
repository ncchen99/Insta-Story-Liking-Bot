import random
import threading
import time

class Worker(threading.Thread):
    def __init__(self, queue, lock, progress, task, cl):
        threading.Thread.__init__(self)
        self.queue = queue
        self.lock = lock
        self.progress = progress
        self.task = task
        self.cl = cl

    def run(self):
        while self.queue.qsize() > 0:
            id = self.queue.get()
            # time.sleep(random.randint(1,5)) 防止違反社群法則用 
            self.cl.story_like(id)
            self.lock.acquire()
            self.progress.update(self.task, advance=1)
            self.lock.release()
