import csv
import os


def write_csv(poam, out_dir="reports"):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "poam_register.csv")

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=poam[0].keys())
        writer.writeheader()
        writer.writerows(poam)

    return path


def write_exec_md(poam, out_dir="reports"):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "executive_summary.md")

    total = len(poam)
    overdue = sum(1 for p in poam if p["status"] == "OVERDUE")

    with open(path, "w", encoding="utf-8") as f:
        f.write("# Executive Risk Summary\n\n")
        f.write(f"- Total findings: {total}\n")
        f.write(f"- Overdue: {overdue}\n\n")

        f.write("| ID | Risk | System | Control | Due Date | Status |\n")
        f.write("|----|------|--------|---------|---------|--------|\n")

        for p in poam:
            f.write(
                f"| {p['id']} | {p['risk']} | {p['system']} | {p['control']} | {p['due_date']} | {p['status']} |\n"
            )

    return path
