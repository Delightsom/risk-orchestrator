import sys
from datetime import datetime, timedelta

from ingest import load_findings
from report import write_csv, write_exec_md


def risk_priority(risk):
    return {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4
    }.get(risk, 5)


def generate_poam(findings):
    poam = []
    today = datetime.today().date()

    for f in findings:
        due_dt = datetime.today() + timedelta(days=f["sla_days"])
        due_date = due_dt.date()

        days_to_due = (due_date - today).days
        overdue_days = abs(days_to_due) if days_to_due < 0 else 0
        status = "OVERDUE" if days_to_due < 0 else "OPEN"

        age_bucket = (
            "0-30" if f["sla_days"] <= 30 else
            "31-60" if f["sla_days"] <= 60 else
            "61-90" if f["sla_days"] <= 90 else
            "90+"
        )

        poam.append({
            "id": f["id"],
            "risk": f["risk"],
            "priority": risk_priority(f["risk"]),
            "system": f["system"],
            "control": f["control"],
            "remediation": f["remediation"],
            "due_date": due_date.strftime("%Y-%m-%d"),
            "status": status,
            "days_to_due": days_to_due,
            "overdue_days": overdue_days,
            "age_bucket": age_bucket
        })

    poam.sort(key=lambda x: (x["priority"], -x["overdue_days"]))
    return poam



if __name__ == "__main__":
    csv_input = sys.argv[1] if len(sys.argv) > 1 else "data/vulns_sample.csv"

    findings = load_findings(csv_input)
    poam = generate_poam(findings)

    csv_path = write_csv(poam)
    md_path = write_exec_md(poam)

    print("\nPOA&M Tracker\n-------------")
    for item in poam:
        print(item)

    print(f"\nGenerated: {csv_path}")
    print(f"Generated: {md_path}")
