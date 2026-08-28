from utils.helpers import TripRequest


def analyze_budget(trip: TripRequest):
    total_budget = trip.budget
    travelers = trip.travelers
    days = trip.days

    budget_per_person = total_budget / travelers
    budget_per_day = total_budget / days
    budget_per_person_per_day = total_budget / (travelers * days)

    return {
        "total_budget": total_budget,
        "travelers": travelers,
        "days": days,
        "budget_per_person": round(budget_per_person, 2),
        "budget_per_day": round(budget_per_day, 2),
        "budget_per_person_per_day": round(
            budget_per_person_per_day,
            2
        ),
        "transport_preference": trip.transport_preference,
        "note": (
            "Actual hotel, transport, food and activity "
            "prices must be verified separately."
        )
    }