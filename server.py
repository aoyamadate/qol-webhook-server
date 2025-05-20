from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ログタイプごとのGAS Webhook URLをここで一元管理
GAS_ENDPOINTS = {
    "emotion-log": "https://script.google.com/macros/s/AKfycbzu9ABKFahbFIQsDWkTJR8ZE-czB4mrp9XEzxq9ahy8fIMoAw_-gARgx2cQd-XefrrfCA/exec",
    "dialogue-log": "https://script.google.com/macros/s/AKfycbxTi-TURT9me63Txvp4E8XerGXX7u1HorEpCbJn89F0oF599IJyb6VwFEDCuRGWXsSX/exec"
    # 今後追加予定: "task-log": "https://..." など
}

@app.route("/<log_type>", methods=["POST"])
def relay_log(log_type):
    if log_type not in GAS_ENDPOINTS:
        return jsonify({"error": f"Unknown log type: {log_type}"}), 404

    try:
        data = request.json
        gas_url = GAS_ENDPOINTS[log_type]
        response = requests.post(gas_url, json=data)
        return jsonify({
            "status": "relayed",
            "log_type": log_type,
            "gas_response": response.text
        }), response.status_code
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
