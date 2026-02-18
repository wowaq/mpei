import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def menu_info():
    print("Welcome to the menu!")
    print("Please select an option:")
    print("1. Choice 1")
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
            choice = input("Enter your choice: ")
            if choice == "1":
                print("Choice 1 selected")
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
