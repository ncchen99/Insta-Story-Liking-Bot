import os
from instagrapi import Client
from dotenv import load_dotenv
from time import sleep
from rich.console import Console
from rich.progress import track
from pprint import pprint

load_dotenv()

username = os.environ.get('ACCOUNT')
password = os.environ.get('PASSWORD')
ERFA = os.environ.get('ERFA', "false") == "true"  # 2fa
ERFA_code = ""

if ERFA:
    ERFA_code = input("🚀 Input verification code:")

class Animator():
    def __init__(self, console):
        self.console = console
        self.contents = {"login": ":smirk_cat: [bold cyan]Initialized[/bold cyan] instagrapi",
                         "get following": ":smiling_imp: [bold #48C9B0 ]Login[/bold #48C9B0 ] successful",
                         "done": ":alien: [bold #AF7AC5]Get following[/bold #AF7AC5] complete"}
        
    def createStatus(self):
        self.stat = self.console.status(
            status=f"[bold green]Working on initial...", spinner="moon")
        return self.stat
    
    def update(self, statusText):
        self.console.print(self.contents[statusText])
        self.stat.update(
            status=f"[bold green]Working on {statusText}...")


console = Console()
ani = Animator(console)
cl = None

with ani.createStatus() as status:
    # initialize
    cl = Client()
    ani.update("login")

    # Login
    cl.login(username, password, verification_code=ERFA_code)
    ani.update("get following")

    # Get the list of following
    followers = cl.user_following(cl.user_id)
    ani.update("done")


storys = []

console.print("💀 [bold #EB984E]Getting[bold #EB984E] all users story")
for follower_id in track(followers, description=""):
    storys.extend([i.dict()["id"] for i in cl.user_stories(follower_id)])

console.print("💓 [bold #F458F6]Liking storys[bold #F458F6]")
for id in track(storys, description=""):
    cl.story_like(id)
    


    
