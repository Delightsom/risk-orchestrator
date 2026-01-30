from datetime import datetime, timedelta
from scorer import score_vulnerability


def generate_poam(findings):
    poam = []

    for f in findings:
        risk, sla_days = score_vulnerability(f["severity"])
        due = datetime.today() + timedelta(days=sla_days)

        poam.append({
            "id": f["id"],
            "severity": f["severity"],
            "risk": risk,
            "system": f["system"],
            "remediation": f["remediation"],
            "due_date": due.strftime("%Y-%m-%d")
        })

    return poam


if __name__ == "__main__":
    sample_findings = [
        {
            "id": "VULN-001",
            "severity": "High",
            "system": "S3 Storage",
            "remediation": "Enable encryption at rest"
        },
        {
            "id": "VULN-002",
            "severity": "Medium",
            "system": "IAM",
            "remediation": "Rotate stale credentials"
        }
    ]

    poam = generate_poam(sample_findings)

    print("\nPOA&M Tracker\n-------------")
    for item in poam:
        print(item)

