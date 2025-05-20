from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GAS_ENDPOINTS = {
    "emotion-log": "https://script.google.com/macros/s/xxxxx/exec",
    "dialogue-log": "https://script.google.com/macros/s/yyyyy/exec",
    "task-log": "https://script.google.com/macros/s/zzzzz/exec",
    "get-task-log": "https://script.google.com/macros/s/zzzzz/exec"
}

@app.route("/<log_type>", methods=["POST", "GET"])
def relay_log(log_type):
    if log_type not in GAS_ENDPOINTS:
        return jsonify({"error": f"Unknown log type: {log_type}"}), 404

    try:
        gas_url = GAS_ENDPOINTS[log_type]

        if request.method == "POST":
            data = request.json
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
