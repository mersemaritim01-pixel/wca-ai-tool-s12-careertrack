def display_menu():
    print("\n" + "=" * 40)
    print("       JOB APPLICATION TRACKER")
    print("=" * 40)

    print("1. Start a new conversation")
    print("2. View saved conversations")
    print("3. View job applications")
    print("4. View conversation summary")
    print("5. Exit")

    print("=" * 40)


def main():
    while True:
        display_menu()

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            print("\nStarting a new conversation...")

        elif choice == "2":
            print("\nSaved conversations will appear here.")

        elif choice == "3":
            print("\nYour job applications will appear here.")

        elif choice == "4":
            print("\nYour conversation summary will appear here.")

        elif choice == "5":
            print("\nThank you for using Job Application Tracker!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()