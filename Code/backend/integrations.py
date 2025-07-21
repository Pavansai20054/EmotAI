# Simple webhooks for integration; expand as needed
from flask import Blueprint, request, jsonify

integrations_bp = Blueprint("integrations", __name__)

@integrations_bp.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    # Example: log integration event
    # You could add Slack, Teams, etc. logic here
    print(f"Received integration webhook: {data}")
    return jsonify({"status": "received"}), 200