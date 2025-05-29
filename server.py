from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# GAS Webhook の送信先URL一覧（最新版）
GAS_ENDPOINTS = {
    # ✅ 感情ログ（記録・取得）※どちらも同じ最新版URL
    "emotion-log": "https://script.google.com/macros/s/AKfycbyQCW6ESFhZ8c_lXi71ewgYqqOkBlOLFb8am943OY_TjwK5D6-s1SeTZABh2j2eU_NUJg/exec",
    "emotion-log-data": "https://script.google.com/macros/s/AKfycbyQCW6ESFhZ8c_lXi71ewgYqqOkBlOLFb8am943OY_TjwK5D6-s1SeTZABh2j2eU_NUJg/exec",

    # ✅ 対話ログ（記録・取得）
    "dialogue-log": "https://script.google.com/macros/s/AKfycbyMZ6wlOcN-5kU78OJ-7WM9Jqe1RSQykQEC_F7U_tgT7UyQ3nO5G95NLoYr5pOwVqF_/exec",
    "dialogue-log-data": "https://script.google.com/macros/s/AKfycbyMZ6wlOcN-5kU78OJ-7WM9Jqe1RSQykQEC_F7U_tgT7UyQ3nO5G95NLoYr5pOwVqF_/exec",

    # ✅ タスクログ（記録・取得）
    "task-log": "https://script.google.com/macros/s/AKfycbzqaYZcZz_GT9Hz1Uiv7t9T86Keg5K0WbGN6tTBOir5bZp8zckMKy-BtpyD_svQOkQymw/exec",
    "get-task-log": "https://script.google.com/macros/s/AKfycbzqaYZcZz_GT9Hz1Uiv7t9T86Keg5K0WbGN6tTBOir5bZp8zckMKy-BtpyD_svQOkQymw/exec",

    # ✅ 食事ログ（記録・取得）
    "meal-log": "https://script.google.com/macros/s/AKfycbz-4kpInqstJKSFvz7HX4oVS00oXK1KICezRPl4_HmMRqhjo_4JFH3M-eYTz7XrVc4/exec",
    "meal-log-data": "https://script.google.com/macros/s/AKfycbz-4kpInqstJKSFvz7HX4oVS00oXK1KICezRPl4_HmMRqhjo_4JFH3M-eYTz7XrVc4/exec",

    # ✅ 睡眠ログ（記録・取得）
    "sleep-log": "https://script.google.com/macros/s/AKfycbzI5woorPQImM0VT7K9LDHmpiVUiXKzkUURjTs3I2D7s-U4ZfJBx0oxNmOZHDCtPpyu/exec",
    "sleep-log-data": "https://script.google.com/macros/s/AKfycbzI5woorPQImM0VT7K9LDHmpiVUiXKzkUURjTs3I2D7s-U4ZfJBx0oxNmOZHDCtPpyu/exec",

    # ✅ 通学スケジュール登録（追加）
    "commute-schedule": "https://script.google.com/macros/s/AKfycbyYi7X8mFqwuBcnuaUR2-tj_yZi82yKrOIpLZGjif9tGME1SxoUwMbfwQeklRci2Ylt/exec",

    # ✅ カレンダー予定取得（追加）
    "calendar-events": "https://script.google.com/macros/s/AKfycbyRT7RLNz7jRC9kvCWDmFnOyyWVKETUv6mrzHt470EYBDDwXTx2qRiSLhbrD9x1U0mY/exec"
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
