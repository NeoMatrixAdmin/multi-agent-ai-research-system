from dotenv import load_dotenv
load_dotenv()

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from core.memory import ResearchMemory
from core.orchestrator import Orchestrator

from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.analyst import AnalystAgent
from agents.writer import WriterAgent
from agents.fact_checker import FactCheckerAgent

from datetime import datetime
import re
import os


app = typer.Typer()
console = Console()


def show_header():
    console.print(
        Panel.fit(
            "[bold cyan]🤖 MULTI-AGENT AI RESEARCH SYSTEM[/bold cyan]\n"
            "[dim]Enterprise-grade LLM Orchestration[/dim]",
            border_style="cyan",
        )
    )


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:50]


@app.command()
def run():
    show_header()

    query = Prompt.ask(
        "[bold yellow]Enter your research prompt[/bold yellow]"
    )

    console.print(f"\n[bold cyan]Message:[/bold cyan]\n{query}\n")

    memory = ResearchMemory(query)

    orchestrator = Orchestrator(
        planner=PlannerAgent(),
        researcher=ResearcherAgent(),
        analyst=AnalystAgent(),
        writer=WriterAgent(),
        fact_checker=FactCheckerAgent(),
        memory=memory,
    )

    result = orchestrator.run()

    if result["status"] == "approved":
        # 🔐 ensure output directory exists
        os.makedirs("outputs/reports", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_slug = slugify(query)

        output_path = f"outputs/reports/{timestamp}_{query_slug}.md"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["draft"]["markdown"])

        console.print(
            f"\n[bold green]✔ Report saved to:[/bold green] {output_path}"
        )
    else:
        console.print(
            "\n[bold red]✖ Research failed or insufficient evidence found.[/bold red]"
        )


if __name__ == "__main__":
    app()
