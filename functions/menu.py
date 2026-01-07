import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align
from rich.text import Text
from user.signup import run_signup
from user.login import run_login
from functions.loadgame import run_loadgame
import json
console = Console()

USERS_FILE = os.path.join(BASE_DIR, "user", "users.json")


def get_top_players(limit=5):
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(users, list):
        return []

    for user in users:
        user["point"] = user.get("point", 0)

    users.sort(key=lambda u: u["point"], reverse=True)

    return users[:limit]



def show_leaderboard():
    clear()
    show_title()

    top_players = get_top_players()

    if not top_players:
        console.print("[bold red]No users found![/bold red]")
        pause()
        return

    table = Table(
        title="[bold magenta]🏆 Top Players Leaderboard[/bold magenta]",
        header_style="bold cyan",
        expand=True
    )

    table.add_column("Rank", justify="center")
    table.add_column("Username", justify="center")
    table.add_column("Email", justify="center")
    table.add_column("Points", justify="center")

    for idx, user in enumerate(top_players, start=1):
        point = user.get("point", 0)

        point_style = "green" if point > 0 else "dim"
        table.add_row(
            str(idx),
            user.get("username", "-"),
            user.get("email", "-"),
            f"[{point_style}]{point}[/{point_style}]"
        )

    console.print(table)
    pause()



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

                elif sub_choice=="1":
                    clear()
                    run_signup()

                elif sub_choice=="2":
                    clear()
                    func=run_login()

                    if(func):
                        return True

                


                pause()

        elif choice == "2":
            clear()
            func=run_loadgame()

            if(func):
                return True

        elif choice == "3":
            show_leaderboard()

        elif choice == "4":
            console.print("\n[bold red]Exiting Game...[/bold red]")
            break


if __name__ == "__main__":
    run_menu()
