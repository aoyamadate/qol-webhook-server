from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# GAS Webhook の送信先URL（task-logのみ修正済み）
GAS_ENDPOINTS = {
    "emotion-log": "https://script.google.com/macros/s/AKfycbzu9ABKFahbFIQsDWkTJR8ZE-czB4mrp9XEzxq9ahy8fIMoAw_-gARgx2cQd-XefrrfCA/exec",
    "dialogue-log": "https://script.google.com/macros/s/AKfycbz3ATERSJlJBzg8iYKJ2n3gCYIx5orU6F3Boh7yybK47loa2c2adyxT8xIKPaYlOpd0/exec",
    
    # ✅ 修正ポイント：タスクログはこの新しいURLを使う
    "task-log": "https://script.google.com/macros/s/AKfycbzqaYZcZz_GT9Hz1Uiv7t9T86Keg5K0WbGN6tTBOir5bZp8zckMKy-BtpyD_svQOkQymw/exec",
    "get-task-log": "https://script.google.com/macros/s/AKfycbzqaYZcZz_GT9Hz1Uiv7t9T86Keg5K0WbGN6tTBOir5bZp8zckMKy-BtpyD_svQOkQymw/exec",
}

@app.route("/<log_type>", methods=["POST", "GET"])
def relay_log(log_type):
    if log_type not in GAS_ENDPOINTS:
        return jsonify({"error": f"Unknown log type: {log_type}"}), 404

    try:
        gas_url = GAS_ENDPOINTS[log_type]

        if request.method == "POST":
            data = request.json
            print("📤 送信内容:", data)  # ログ出力（確認用）
            response = requests.post(gas_url, json=data)
        else:  # GET
            response = requests.get(gas_url)

        return jsonify({
            "status": "relayed",
            "method": request.method,
            "log_type": log_type,
            "gas_response": response.text
        }), response.status_code

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
