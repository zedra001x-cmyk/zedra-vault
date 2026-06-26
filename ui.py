from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

def show_banner():
    console.print(Panel.fit(
        "[bold cyan]ZEDRA VAULT[/bold cyan]\n[dim]Secure Password Manager v1.0[/dim]",
        border_style="cyan"
    ))

def show_menu():
    console.print("\n[bold yellow]MENU[/bold yellow]")
    console.print("[1] Add Password")
    console.print("[2] View All Passwords")
    console.print("[3] Search Password")
    console.print("[4] Delete Password")
    console.print("[5] Exit")
    return input("\nChoose option: ").strip()

def show_passwords(entries: list):
    if not entries:
        console.print("[red]No passwords found.[/red]")
        return
    table = Table(box=box.ROUNDED, border_style="cyan")
    table.add_column("ID", style="dim")
    table.add_column("Site", style="bold cyan")
    table.add_column("Username", style="green")
    table.add_column("Password", style="yellow")
    table.add_column("Notes", style="dim")
    for e in entries:
        table.add_row(
            str(e["id"]),
            e["site"],
            e["username"],
            e["password"],
            e["notes"] or ""
        )
    console.print(table)

def prompt_add():
    console.print("\n[bold cyan]Add New Password[/bold cyan]")
    site = input("Site/App name: ").strip()
    username = input("Username/Email: ").strip()
    password = input("Password: ").strip()
    notes = input("Notes (optional): ").strip()
    return site, username, password, notes

def prompt_search():
    return input("Enter site name to search: ").strip()

def prompt_delete():
    return int(input("Enter ID to delete: ").strip())

def show_success(msg: str):
    console.print(f"[bold green]✓ {msg}[/bold green]")

def show_error(msg: str):
    console.print(f"[bold red]✗ {msg}[/bold red]")
