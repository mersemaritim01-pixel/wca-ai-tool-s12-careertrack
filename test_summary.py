
from summary import generate_summary, display_summary

applications = [
    {"company": "NCBA Bank", "status": "Interview"},
    {"company": "Britam", "status": "Applied"},
    {"company": "Jubilee", "status": "Offer"},
    {"company": "Co-op Bank", "status": "Rejected"}
]

# Generate summary
result = generate_summary(applications)

print(result)

# Display summary
display_summary(applications)
