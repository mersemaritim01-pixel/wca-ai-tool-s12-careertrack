
from job_tracker import JobTracker


# Create tracker
tracker = JobTracker()

# Add an application
application = tracker.add_application(
    company="NCBA Bank",
    job_title="Customer Service Officer",
    location="Nairobi",
    notes="Application submitted successfully."
)

print("\nAPPLICATION ADDED")
print(application)

# View applications
print("\nALL APPLICATIONS")
for app in tracker.view_applications():
    print(app)

# Update application status
tracker.update_application(
    application["id"],
    status="Interview"
)

print("\nUPDATED APPLICATION")
print(tracker.get_application(application["id"]))

# Search applications
print("\nSEARCH RESULTS")
print(tracker.search_applications("NCBA"))

# Delete application
# Uncomment the next two lines to test deletion.
# tracker.delete_application(application["id"])
# print("Application deleted successfully.")
