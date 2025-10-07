from flask import Flask, request,jsonify, render_template
from flask_cors import CORS
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")  

uri = MONGO_URL


client = MongoClient(
    os.getenv("MONGO_URL"),
    server_api=ServerApi("1"),
    tls=True,
    tlsAllowInvalidCertificates=True  # bypass TLS validation (not secure, testing only)
)

db = client["testDb"]
collection = db["flask-trial"]

try:
    client.admin.command("ping")
    print("✅ Connected to MongoDB Atlas!")
except Exception as e:
    print("❌ Connection failed:", e)
app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route("/add-entry", methods=["POST"])
def add_entry():
    try:
        data = request.get_json()
        name = data.get("name")
        task = data.get("task")

        if not name or not task:
            return jsonify({"error": "Both name and task are required"}), 400

        result = collection.insert_one({"name": name, "task": task})

        return jsonify({
            "message": "Entry added successfully",
            "id": str(result.inserted_id)  # <-- convert ObjectId to string
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':

    app.run(host='0.0.0.0',port=5000,debug=True)