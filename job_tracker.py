import json
import uuid
from pathlib import Path
from datetime import date


# Location for storing job applications
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATA_FILE = DATA_DIR / "applications.json"


class JobTracker:

    def __init__(self):
        self.applications = []
        self.load_applications()

    def load_applications(self):
        """Load applications from JSON storage."""

        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                self.applications = json.load(file)

            if not isinstance(self.applications, list):
                raise ValueError("Invalid applications data.")

            # Add missing fields to older records
            # without deleting existing information.
            for application in self.applications:
                application.setdefault("salary", "")
                application.setdefault("interview_date", "")
                application.setdefault("follow_up_date", "")

    def save_applications(self):
        """Save applications to JSON storage."""

        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.applications, file, indent=4)

    def validate_date(self, value, field_name):
        """Check that a date uses YYYY-MM-DD format."""

        if value == "":
            return

        try:
            date.fromisoformat(value)
        except (ValueError, TypeError):
            raise ValueError(
                f"{field_name} must use YYYY-MM-DD format."
            )

    def add_application(
        self,
        company,
        job_title,
        location="",
        salary="",
        interview_date="",
        follow_up_date="",
        notes=""
    ):
        """Add a new job application."""

        if not company.strip() or not job_title.strip():
            raise ValueError("Company and job title are required.")

        self.validate_date(interview_date, "Interview date")
        self.validate_date(follow_up_date, "Follow-up date")

        application = {
            "id": str(uuid.uuid4()),
            "company": company.strip(),
            "job_title": job_title.strip(),
            "location": location.strip(),
            "salary": salary.strip(),
            "application_date": date.today().isoformat(),
            "interview_date": interview_date.strip(),
            "follow_up_date": follow_up_date.strip(),
            "status": "Applied",
            "notes": notes.strip()
        }

        self.applications.append(application)
        self.save_applications()

        return application

    def view_applications(self):
        """Return all job applications."""

        return self.applications

    def get_application(self, application_id):
        """Find an application using its ID."""

        for application in self.applications:
            if application["id"] == application_id:
                return application

        return None

    def update_application(self, application_id, **updates):
        """Update application details."""

        allowed_fields = {
            "company",
            "job_title",
            "location",
            "salary",
            "application_date",
            "interview_date",
            "follow_up_date",
            "status",
            "notes"
        }

        valid_statuses = {
            "Applied",
            "Under Review",
            "Interview",
            "Rejected",
            "Offer",
            "Withdrawn"
        }

        application = self.get_application(application_id)

        if application is None:
            return False

        # Validate all updates before changing the record
        for field, value in updates.items():

            if field not in allowed_fields:
                raise ValueError(f"Invalid field: {field}")

            if not isinstance(value, str):
                raise ValueError(f"{field} must be text.")

            if field in {"company", "job_title"} and not value.strip():
                raise ValueError(f"{field} cannot be empty.")

            if field in {
                "application_date",
                "interview_date",
                "follow_up_date"
            }:
                self.validate_date(value, field)

            if field == "status" and value not in valid_statuses:
                raise ValueError("Invalid application status.")

        for field, value in updates.items():
            application[field] = value.strip()

        self.save_applications()
        return True

    def delete_application(self, application_id):
        """Delete an application."""

        application = self.get_application(application_id)

        if application is None:
            return False

        self.applications.remove(application)
        self.save_applications()

        return True

    def search_applications(self, keyword):
        """Search applications by company, title or location."""

        keyword = keyword.strip().lower()

        if not keyword:
            return []

        return [
            application
            for application in self.applications
            if keyword in application["company"].lower()
            or keyword in application["job_title"].lower()
            or keyword in application["location"].lower()
        ]
