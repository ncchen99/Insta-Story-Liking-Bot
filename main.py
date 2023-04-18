import os
from instagrapi import Client
from dotenv import load_dotenv
from time import sleep
from rich.console import Console

load_dotenv()

username = os.environ.get('ACCOUNT')
password = os.environ.get('PASSWORD')
ERFA = os.environ.get('ERFA', "false") == "true"  # 2fa
ERFA_code = ""

if ERFA:
    ERFA_code = input("🚀 Input verification code:")

class Animator():
    def __init__(self):
        self.console = Console()
        self.contents = {"login": ":smirk_cat: [bold cyan]Initialized[/bold cyan] instagrapi",
                         "get followers": ":smiling_imp: [bold #48C9B0 ]Login[/bold #48C9B0 ] successful",
                         "done": ":alien: [bold #AF7AC5]Get followers[/bold #AF7AC5] complete"}
        
    def createStatus(self):
        self.stat = self.console.status(
            status=f"[bold green]Working on initial...", spinner="moon")
        return self.stat
    
    def update(self, statusText):
        self.console.print(self.contents[statusText])
        self.ani.update(
            status=f"[bold green]Working on {statusText}...")

ani = Animator()
with ani.createStatus() as status:
    # initialize
    cl = Client()
    ani.update("login")

    # Login
    cl.login(username, password, verification_code=ERFA_code)
    ani.update("get followers")

    # Get the list of followers
    followers = cl.user_followers(cl.user_id)
    ani.update("done")
