import csv

def load_findings(csv_path):
    findings = []

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            findings.append({
                "id": row["id"],
                "risk": row["risk"],
                "system": row["system"],
                "control": row.get("control", "UNMAPPED"),
                "remediation": row["remediation"],
                "sla_days": int(row["sla_days"])
            })

    return findings
