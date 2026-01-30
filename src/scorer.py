def score_vulnerability(severity):
    mapping = {
        "Critical": ("High", 15),
        "High": ("High", 30),
        "Medium": ("Medium", 60),
        "Low": ("Low", 120)
    }
    return mapping.get(severity, ("Low", 120))
