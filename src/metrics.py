from collections import Counter


def calculate_metrics(poam):
    total = len(poam)
    overdue = sum(1 for p in poam if p["status"] == "OVERDUE")
    critical = sum(1 for p in poam if p["risk"] == "Critical")

    by_risk = Counter(p["risk"] for p in poam)
    by_system = Counter(p["system"] for p in poam)

    return {
        "total_findings": total,
        "overdue": overdue,
        "critical": critical,
        "by_risk": dict(by_risk),
        "by_system": dict(by_system),
    }
