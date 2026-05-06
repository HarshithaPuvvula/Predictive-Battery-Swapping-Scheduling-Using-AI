# notifier.py
# Generates human-readable explanation for recommendation

def explain(station):
    reasons = []

    if station["charged_batteries"] >= 3:
        reasons.append("High number of charged batteries available")

    if station["queue"] <= 2:
        reasons.append("Low waiting queue at the station")

    if station["distance_km"] <= 2.5:
        reasons.append("Station is relatively nearby")

    return reasons
