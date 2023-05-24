import queue
import threading
from instagrapi import Client
from rich.progress import Progress
from lib import get_storys_worker
from lib import like_storys_worker
from lib import animator
from lib import login

ani = animator.Animator()
cl = None

with ani.createStatus() as status:
    # initialize
    cl = Client()
    ani.update("login")

    # Login
    login.login_user(cl, status)
    ani.update("get following")

    # Get the list of following
    following = cl.user_following(cl.user_id)
    ani.update("done")


work_following = queue.Queue()
work_following.queue = queue.deque(following.keys())
work_storys = queue.Queue()

# 建立 lock
lock = threading.Lock()

workers = []

###############################################################

with Progress() as progress:

    task_following = progress.add_task("💀 [bold #EB984E]Getting[bold #EB984E] all users story", total=work_following.qsize())
    
    # 產生 20 個 worker
    for i in range(20):
        workers.append(get_storys_worker.Worker(work_following, lock, progress, task_following, work_storys, cl))
        workers[-1].start()

    for worker in workers:
        worker.join()

    ################################################################

    task_storys = progress.add_task("💓 [bold #F458F6]Liking storys[bold #F458F6]", total=work_storys.qsize())

    workers.clear()
    
    # adds a random delay between 1 and 3 seconds after each request
    cl.delay_range = [1, 3]

    # 產生 1 個 worker
    for i in range(1):
        workers.append(like_storys_worker.Worker(work_storys, lock, progress, task_storys, cl))
        workers[-1].start()

    for worker in workers:
        worker.join()

        


        
