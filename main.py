
from job_tracker import JobTracker
from summary import display_summary
from memory import ConversationMemory
from ai_assistant import ask_with_memory
import json
from pathlib import Path

from ai_assistant import finalize_session


def display_menu():
    print("\n====================================")
    print("          CAREERTRACK AI")
    print("       JOB APPLICATION TRACKER")
    print("====================================")
    print("1. Add Job Application")
    print("2. View All Applications")
    print("3. Update Application")
    print("4. Delete Application")
    print("5. Search Applications")
    print("6. View Application Summary")
    print("7. Ask CareerTrack AI")
    print("8. Exit")
    print("====================================")



def add_application(tracker):
    print("\n--- ADD JOB APPLICATION ---")

    company = input("Company name: ")
    job_title = input("Job title: ")
    location = input("Location: ")
    salary = input("Salary (e.g. KES 50,000): ")
    interview_date = input("Interview date (YYYY-MM-DD, or leave blank): ")
    follow_up_date = input("Follow-up date (YYYY-MM-DD, or leave blank): ")
    notes = input("Additional notes: ")

    try:
        application = tracker.add_application(
            company=company,
            job_title=job_title,
            location=location,
            salary=salary,
            interview_date=interview_date,
            follow_up_date=follow_up_date,
            notes=notes
        )

        print("\nApplication added successfully!")
        print("Application ID:", application["id"])

    except ValueError as error:
        print("Error:", error)

def view_applications(tracker):
    print("\n--- ALL JOB APPLICATIONS ---")

    applications = tracker.view_applications()

    if not applications:
        print("No applications found.")
        return

    for app in applications:
        print("\nCompany:", app["company"])
        print("Job Title:", app["job_title"])
        print("Location:", app["location"])
        print("Salary:", app.get("salary", "Not provided"))
        print("Interview Date:", app.get("interview_date", "Not set"))
        print("Follow-up Date:", app.get("follow_up_date", "Not set"))
        print("Status:", app["status"])
        print("Application Date:", app["application_date"])
        print("Application ID:", app["id"])


def update_application(tracker):
    print("\n--- UPDATE APPLICATION ---")

    application_id = input("Enter application ID: ")

    application = tracker.get_application(application_id)

    if application is None:
        print("Application not found.")
        return

    print("1. Update company")
    print("2. Update job title")
    print("3. Update location")
    print("4. Update salary")
    print("5. Update application date")
    print("6. Update interview date")
    print("7. Update follow-up date")
    print("8. Update status")
    print("9. Update notes")

    choice = input("Choose what to update: ")

    fields = {
        "1": "company",
        "2": "job_title",
        "3": "location",
        "4": "salary",
        "5": "application_date",
        "6": "interview_date",
        "7": "follow_up_date",
        "8": "status",
        "9": "notes"
}

    if choice not in fields:
        print("Invalid choice.")
        return

    field = fields[choice]
    new_value = input(f"Enter new {field}: ")

    if field == "status":
        print("Valid statuses: Applied, Under Review, Interview, Rejected, Offer, Withdrawn")

    try:
        success = tracker.update_application(
            application_id, **{field: new_value}
        )

        if success:
            print("Application updated successfully!")

    except ValueError as error:
        print("Error:", error)


def delete_application(tracker):
    print("\n--- DELETE APPLICATION ---")

    application_id = input("Enter application ID: ")

    application = tracker.get_application(application_id)

    if application is None:
        print("Application not found.")
        return

    confirm = input(
        f"Delete {application['job_title']} at "
        f"{application['company']}? (yes/no): "
    )

    if confirm.lower() == "yes":
        tracker.delete_application(application_id)
        print("Application deleted successfully!")
    else:
        print("Deletion cancelled.")


def search_applications(tracker):
    print("\n--- SEARCH APPLICATIONS ---")

    keyword = input(
        "Enter company name, job title or location: "
    )

    results = tracker.search_applications(keyword)

    if not results:
        print("No matching applications found.")
        return

    print("\n--- SEARCH RESULTS ---")

    for app in results:
        print("\nCompany:", app["company"])
        print("Job Title:", app["job_title"])
        print("Location:", app["location"])
        print("Salary:", app.get("salary", "Not provided"))
        print("Status:", app["status"])
        print("Interview Date:", app.get("interview_date", "Not set"))
        print("Follow-up Date:", app.get("follow_up_date", "Not set"))
        print("Application ID:", app["id"])


def ask_ai(memory, tracker):
    print("\n--- CAREERTRACK AI ASSISTANT ---")

    question = input("Ask your question: ").strip()

    if not question:
        print("Please enter a question.")
        return

    try:
        result = ask_with_memory(
            question,
            memory,
            tracker.view_applications()
        )

        print("\nCareerTrack AI:")
        print(result["reply"])

    except Exception as error:
        print("\nUnable to connect to the AI assistant.")
        print("Error:", error)
        print("Please check your API configuration and try again.")

def display_session_menu():
    print("\n====================================")
    print("       CAREERTRACK AI")
    print("         SESSION MENU")
    print("====================================")
    print("1. Start New Session")
    print("2. Open Previous Session")
    print("3. Exit")
    print("====================================")


def open_previous_session():
    session_folder = Path(__file__).resolve().parent / "sessions"

    if not session_folder.exists():
        print("No saved sessions found.")
        return

    session_files = sorted(
        session_folder.glob("session_*.json"),
        reverse=True
    )

    if not session_files:
        print("No completed sessions found.")
        return

    print("\n--- SAVED CONVERSATION SESSIONS ---")

    for index, file_path in enumerate(session_files, start=1):
        print(f"{index}. {file_path.name}")

    choice = input("\nSelect session number (or 0 to go back): ")

    if choice == "0":
        return

    try:
        selected = int(choice)

        if selected < 1 or selected > len(session_files):
            print("Invalid session selection.")
            return

        with open(session_files[selected - 1], "r", encoding="utf-8") as file:
            session = json.load(file)

        print("\n========== SAVED SESSION ==========")
        print("Session ID:", session.get("session_id"))
        print("Date:", session.get("date"))

        print("\nCONVERSATION HISTORY:")

        for message in session.get("conversation_history", []):
            print(f"\n{message['role'].upper()}: {message['content']}")

        print("\nFINAL SUMMARY:")
        print(json.dumps(session.get("summary", {}), indent=4))

    except ValueError:
        print("Please enter a valid number.")

    except (OSError, json.JSONDecodeError) as error:
        print("Unable to open session:", error)


def start_new_session(tracker):
    print("\nStarting a new CareerTrack AI session...")

    memory = ConversationMemory()

    while True:
        display_menu()

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_application(tracker)

        elif choice == "2":
            view_applications(tracker)
            input("\nPress Enter to return to the menu...")

        elif choice == "3":
            update_application(tracker)

        elif choice == "4":
            delete_application(tracker)

        elif choice == "5":
            search_applications(tracker)

        elif choice == "6":
            display_summary(tracker.view_applications())
            input("\nPress Enter to return to the menu...")

        elif choice == "7":
            ask_ai(memory, tracker)

        elif choice == "8":
            print("\nSaving your conversation session...")
            finalize_session(memory)
            print("Session completed successfully!")
            break

        else:
            print("Invalid choice. Please select 1-8.")


def main():
    tracker = JobTracker()

    print("\nWelcome to CareerTrack AI!")

    while True:
        display_session_menu()

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            start_new_session(tracker)

        elif choice == "2":
            open_previous_session()
            input("\nPress Enter to return to the menu...")

        elif choice == "3":
            print("\nThank you for using CareerTrack AI!")
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-3.")


if __name__ == "__main__":
    main()
