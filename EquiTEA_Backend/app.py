from flask import Flask, request, jsonify
import face_recognition
import numpy as np
import os

from blockchain import process_wage

app = Flask(__name__)

# ----------------------------
# Load known faces
# ----------------------------
known_face_encodings = []
known_face_ids = []

face_dir = "known_faces"
for worker_id in os.listdir(face_dir):
    worker_folder = os.path.join(face_dir, worker_id)
    if os.path.isdir(worker_folder):
        for filename in os.listdir(worker_folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(worker_folder, filename)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if len(encodings) > 0:
                    known_face_encodings.append(encodings[0])
                    known_face_ids.append(worker_id)

# ----------------------------
# Face recognition + blockchain wage
# ----------------------------
@app.route("/recognize", methods=["POST"])
def recognize():
    file = request.files.get("image")
    if not file:
        return jsonify({"status": "error", "message": "No image uploaded"}), 400

    unknown_image = face_recognition.load_image_file(file)
    encodings = face_recognition.face_encodings(unknown_image)

    if len(encodings) == 0:
        return jsonify({"status": "error", "message": "No face detected"}), 400

    unknown_encoding = encodings[0]
    results = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
    face_distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
    best_match_index = np.argmin(face_distances)

    if results[best_match_index]:
        worker_id = known_face_ids[best_match_index]

        # ----------------------------
        # Static weight for now
        # ----------------------------
        weight_in_kg = 5  

        # ----------------------------
        # Process wage on blockchain and return receipt
        # ----------------------------
        try:
            tx_receipt = process_wage(worker_id, weight_in_kg)
            return jsonify({
                "status": "success",
                "worker_id": worker_id,
                "weight_kg": weight_in_kg,
                "tx_hash": tx_receipt.transactionHash.hex(),
                "blockNumber": tx_receipt.blockNumber,
                "gasUsed": tx_receipt.gasUsed
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "Unknown face"}), 404

# ----------------------------
# Direct wage processing endpoint (for testing)
# ----------------------------
@app.route("/process_wage_direct", methods=["POST"])
def process_wage_direct():
    data = request.get_json()
    worker_id = data.get("worker_id")
    weight = data.get("weight")

    if not worker_id or weight is None:
        return jsonify({"status": "error", "message": "worker_id or weight missing"}), 400

    try:
        tx_receipt = process_wage(worker_id, weight)
        return jsonify({
            "status": "success",
            "worker_id": worker_id,
            "weight_kg": weight,
            "tx_hash": tx_receipt.transactionHash.hex(),
            "blockNumber": tx_receipt.blockNumber,
            "gasUsed": tx_receipt.gasUsed
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ----------------------------
# Run the Flask server
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)