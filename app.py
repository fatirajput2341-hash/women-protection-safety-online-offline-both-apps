from flask import Flask, request, jsonify, render_template_string
import datetime

app = Flask(__name__)

# Temporary database list jo incoming alerts ko save karegi
alerts_database = []

# 1. HOME PAGE (Chrome/Firefox par dekhne ke liye Dashboard)
@app.route('/', methods=['GET'])
def dashboard():
    # Ek aasan aur khoobsurat HTML interface jo browser par dikhega
    html_layout = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Women Safety Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; }
            h2 { color: #d9534f; border-bottom: 2px solid #d9534f; padding-bottom: 10px; }
            .alert-box { background: white; padding: 15px; margin-bottom: 10px; border-left: 5px solid #d9534f; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .badge { background: #d9534f; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px; font-weight: bold; }
            .no-alerts { color: #666; font-style: italic; }
        </style>
    </head>
    <body>
        <h2>🚨 Women Protection & Safety System - Live Admin Control Panel</h2>
        <p>Status: <span style="color: green; font-weight: bold;">🟢 Server Active & Monitoring Online/Offline Data</span></p>
        
        <h3>Recent Emergency SOS Signals:</h3>
        {% if not alerts %}
            <p class="no-alerts">No emergency alerts received yet. System is safe.</p>
        {% else %}
            {% for alert in alerts %}
                <div class="alert-box">
                    <p><span class="badge">SOS EMERGENCY</span> <strong>User:</strong> {{ alert.user }} | <strong>Time:</strong> {{ alert.time }}</p>
                    <p><strong>📍 Coordinates:</strong> Latitude: {{ alert.lat }}, Longitude: {{ alert.lng }}</p>
                    <p><strong>🌐 Mode Detected:</strong> {{ alert.mode }}</p>
                </div>
            {% endfor %}
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html_layout, alerts=alerts_database)

# 2. API ENDPOINT (Jahan app.py ya test_client.py se data aayega)
@app.route('/api/alert', methods=['POST'])
def receive_alert():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid Data"}), 400
        
        # Incoming variables extract karna
        user_name = data.get('user_id', 'Unknown User')
        latitude = data.get('latitude', '0.0')
        longitude = data.get('longitude', '0.0')
        mode = data.get('mode', 'Online Mode') # Dono apps handle karne ke liye
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # New alert dictionary banana
        new_alert = {
            "user": user_name,
            "lat": latitude,
            "lng": longitude,
            "mode": mode,
            "time": current_time
        }
        
        # Database (list) mein save karna taake dashboard par dikhe
        alerts_database.insert(0, new_alert)
        
        # Anaconda Terminal par alert print karna
        print(f"\n🚨 [ALERT RECEIVED] User: {user_name} | Lat: {latitude} | Lng: {longitude} via {mode}")
        
        return jsonify({
            "status": "success", 
            "message": "Emergency response triggered! Location coordinates broadcasted successfully."
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # '0.0.0.0' lagane se browser aur local system dono par chalega
    app.run(host='0.0.0.0', port=5000, debug=True)
