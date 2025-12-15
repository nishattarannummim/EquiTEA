from flask import Flask, request, jsonify
from blockchain import process_wage
from threading import Thread

app = Flask(__name__)
processed = set()

@app.route("/", methods=["GET"])
def home():
    return "Server is online", 200

def send_blockchain_tx(worker_id, weight_in_kg):
    try:
        receipt = process_wage(worker_id, weight_in_kg, tx_amount=0.00001)
        print(f"Blockchain tx completed: {receipt.transactionHash.hex()}")
    except Exception as e:
        print(f"Blockchain error: {e}")

@app.route("/recognize", methods=["POST"])
def recognize():
    data = request.get_json(force=True)

    if not data or "worker_id" not in data or "weight" not in data:
        return jsonify({"status": "error", "message": "Missing worker_id or weight"}), 400

    worker_id = str(data["worker_id"])
    try:
        weight_in_kg = int(float(data["weight"]))
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid weight"}), 400

    key = f"{worker_id}:{weight_in_kg}"
    if key in processed:
        return jsonify({"status": "skipped", "message": "Already processed"}), 200

    processed.add(key)

    Thread(target=send_blockchain_tx, args=(worker_id, weight_in_kg)).start()

    return jsonify({
        "status": "received",
        "worker_id": worker_id,
        "weight_kg": weight_in_kg,
        "message": "Transaction is being processed"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
