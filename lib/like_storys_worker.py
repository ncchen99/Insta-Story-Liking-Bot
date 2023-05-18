import threading
from instagrapi.exceptions import LoginRequired
from instagrapi.exceptions import FeedbackRequired


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
            try:
                self.cl.story_like(id)
                self.lock.acquire()
                self.progress.update(self.task, advance=1)
                self.lock.release()
            except LoginRequired:
                print("🥃 LoginRequired error occurred") 
                break
            except FeedbackRequired:
                print("🥃 FeedbackRequired error occurred") 
                break
            except Exception as e:
                print(f"Error occurred e: {e}")
