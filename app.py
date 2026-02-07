from flask import Flask, request, jsonify
from dotenv import load_dotenv
import boto3
import json
import os
import time

load_dotenv()
app = Flask(__name__)

AWS_REGION = os.getenv("AWS_REGION")
SQS_URL = os.getenv("SQS_URL")

sqs = boto3.client('sqs', region_name=AWS_REGION)
SQS_URL = SQS_URL

@app.route("/event", methods=["POST"])
def handle_event():
    print(f"Received event: {request.json}")

    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    event = {
        "sensor_name": data["sensor_name"],
        "event": data["event"],
        "timestamp": int(time.time())
    }

    sqs.send_message(QueueUrl=SQS_URL, MessageBody=json.dumps(event))
    print(f"Sent event: {event}")
    return jsonify({"message": "Event received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
