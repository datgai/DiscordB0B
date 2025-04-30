import os
import requests
from flask import Flask, jsonify, request
from mangum import Mangum
from asgiref.wsgi import WsgiToAsgi
from discord_interactions import verify_key_decorator
import dotenv

dotenv.load_dotenv()
DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app, lifespan="off")


@app.route("/", methods=["POST"])
async def interactions():
    print(f"👉 Request: {request.json}")
    raw_request = request.json
    return interact(raw_request)


@verify_key_decorator(DISCORD_PUBLIC_KEY)
def interact(raw_request):
    message_content = "No valid command or response available."  # Default value
    if raw_request["type"] == 1:  # PING
        response_data = {"type": 1}  # PONG
    else:
        data = raw_request["data"]
        command_name = data["name"]

        if command_name == "chat":
            original_message = data["options"][0]["value"]
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{
                    "parts": [{"text": f"Using a 'Robot' persona, answer the following the following prompt within 50 words unless mentioned otherwise: \n + {original_message}"}]
                }]
            }
            
            gemini_response = requests.post(gemini_url, headers=headers, json=payload)
            if gemini_response.status_code == 200:
                gemini_data = gemini_response.json()
                message_content = gemini_data.get("contents", [{}])[0].get("parts", [{}])[0].get("text", gemini_response.text)
            else:
                message_content = (f"Error fetching response from Gemini API: {gemini_response.status_code} - {gemini_response.text}")

        response_data = {
            "type": 4,
            "data": {"content": message_content},
        }

    response = jsonify(response_data)
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run(debug=True)
