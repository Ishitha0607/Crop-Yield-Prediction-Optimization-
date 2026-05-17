import os

# ✅ Completely disable python-dotenv auto loading
os.environ["FLASK_SKIP_DOTENV"] = "1"

import random
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ✅ GEMINI API
from google import genai

# ✅ Hardcoded Gemini API key (replace with your own)
GEMINI_API_KEY = "AIzaSyBXnqEuHERfQ6KEUEBFSdQL2EM7xxXEbyo"

# ✅ Initialize Gemini client
genai_client = genai.Client(api_key=GEMINI_API_KEY)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
MAIN_DIR = os.path.join(FRONTEND_DIR, "main")
PRODUCTS_DIR = os.path.join(FRONTEND_DIR, "productspage")
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="/")
CORS(app, resources={r"/api/*": {"origins": "*"}}, methods=["GET", "POST"])


# ✅ FARMING HELPERS
def soil_tip(soil: str) -> str:
    tips = {
        "loamy": "Rich soil; add compost every season and maintain drainage.",
        "clay": "Heavy soil; mix compost + coarse sand to improve aeration.",
        "sandy": "Drains fast; add mulch + organic matter to retain moisture.",
        "black": "Fertile soil; monitor pH and avoid overwatering."
    }
    return tips.get((soil or "").lower(), "Maintain soil pH 6.0–7.0 and add compost.")


def rain_tip(rainfall: float) -> str:
    if rainfall < 50:
        return "Low rainfall — use drip irrigation and mulch."
    if rainfall > 200:
        return "Heavy rainfall — increase drainage and prevent fungus."
    return "Moderate rainfall — maintain stable irrigation."


def predict_yield(crop: str, soil: str, area: float, rainfall: float):
    base = random.uniform(1.5, 3.5)
    predicted_yield = round(base * max(area, 0.01), 2)

    category = "High" if predicted_yield >= 8 else "Medium" if predicted_yield >= 4 else "Low"

    fertilizer = round(area * (60 if soil.lower() in ["loamy", "black"] else 50))
    water = round(area * (3 if rainfall < 80 else 2))

    tips = {
        "fertilizer": f"{fertilizer} kg NPK per season.",
        "water": f"{water} irrigations/week.",
        "soil_tips": soil_tip(soil),
        "weather_advice": rain_tip(rainfall)
    }

    return predicted_yield, category, tips


# ✅ HEALTH CHECK API
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "AgriTech-Gemini", "version": "2.0"})


# ✅ YIELD PREDICTION API
@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json(force=True) or {}

    try:
        crop = data.get("crop", "").strip()
        soil = data.get("soil", "").strip()
        area = float(data.get("area", 0))
        rainfall = float(data.get("rainfall", 0))
    except Exception:
        return jsonify({"success": False, "error": "Invalid input format."}), 400

    if area <= 0:
        return jsonify({"success": False, "error": "Area must be > 0."}), 400
    if rainfall < 0:
        return jsonify({"success": False, "error": "Rainfall cannot be negative."}), 400

    y, category, tips = predict_yield(crop, soil, area, rainfall)

    return jsonify({
        "success": True,
        "data": {
            "crop": crop,
            "soil": soil,
            "area": area,
            "rainfall": rainfall,
            "yield": y,
            "category": category,
            "suggestions": tips
        }
    })


# ✅ ✅ GEMINI CHAT SUPPORT API (MAIN FEATURE)
@app.route("/api/chat-support", methods=["POST"])
def chat_support():
    data = request.get_json(force=True) or {}
    msg = data.get("message", "").strip()
    lang = data.get("lang", "English").strip()

    if not msg:
        return jsonify({"success": False, "error": "Empty message"}), 400

    try:
        # ✅ Farming assistant personality (acts like system prompt)
        farming_assistant_prompt = (
            "I am a Farming Assistant AI. I provide expert advice ONLY about "
            "agriculture, crops, farming methods, soil, irrigation, fertilizer, "
            "pest control, weather effects on crops, and yield improvement. "
            "If the user asks anything unrelated to farming, I will politely refuse "
            "and guide them back to agriculture topics."
        )

        # ✅ Gemini requires ONLY: “user” and “model”
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                # ✅ Model role = system personality
                {"role": "model", "parts": [{"text": farming_assistant_prompt}]},

                # ✅ User message
                {"role": "user", "parts": [{"text": f"Language: {lang}\nUser: {msg}"}]}
            ]
        )

        reply = response.text.strip()
        return jsonify({"success": True, "reply": reply})

    except Exception as e:
        print("❌ Gemini Chat Error:", e)
        return jsonify({"success": False, "error": "Chat failed"}), 503


# ✅ FRONTEND ROUTES
@app.route("/")
def serve_index():
    return send_from_directory(MAIN_DIR, "index.html")


@app.route("/weather")
def serve_weather():
    return send_from_directory(MAIN_DIR, "weather.html")


@app.route("/products")
def serve_products():
    return send_from_directory(PRODUCTS_DIR, "product.html")


@app.route("/assets/<path:path>")
def serve_assets(path):
    return send_from_directory(ASSETS_DIR, path)


@app.route("/<path:path>")
def fallback(path):
    for root in (MAIN_DIR, PRODUCTS_DIR, FRONTEND_DIR):
        fp = os.path.join(root, path)
        if os.path.isfile(fp):
            return send_from_directory(root, path)
    return send_from_directory(MAIN_DIR, "index.html")


# ✅ START SERVER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n✅ AgriTech-Gemini running at http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=True)
