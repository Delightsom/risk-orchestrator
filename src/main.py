from workflow import apply_workflow

import argparse
from datetime import datetime, timedelta

from ingest import load_findings
from report import write_csv, write_exec_md
from metrics import calculate_metrics


def risk_priority(risk: str) -> int:
    return {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4,
    }.get(risk, 5)


def generate_poam(findings):
    poam = []
    today = datetime.today().date()

    for f in findings:
        due_dt = datetime.today() + timedelta(days=int(f["sla_days"]))
        due_date = due_dt.date()

        days_until_due = (due_date - today).days
        overdue = days_until_due < 0

        poam.append(
            {
                "id": f["id"],
                "risk": f["risk"],
                "priority": risk_priority(f["risk"]),
                "system": f["system"],
                "control": f.get("control", ""),
                "remediation": f["remediation"],
                "sla_days": int(f["sla_days"]),
                "due_date": due_date.strftime("%Y-%m-%d"),
                "status": "OVERDUE" if overdue else "OPEN",
                "days_until_due": days_until_due,
                "days_past_due": abs(days_until_due) if overdue else 0,
            }
        )

    poam.sort(key=lambda x: (x["priority"], x["days_until_due"]))
    return poam


def parse_args():
    parser = argparse.ArgumentParser(
        description="Risk Orchestrator: generate a POA&M register + executive summary from vulnerability findings."
    )

    parser.add_argument(
        "input",
        nargs="?",
        default="data/vulns_sample.csv",
        help="Path to input CSV findings file (default: data/vulns_sample.csv)",
    )

    parser.add_argument(
        "--out",
        default="reports",
        help="Output directory for generated reports (default: reports)",
    )

    parser.add_argument(
        "--format",
        default="csv,md",
        help="Comma-separated output formats: csv, md (default: csv,md)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    findings = load_findings(args.input)
    poam = generate_poam(findings)

    # Apply workflow AFTER poam exists
    wf = apply_workflow(poam)
    poam = wf.updated

    if wf.escalated:
        print("\nEscalations")
        print("-----------")
        for item in wf.escalated:
            print(
                f"{item['id']} | {item['risk']} | {item.get('system','')} | {item.get('control','')} | ESCALATED"
            )

    # Metrics (after workflow updates status/buckets)
    metrics = calculate_metrics(poam)
    print("\nRisk Metrics")
    print("-----------")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    # Outputs
    formats = {f.strip().lower() for f in args.format.split(",") if f.strip()}
    csv_path = None
    md_path = None

    if "csv" in formats:
        csv_path = write_csv(poam, out_dir=args.out)

    if "md" in formats:
        md_path = write_exec_md(poam, out_dir=args.out)

    # Console output
    print("\nPOA&M Tracker")
    print("-------------")
    for item in poam:
        print(item)

    if csv_path:
        print(f"\nGenerated: {csv_path}")
    if md_path:
        print(f"Generated: {md_path}")
