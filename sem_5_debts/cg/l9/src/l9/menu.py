import os
import platform
import subprocess
from pathlib import Path


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def bold(text):
    return f"\033[1m{str(text)}\033[0m"


def italic(text):
    return f"\033[3m{str(text)}\033[0m"


def underline(text):
    return f"\033[4m{str(text)}\033[0m"


def open_file(relative_path, go_up_two_levels=True):
    """
    Open a file with path relative to the script's location, optionally going up two directories.

    Args:
        relative_path (str): The relative path to the file from the target directory
        go_up_two_levels (bool): If True, starts from ../../, if False starts from script directory

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        script_dir = Path(__file__).parent.absolute()
        if go_up_two_levels:
            base_dir = script_dir.parent.parent
            print(f"Starting from: ../../ ({base_dir})")
        else:
            base_dir = script_dir
            print(f"Starting from script directory: {base_dir}")

        full_path = base_dir / relative_path
        full_path = full_path.resolve()

        if not full_path.exists():
            print(f"File not found: {full_path}")
            return False

        print(f"Opening file: {full_path}")
        if platform.system() == "Windows":
            os.startfile(str(full_path))
        elif platform.system() == "Darwin":
            subprocess.run(["open", str(full_path)])
        else:
            subprocess.run(["xdg-open", str(full_path)])

        return True

    except Exception as e:
        print(f"Error opening file: {e}")
        return False


def menu_info():
    print("Лабораторная работа №9 по компьютерной графике.")
    print("Выберите ")
    print(f"1. Открыть отчёт({italic('README.md')})")
    print("2. Choice 2")
    print("3. Choice 3")
    print("4. Choice 4")
    print("5. Choice 5")
    print("6. Choice 6")
    print("7. Choice 7")
    print("8. Choice 8")
    print("9. Choice 9")
    print("10. Choice 10")
    print("exit. Exit")


def menu_loop():
    try:
        while True:
            clear_screen()
            menu_info()
            choice = input("Выбор ")
            if choice == "1":
                open_file("README.md")
            elif choice == "2":
                print("Choice 2 selected")
            elif choice == "3":
                print("Choice 3 selected")
            elif choice == "4":
                print("Choice 4 selected")
            elif choice == "5":
                print("Choice 5 selected")
            elif choice == "6":
                print("Choice 6 selected")
            elif choice == "7":
                print("Choice 7 selected")
            elif choice == "8":
                print("Choice 8 selected")
            elif choice == "9":
                print("Choice 9 selected")
            elif choice == "10":
                print("Choice 10 selected")
            elif choice == "exit":
                break
            else:
                print("Invalid choice")
            input("Press Enter to continue...")
    except KeyboardInterrupt:
        print("\nExiting...")
