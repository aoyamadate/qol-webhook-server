from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# GAS Webhook の送信先URL一覧（すべて最新）
GAS_ENDPOINTS = {
    "emotion-log": "https://script.google.com/macros/s/AKfycbzu9ABKFahbFIQsDWkTJR8ZE-czB4mrp9XEzxq9ahy8fIMoAw_-gARgx2cQd-XefrrfCA/exec",
    "dialogue-log": "https://script.google.com/macros/s/AKfycbz3ATERSJlJBzg8iYKJ2n3gCYIx5orU6F3Boh7yybK47loa2c2adyxT8xIKPaYlOpd0/exec",
    "task-log": "https://script.google.com/macros/s/AKfycbzqaYZcZz_GT9Hz1Uiv7t9T86Keg5K0WbGN6tTBOir5bZp8zckMKy-BtpyD_svQOkQymw/exec",
    "get-task-log": "https://script.google.com/macros/s/AKfycbzqaYZcZz_GT9Hz1Uiv7t9T86Keg5K0WbGN6tTBOir5bZp8zckMKy-BtpyD_svQOkQymw/exec",

    # ✅ 統一された食事記録（記録・取得どちらも）
    "meal-log": "https://script.google.com/macros/s/AKfycbz3vEJhypmAonEAWpTwABu1Jh3XLF54ltL1ZII1IoPM3yGsoDQh4Q9prf0l1CWSdJ9v/exec",
    "meal-log-data": "https://script.google.com/macros/s/AKfycbz3vEJhypmAonEAWpTwABu1Jh3XLF54ltL1ZII1IoPM3yGsoDQh4Q9prf0l1CWSdJ9v/exec"
}

@app.route("/<log_type>", methods=["POST", "GET"])
def relay_log(log_type):
    if log_type not in GAS_ENDPOINTS:
        return jsonify({"error": f"Unknown log type: {log_type}"}), 404

    try:
        gas_url = GAS_ENDPOINTS[log_type]

        if request.method == "POST":
            data = request.json
            print("📤 POST送信:", data)
            response = requests.post(gas_url, json=data)
        else:  # GET
            params = request.args.to_dict()
            print("📥 GETパラメータ:", params)
            response = requests.get(gas_url, params=params)

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
