from fastapi import FastAPI
from pydantic import BaseModel
from stations import stations

from logic import (
    expected_wait_time,
    cancellation_risk,
    confidence_badge,
    ai_assisted_station_choice,
    soc_urgency
)
from notifier import explain

app = FastAPI(title="EV Battery Swap Recommendation API")


# ----------- REQUEST MODEL -----------
class UserRequest(BaseModel):
    soc: int


# ----------- RESPONSE MODEL -----------
class RecommendationResponse(BaseModel):
    best_station: str
    distance_km: float
    expected_wait_time_min: int
    battery_available: bool
    confidence_badge: str
    cancellation_risk: str
    explanation: list[str]


# ----------- API ENDPOINT -----------
@app.post("/recommend", response_model=RecommendationResponse)
def recommend(user: UserRequest):

    # Case 1: Battery level is sufficient
    if user.soc > 30:
        return {
            "best_station": "NONE",
            "distance_km": 0.0,
            "expected_wait_time_min": 0,
            "battery_available": False,
            "confidence_badge": "HIGH",
            "cancellation_risk": "LOW",
            "explanation": [
                "Battery level is sufficient. No swapping required."
            ]
        }

    # 🔋 Step 1: Determine urgency from SOC
    urgency = soc_urgency(user.soc)

    # 🔮 Step 2: AI-assisted station selection (placeholder LSTM output)
    predicted_arrivals = 4  # simulated prediction
    best_station = ai_assisted_station_choice(stations, predicted_arrivals)

    # ⏳ Step 3: SOC-aware waiting time
    wait_time = expected_wait_time(best_station, urgency)

    # ⚠️ Step 4: Risk assessment
    risk = cancellation_risk(best_station)

    # 🟢🟡🔴 Step 5: Confidence calculation (SOC-aware)
    if urgency == "CRITICAL" and wait_time > 5:
        confidence = "LOW"
    else:
        confidence = confidence_badge(wait_time, risk)

    # 🧠 Step 6: Explanation
    explanation = explain(best_station)
    explanation.append(f"Battery urgency level: {urgency}")

    return {
        "best_station": best_station["id"],
        "distance_km": best_station["distance_km"],
        "expected_wait_time_min": wait_time,
        "battery_available": best_station["charged_batteries"] > 0,
        "confidence_badge": confidence,
        "cancellation_risk": risk,
        "explanation": explanation
    }

