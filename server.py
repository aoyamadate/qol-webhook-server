from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# GAS Webhook の送信先URL一覧（すべて最新）
GAS_ENDPOINTS = {
    "emotion-log": "https://script.google.com/macros/s/AKfycbzu9ABKFahbFIQsDWkTJR8ZE-czB4mrp9XEzxq9ahy8fIMoAw_-gARgx2cQd-XefrrfCA/exec",
    "dialogue-log": "https://script.google.com/macros/s/AKfycbz3ATERSJlJBzg8iYKJ2n3gCYIx5orU6F3Boh7yybK47loa2c2adyxT8xIKPaYlOpd0/exec",
    "task-log": "https://script.google.com/macros/s/AKfycbzqaYZcZz_GT9Hz1Uiv7t9T86Keg5K0WbGN6tTBOir5bZp8zckMKy-BtpyD_svQOkQymw/exec",
    "get-task-log": "https://script.google.com/macros/s/AKfycbzqaYZcZz_GT9Hz1Uiv7t9T86Keg5K0WbGN6tTBOir5bZp8zckMKy-BtpyD_svQOkQymw/exec",

    # ✅ 食事記録（記録・取得共通）
    "meal-log": "https://script.google.com/macros/s/AKfycbz3vEJhypmAonEAWpTwABu1Jh3XLF54ltL1ZII1IoPM3yGsoDQh4Q9prf0l1CWSdJ9v/exec",
    "meal-log-data": "https://script.google.com/macros/s/AKfycbz3vEJhypmAonEAWpTwABu1Jh3XLF54ltL1ZII1IoPM3yGsoDQh4Q9prf0l1CWSdJ9v/exec",

    # ✅ 睡眠記録（記録・取得共通）
    "sleep-log": "https://script.google.com/macros/s/AKfycbzI5woorPQImM0VT7K9LDHmpiVUiXKzkUURjTs3I2D7s-U4ZfJBx0oxNmOZHDCtPpyu/exec",
    "sleep-log-data": "https://script.google.com/macros/s/AKfycbzI5woorPQImM0VT7K9LDHmpiVUiXKzkUURjTs3I2D7s-U4ZfJBx0oxNmOZHDCtPpyu/exec"
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

@app.route("/task-review-input", methods=["POST"])
def handle_task_review():
    try:
        data = request.json
        print("📥 受信データ（朝の送信）:", data)

        # 仮のタスク配置レスポンス（今後GPT連携に置き換え）
        example_response = [
            {
                "title": "［自動］資料作成",
                "start": f"{data['date']}T10:00:00+09:00",
                "end": f"{data['date']}T11:00:00+09:00",
                "calendarId": "自動タスク配置"
            },
            {
                "title": "［自動］日報記録",
                "start": f"{data['date']}T14:00:00+09:00",
                "end": f"{data['date']}T14:15:00+09:00",
                "calendarId": "自動タスク配置"
            }
        ]

        # GASへ送信
        schedule_url = "https://script.google.com/macros/s/AKfycbzCY_WIGjj68oPeRXJhe7lvon7E_2AlggfzyK6rPRQavPLLC8ZfBCGvd9IIWZxixgcD/exec"
        response = requests.post(schedule_url, json=example_response)

        return jsonify({
            "status": "processed",
            "message": "GPT判断（仮）→ GASへ送信完了",
            "gas_response": response.text
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
