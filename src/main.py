from datetime import datetime, timedelta

def generate_poam(findings):
    poam = []
    for f in findings:
        due = datetime.today() + timedelta(days=f["sla_days"])
        poam.append({
            "id": f["id"],
            "risk": f["risk"],
            "system": f["system"],
            "remediation": f["remediation"],
            "due_date": due.strftime("%Y-%m-%d")
        })
    return poam


if __name__ == "__main__":
    sample_findings = [
        {
            "id": "VULN-001",
            "risk": "High",
            "system": "S3 Storage",
            "remediation": "Enable encryption at rest",
            "sla_days": 30
        },
        {
            "id": "VULN-002",
            "risk": "Medium",
            "system": "IAM",
            "remediation": "Rotate stale credentials",
            "sla_days": 60
        }
    ]

    poam = generate_poam(sample_findings)

    print("\nPOA&M Tracker\n-------------")
    for item in poam:
        print(item)
