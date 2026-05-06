# logic.py
# Core decision-making logic

def expected_wait_time(station, urgency="MEDIUM"):
    base_wait = station["queue"] * 2

    if urgency == "CRITICAL":
        return max(0, base_wait - 2)
    elif urgency == "HIGH":
        return max(0, base_wait - 1)
    else:
        return base_wait



def cancellation_risk(station):
    """
    Estimate risk that a charged battery may not be available
    """
    demand_pressure = station["arrival_rate"] * 10
    supply = station["charged_batteries"]

    if demand_pressure < supply:
        return "LOW"
    elif demand_pressure < supply + 2:
        return "MEDIUM"
    else:
        return "HIGH"


def confidence_badge(wait_time, risk):
    """
    Confidence in recommendation
    """
    if wait_time <= 3 and risk == "LOW":
        return "HIGH"
    elif wait_time <= 6:
        return "MEDIUM"
    else:
        return "LOW"


def station_score(station):
    """
    Lower score = better station
    """
    return (
        station["distance_km"] * 0.4 +
        expected_wait_time(station) * 0.4 -
        station["charged_batteries"] * 0.2
    )


def choose_best_station(stations):
    return min(stations, key=station_score)
def choose_station_with_reservation(stations, reserve=1):
    viable = [s for s in stations if s["charged_batteries"] > reserve]

    if viable:
        return choose_best_station(viable)
    else:
        return choose_best_station(stations)
def dynamic_reserve(predicted_arrivals):
    """
    Decide reserve threshold based on predicted arrival pressure
    """
    if predicted_arrivals <= 2:
        return 0
    elif predicted_arrivals <= 4:
        return 1
    else:
        return 2
def ai_assisted_station_choice(stations, predicted_arrivals):
    reserve = dynamic_reserve(predicted_arrivals)
    return choose_station_with_reservation(stations, reserve)
def soc_urgency(soc):
    if soc <= 10:
        return "CRITICAL"
    elif soc <= 20:
        return "HIGH"
    else:
        return "MEDIUM"

import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
