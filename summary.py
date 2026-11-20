
def generate_summary(applications):
    """
    Generate statistics for job applications.
    """

    total = len(applications)

    statuses = {
        "Applied": 0,
        "Under Review": 0,
        "Interview": 0,
        "Rejected": 0,
        "Offer": 0,
        "Withdrawn": 0
    }

    for application in applications:
        status = application.get("status", "Applied")

        if status in statuses:
            statuses[status] += 1

    active = total - statuses["Withdrawn"]

    return {
        "total_applications": total,
        "active_applications": active,
        "under_review": statuses["Under Review"],
        "interviews": statuses["Interview"],
        "rejections": statuses["Rejected"],
        "offers": statuses["Offer"],
        "withdrawn": statuses["Withdrawn"],
        "status_breakdown": statuses
    }


def display_summary(applications):
    """
    Display application statistics.
    """

    summary = generate_summary(applications)

    print("\n========== CAREERTRACK SUMMARY ==========")

    print("Total Applications:", summary["total_applications"])
    print("Active Applications:", summary["active_applications"])
    print("Under Review:", summary["under_review"])
    print("Interviews:", summary["interviews"])
    print("Rejections:", summary["rejections"])
    print("Job Offers:", summary["offers"])
    print("Withdrawn:", summary["withdrawn"])

    print("\nStatus Breakdown:")

    for status, count in summary["status_breakdown"].items():
        print(f"{status}: {count}")

    print("=========================================")
