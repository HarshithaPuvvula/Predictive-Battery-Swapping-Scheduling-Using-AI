from stations import stations
from logic import choose_best_station, expected_wait_time

# Dumb method: always go to nearest station
def nearest_station(stations):
    return min(stations, key=lambda s: s["distance_km"])

# Simulation
def simulate(strategy, users=50):
    total_wait = 0
    failures = 0

    for _ in range(users):
        station = strategy(stations)
        wait = expected_wait_time(station)

        total_wait += wait
        if station["charged_batteries"] == 0:
            failures += 1

    avg_wait = total_wait / users
    return avg_wait, failures
def simulate_with_depletion(strategy, users=50):
    total_wait = 0
    failures = 0

    # Copy station state
    temp_stations = [s.copy() for s in stations]

    for _ in range(users):
        station = strategy(temp_stations)

        if station["charged_batteries"] == 0:
            failures += 1
            continue

        station["charged_batteries"] -= 1
        wait = expected_wait_time(station)
        total_wait += wait

    successful_users = users - failures
    avg_wait = total_wait / max(successful_users, 1)
    return avg_wait, failures
def simulate_with_charging(strategy, users=50, charge_rate=1):
    total_wait = 0
    failures = 0

    temp_stations = [s.copy() for s in stations]

    for _ in range(users):

        # charging happens before next user arrives
        for s in temp_stations:
            s["charged_batteries"] += charge_rate

        station = strategy(temp_stations)

        if station["charged_batteries"] == 0:
            failures += 1
            continue

        station["charged_batteries"] -= 1
        wait = expected_wait_time(station)
        total_wait += wait

    successful = users - failures
    avg_wait = total_wait / max(successful, 1)
    return avg_wait, failures
from arrival_data import generate_arrival_data
from lstm_predictor import train_lstm, predict_next
from logic import dynamic_reserve, choose_station_with_reservation

def simulate_with_lstm(users=50, charge_rate=1):
    df = generate_arrival_data()
    arrivals = df["arrivals"].values

    model, scaler = train_lstm(arrivals)

    total_wait = 0
    failures = 0
    temp_stations = [s.copy() for s in stations]

    for i in range(users):

        # 🔁 charging step (THIS WAS MISSING)
        for s in temp_stations:
            s["charged_batteries"] += charge_rate

        # 🔮 predict arrival pressure
        history = arrivals[max(0, i-5):i+1]
        predicted = predict_next(model, scaler, history)
        reserve = dynamic_reserve(predicted)

        # 🧭 choose station with AI-aware reservation
        station = choose_station_with_reservation(temp_stations, reserve)

        if station["charged_batteries"] == 0:
            failures += 1
            continue

        station["charged_batteries"] -= 1
        wait = expected_wait_time(station)
        total_wait += wait

    successful = users - failures
    avg_wait = total_wait / max(successful, 1)
    return avg_wait, failures
