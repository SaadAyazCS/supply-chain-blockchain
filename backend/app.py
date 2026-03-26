from flask import Flask, jsonify, request
from datetime import datetime
import hashlib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

products = {}

# =========================
# HASH FUNCTION
# =========================
def calculate_hash(product_id, product_name, location, time, previous_hash):
    raw = f"{product_id}{product_name}{location}{time}{previous_hash}"
    return hashlib.sha256(raw.encode()).hexdigest()

@app.route("/")
def home():
    return jsonify({"message": "Backend Running"})

# =========================
# ADD PRODUCT (GENESIS BLOCK)
# =========================
@app.route("/add-product", methods=["POST"])
def add_product():
    data = request.json

    product_id = data.get("product_id", "").strip()
    product_name = data.get("product_name", "").strip()
    location = data.get("location", "").strip()

    if not product_id or not product_name or not location:
        return jsonify({"error": "All fields are required"}), 400

    if product_id in products:
        return jsonify({"error": "Product already exists"}), 400

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    genesis_hash = calculate_hash(
        product_id,
        product_name,
        location,
        time,
        "0"
    )

    products[product_id] = {
        "product_name": product_name,
        "history": [
            {
                "location": location,
                "time": time,
                "previous_hash": "0",
                "hash": genesis_hash
            }
        ]
    }

    return jsonify({"status": "Product added successfully"})

# =========================
# UPDATE LOCATION (NEW BLOCK)
# =========================
@app.route("/update-location", methods=["POST"])
def update_location():
    data = request.json

    product_id = data.get("product_id", "").strip()
    location = data.get("location", "").strip()

    if not product_id or not location:
        return jsonify({"error": "Invalid input"}), 400

    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404

    last_block = products[product_id]["history"][-1]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_hash = calculate_hash(
        product_id,
        products[product_id]["product_name"],
        location,
        time,
        last_block["hash"]
    )

    products[product_id]["history"].append({
        "location": location,
        "time": time,
        "previous_hash": last_block["hash"],
        "hash": new_hash
    })

    return jsonify({"status": "Location updated successfully"})

# =========================
# TRACK PRODUCT
# =========================
@app.route("/track/<product_id>")
def track_product(product_id):
    product_id = product_id.strip()

    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(products[product_id])

# =========================
# BLOCKCHAIN VERIFICATION
# =========================
@app.route("/verify/<product_id>")
def verify_blockchain(product_id):
    product_id = product_id.strip()

    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404

    chain = products[product_id]["history"]
    product_name = products[product_id]["product_name"]

    for i in range(len(chain)):
        block = chain[i]

        prev_hash = "0" if i == 0 else chain[i - 1]["hash"]

        recalculated_hash = calculate_hash(
            product_id,
            product_name,
            block["location"],
            block["time"],
            prev_hash
        )

        if block["hash"] != recalculated_hash:
            return jsonify({
                "status": "❌ TAMPERED",
                "block": i + 1
            })

        if block["previous_hash"] != prev_hash:
            return jsonify({
                "status": "❌ TAMPERED (Broken Chain)",
                "block": i + 1
            })

    return jsonify({
        "status": "✅ VERIFIED",
        "blocks": len(chain)
    })

if __name__ == "__main__":
    app.run(debug=True)
