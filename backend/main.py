import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn

app = FastAPI(title="Leftover Magic API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- API models ----
class SuggestReq(BaseModel):
    ingredients: List[str]

# ---- Fake data (so it's zero-cost to run) ----
RECIPES = [
    {
        "id": "rx_pesto_pasta",
        "title": "Pesto Pasta Salad",
        "why_it_works": "Uses your pasta + tomatoes; bright and quick.",
        "missing": ["lemon", "olive oil"],
        "serves": 2
    },
    {
        "id": "rx_garlic_prawns",
        "title": "Garlic Butter Prawns",
        "why_it_works": "Great with cherry tomatoes & linguine.",
        "missing": ["parsley", "butter"],
        "serves": 2
    },
    {
        "id": "rx_couscous",
        "title": "Roast Veg Couscous",
        "why_it_works": "Perfect if you have carrots & capsicum.",
        "missing": ["couscous"],
        "serves": 4
    }
]

RECIPE_DETAILS: Dict[str, Dict[str, Any]] = {
    "rx_pesto_pasta": {
        "title": "Pesto Pasta Salad",
        "ingredients": [
            "Cooked pasta (300 g)",
            "Cherry tomatoes (1 cup)",
            "Pesto (3 tbsp)",
            "Baby spinach (1 cup)",
            "Lemon (1/2)",
            "Olive oil (1 tbsp)"
        ],
        "steps": [
            "Toss warm pasta with pesto and olive oil.",
            "Fold in tomatoes and spinach.",
            "Finish with lemon juice and cracked pepper."
        ],
        "nutrition": {"kcal": 520, "protein_g": 15, "carbs_g": 70, "fat_g": 20}
    },
    "rx_garlic_prawns": {
        "title": "Garlic Butter Prawns",
        "ingredients": [
            "Prawns (300 g)",
            "Butter (2 tbsp)",
            "Garlic (3 cloves)",
            "Parsley (small bunch)",
            "Cooked pasta or bread, to serve"
        ],
        "steps": [
            "Sizzle garlic in butter 30 sec.",
            "Add prawns; cook until pink.",
            "Toss with parsley and serve over pasta."
        ],
        "nutrition": {"kcal": 430, "protein_g": 32, "carbs_g": 10, "fat_g": 28}
    },
    "rx_couscous": {
        "title": "Roast Veg Couscous",
        "ingredients": [
            "Couscous (1 cup)",
            "Carrot & capsicum (2 cups, chopped)",
            "Olive oil (1 tbsp)",
            "Lemon (1/2)",
            "Herbs (to taste)"
        ],
        "steps": [
            "Roast veg at 200°C until tender.",
            "Steam couscous; fluff with fork.",
            "Combine; finish with lemon and herbs."
        ],
        "nutrition": {"kcal": 480, "protein_g": 12, "carbs_g": 78, "fat_g": 14}
    }
}

@app.post("/api/suggest")
def suggest(req: SuggestReq):
    # For MVP we just return the seed list. You can swap to AI later.
    return {"recipes": RECIPES}

@app.get("/api/recipe/{rid}")
def recipe_detail(rid: str):
    return RECIPE_DETAILS.get(rid, {"error": "recipe not found"})

# Serve the static frontend
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend", "public")
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))