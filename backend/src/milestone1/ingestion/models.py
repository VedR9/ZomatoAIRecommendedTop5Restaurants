from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Restaurant:
    id: str
    name: str
    location: str
    cuisines: list[str]
    cost_for_two: float | None
    rating: float | None
