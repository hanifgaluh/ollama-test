import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma3:270m")
PORT = int(os.getenv("PORT", 5004))


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "API Chat Ollama aktif",
        "model": MODEL_NAME,
        "endpoints": {
            "health": "GET /health",
            "chat": "POST /chat"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "flask-api",
        "model": MODEL_NAME
    })


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Body JSON diperlukan."}), 400

    prompt = (data.get("prompt") or "").strip()

    if not prompt:
        return jsonify({"error": "Field 'prompt' tidak boleh kosong."}), 400

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()

        return jsonify({
            "success": True,
            "model": MODEL_NAME,
            "prompt": prompt,
            "response": result.get("response", "").strip()
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": f"Gagal menghubungi Ollama: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)