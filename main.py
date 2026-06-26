from vault import ZedraVault
from auth import master_exists
from generator import generate_password, check_strength
from ui import (
    show_banner, show_menu, show_passwords,
    prompt_add, prompt_search, prompt_delete,
    show_success, show_error, show_strength, console
)
import getpass
import time

def main():
    vault = ZedraVault()
    show_banner()

    if not master_exists():
        console.print("\n[bold yellow]First time setup — create your master password.[/bold yellow]")
        while True:
            master = getpass.getpass("Create master password: ")
            confirm = getpass.getpass("Confirm master password: ")
            if master == confirm and len(master) >= 8:
                vault.setup(master)
                show_success("Master password set. Vault created.")
                break
            else:
                show_error("Passwords do not match or too short (min 8 chars).")
    else:
        console.print("\n[bold cyan]Enter your master password to unlock.[/bold cyan]")
        attempts = 0
        while attempts < 3:
            master = getpass.getpass("Master password: ")
            if vault.login(master):
                show_success("Vault unlocked.")
                break
            else:
                attempts += 1
                show_error(f"Wrong password. {3 - attempts} attempts left.")
        else:
            show_error("Too many failed attempts. Exiting.")
            return

    last_active = time.time()

    while True:
        if vault.auto_lock_check(last_active):
            show_error("Vault locked due to inactivity.")
            master = getpass.getpass("Master password: ")
            if vault.login(master):
                show_success("Vault unlocked.")
                last_active = time.time()
            else:
                show_error("Wrong password. Exiting.")
                break

        choice = show_menu()
        last_active = time.time()

        if choice == "1":
            site, username, password, notes = prompt_add()
            vault.add_password(site, username, password, notes)
            show_success("Password saved.")

        elif choice == "2":
            entries = vault.get_passwords()
            show_passwords(entries)

        elif choice == "3":
            site = prompt_search()
            entries = vault.search(site)
            show_passwords(entries)

        elif choice == "4":
            entries = vault.get_passwords()
            show_passwords(entries)
            entry_id = prompt_delete()
            vault.delete_password(entry_id)
            show_success("Entry deleted.")

        elif choice == "5":
            length = input("Password length (default 16): ").strip()
            length = int(length) if length.isdigit() else 16
            pwd = generate_password(length)
            console.print(f"\n[bold green]Generated: {pwd}[/bold green]")

        elif choice == "6":
            pwd = input("Enter password to check: ").strip()
            result = check_strength(pwd)
            show_strength(result)

        elif choice == "7":
            filename = vault.export_backup()
            show_success(f"Backup saved to {filename}")

        elif choice == "8":
            console.print("[cyan]Goodbye. Stay secure.[/cyan]")
            break

        else:
            show_error("Invalid option.")

if __name__ == "__main__":
    main()
