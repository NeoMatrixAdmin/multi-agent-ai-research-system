from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.text import Text
import time

console = Console()


def header():
    console.print(
        Panel.fit(
            "[bold cyan]🤖 MULTI-AGENT AI RESEARCH SYSTEM[/bold cyan]\n"
            "[dim]Enterprise-grade LLM Orchestration[/dim]",
            border_style="cyan",
        )
    )


def section(title: str):
    console.print(Rule(f"[bold yellow]{title}[/bold yellow]"))


def log(msg: str, style="white"):
    console.print(f"[{style}]{msg}[/{style}]")


class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.elapsed = time.time() - self.start
