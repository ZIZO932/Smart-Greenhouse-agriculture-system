import paho.mqtt.client as mqtt
import mysql.connector
import json
from flask import Flask, render_template, jsonify, request
from threading import Thread
app = Flask(__name__)
db_config = {"host": "localhost", "user": "root", "password": "", "database": "vervex_database"}
def get_db(): return mysql.connector.connect(**db_config)
broker = "192.168.0.169"
topic_data = "esp32/01/data"
mqtt_shared_client = None
last_received_data = {}
def on_message(client, userdata, msg):
    global last_received_data
    try:
        data = json.loads(msg.payload.decode())
        last_received_data = data
        conn = get_db()
        cursor = conn.cursor()
        query = "INSERT INTO sensor_data (device_id, temperature, light, moisture, npk_n, npk_p, npk_k, rssi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (data.get('device_id', 'SN_01'), data.get('temp', 0), data.get('light', 0), data.get('moisture', 0), data.get('npk_n', 0), data.get('npk_p', 0), data.get('npk_k', 0), data.get('rssi', 0)))
        conn.commit()
        cursor.close()
        conn.close()
    except: pass
def start_mqtt():
    global mqtt_shared_client
    client = mqtt.Client()
    client.on_message = on_message
    try:
        client.connect(broker, 1883)
        client.subscribe(topic_data)
        mqtt_shared_client = client
        client.loop_forever()
    except: pass
@app.route('/')
def index(): return render_template('index.html')
@app.route('/api/get_data')
def get_data():
    r = request.args.get('range', 'latest')
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if r == 'latest': cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1")
    elif r == 'today': cursor.execute("SELECT * FROM sensor_data WHERE created_at >= CURDATE() ORDER BY id ASC")
    elif r == 'week': cursor.execute("SELECT * FROM sensor_data WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) ORDER BY id ASC")
    elif r == 'month': cursor.execute("SELECT * FROM sensor_data WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) ORDER BY id ASC")
    else: cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 100")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)
@app.route('/api/actuator_states')
def actuator_states(): return jsonify(last_received_data)
@app.route('/api/notify_plant', methods=['POST'])
def notify_plant():
    p = request.json.get('plant')
    if mqtt_shared_client: mqtt_shared_client.publish("esp32/01/plant", p)
    return jsonify({"ok": True})
if __name__ == '__main__':
    Thread(target=start_mqtt, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
