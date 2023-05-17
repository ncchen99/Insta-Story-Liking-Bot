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