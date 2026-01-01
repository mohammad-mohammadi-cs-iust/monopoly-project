from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align
from rich.text import Text
import os

console = Console()


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    console.print("\n[gray]Press Enter to continue...[/gray]")
    input()


def show_title():
    title = Text("MONOPOLY", style="bold white on red", justify="center")
    subtitle = Text("Console Edition", style="italic bright_white")

    panel = Panel(
        Align.center(title + "\n" + subtitle),
        border_style="bright_white",
        padding=(1, 4)
    )
    console.print(panel)



def main_menu():
    table = Table(show_header=False, box=None, expand=True)

    table.add_row("[bold cyan]1[/bold cyan]", "New Game")
    table.add_row("[bold cyan]2[/bold cyan]", "Load Game")
    table.add_row("[bold cyan]3[/bold cyan]", "Leaderboard")
    table.add_row("[bold cyan]4[/bold cyan]", "Exit")

    panel = Panel(
        table,
        title="[bold yellow]Main Menu[/bold yellow]",
        border_style="green",
        padding=(1, 2)
    )

    console.print(panel)



def new_game_menu():
    table = Table(show_header=False, box=None, expand=True)

    table.add_row("[bold cyan]1[/bold cyan]", "Signup")
    table.add_row("[bold cyan]2[/bold cyan]", "Login")
    table.add_row("[bold cyan]3[/bold cyan]", "Exit")

    panel = Panel(
        table,
        title="[bold yellow]New Game[/bold yellow]",
        border_style="blue",
        padding=(1, 2)
    )

    console.print(panel)


def run_menu():
    while True:
        clear()
        show_title()
        main_menu()

        choice = Prompt.ask(
            "\n[bold white]Select an option[/bold white]",
            choices=["1", "2", "3", "4"]
        )

        clear()

        if choice == "1":
            while True:
                clear()
                show_title()
                new_game_menu()

                sub_choice = Prompt.ask(
                    "\n[bold white]Select an option[/bold white]",
                    choices=["1", "2", "3"]
                )

                if sub_choice == "3":
                    break

                pause()

        elif choice == "2":
            console.print("\n[bold blue]Load Game[/bold blue]")
            pause()

        elif choice == "3":
            console.print("\n[bold magenta]Leaderboard[/bold magenta]")
            pause()

        elif choice == "4":
            console.print("\n[bold red]Exiting Game...[/bold red]")
            break


if __name__ == "__main__":
    run_menu()
