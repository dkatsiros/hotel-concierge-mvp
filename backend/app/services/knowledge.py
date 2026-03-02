import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


class KnowledgeService:
    def __init__(self):
        self._cache: dict[str, str] = {}

    def _load_json(self, filename: str) -> dict:
        path = DATA_DIR / filename
        if path.exists():
            return json.loads(path.read_text())
        return {}

    def _load_text(self, filename: str) -> str:
        path = DATA_DIR / filename
        if path.exists():
            return path.read_text()
        return ""

    def get_system_context(self) -> str:
        if "system_context" in self._cache:
            return self._cache["system_context"]

        hotel = self._load_json("hotel_info.json")
        restaurants = self._load_json("restaurants.json")
        services = self._load_json("services.json")
        faq = self._load_text("faq.txt")
        attractions = self._load_text("local_attractions.txt")

        parts = [
            "You are a friendly and helpful hotel concierge AI assistant.",
            "Answer guest questions using the hotel information below.",
            "Be concise, warm, and professional.",
            "",
            f"## Hotel Info\n{json.dumps(hotel, indent=2)}",
            f"## Restaurants\n{json.dumps(restaurants, indent=2)}",
            f"## Services\n{json.dumps(services, indent=2)}",
            f"## FAQ\n{faq}",
            f"## Local Attractions\n{attractions}",
        ]

        ctx = "\n\n".join(parts)
        self._cache["system_context"] = ctx
        return ctx
