import threading

class Worker(threading.Thread):
    def __init__(self, queue, lock, progress, task, work_storys, cl):
        threading.Thread.__init__(self)
        self.queue = queue
        self.lock = lock
        self.progress = progress
        self.task = task
        self.work_storys = work_storys
        self.cl = cl

    def run(self):
        while self.queue.qsize() > 0:
            following_id = self.queue.get()
            for i in self.cl.user_stories(following_id):
                self.work_storys.put(i.dict()["id"])
            self.lock.acquire()
            self.progress.update(self.task, advance=1)
            self.lock.release()
