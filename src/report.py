from pathlib import Path

def write_csv(poam, out_path="reports/poam_register.csv"):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    header = "id,risk,priority,system,control,remediation,due_date,status,days_to_due,overdue_days,age_bucket\n"
    lines = [header]

    for item in poam:
        lines.append(
            f'{item["id"]},{item["risk"]},{item["priority"]},'
            f'{item["system"]},{item["control"]},"{item["remediation"]}",'
            f'{item["due_date"]},{item["status"]},{item["days_to_due"]},'
            f'{item["overdue_days"]},{item["age_bucket"]}\n'
        )

    Path(out_path).write_text("".join(lines), encoding="utf-8")
    return out_path


def write_exec_md(poam, out_path="reports/executive_summary.md"):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    total = len(poam)

    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    overdue_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    bucket_counts = {"0-30": 0, "31-60": 0, "61-90": 0, "90+": 0}

    for p in poam:
        counts[p["risk"]] = counts.get(p["risk"], 0) + 1
        bucket_counts[p["age_bucket"]] = bucket_counts.get(p["age_bucket"], 0) + 1
        if p["status"] == "OVERDUE":
            overdue_counts[p["risk"]] = overdue_counts.get(p["risk"], 0) + 1

    overdue_total = sum(overdue_counts.values())

    # Top lists
    top_overdue = sorted([p for p in poam if p["status"] == "OVERDUE"], key=lambda x: (-x["overdue_days"], x["priority"]))[:5]
    top_priority = sorted(poam, key=lambda x: (x["priority"], -x["overdue_days"]))[:5]

    md = []
    md.append("# Executive Risk Summary\n\n")
    md.append(f"**Total findings:** {total}\n\n")

    md.append("## Risk Breakdown\n\n")
    md.append(f"- Critical: **{counts.get('Critical', 0)}** (Overdue: **{overdue_counts.get('Critical', 0)}**)\n")
    md.append(f"- High: **{counts.get('High', 0)}** (Overdue: **{overdue_counts.get('High', 0)}**)\n")
    md.append(f"- Medium: **{counts.get('Medium', 0)}** (Overdue: **{overdue_counts.get('Medium', 0)}**)\n")
    md.append(f"- Low: **{counts.get('Low', 0)}** (Overdue: **{overdue_counts.get('Low', 0)}**)\n")
    md.append(f"\n**Total overdue:** {overdue_total}\n\n")

    md.append("## SLA Age Buckets (by assigned SLA days)\n\n")
    md.append(f"- 0–30: **{bucket_counts.get('0-30', 0)}**\n")
    md.append(f"- 31–60: **{bucket_counts.get('31-60', 0)}**\n")
    md.append(f"- 61–90: **{bucket_counts.get('61-90', 0)}**\n")
    md.append(f"- 90+: **{bucket_counts.get('90+', 0)}**\n\n")

    md.append("## Top Priority Items\n\n")
    for item in top_priority:
        md.append(
            f'- **{item["id"]}** ({item["risk"]}) [{item["status"]}] '
            f'{item["system"]} | {item["control"]} | Due {item["due_date"]} | Days-to-due {item["days_to_due"]}\n'
        )

    md.append("\n## Top Overdue Items\n\n")
    if not top_overdue:
        md.append("- None overdue.\n")
    else:
        for item in top_overdue:
            md.append(
                f'- **{item["id"]}** ({item["risk"]}) OVERDUE by {item["overdue_days"]} days '
                f'| {item["system"]} | {item["control"]} | Due {item["due_date"]}\n'
            )

    Path(out_path).write_text("".join(md), encoding="utf-8")
    return out_path


