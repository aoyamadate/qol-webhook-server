from flask import Flask, request
import requests

app = Flask(__name__)

# あなたのGAS Webhookエンドポイント
GAS_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbz3ATERSJlJBzg8iYKJ2n3gCYIx5orU6F3Boh7yybK47loa2c2adyxT8xIKPaYlOpd0/exec"

@app.route("/", methods=["POST"])
def relay():
    data = request.json
    res = requests.post(GAS_WEBHOOK_URL, json=data)
    return {"status": "relayed", "gas_response": res.text}, 200
