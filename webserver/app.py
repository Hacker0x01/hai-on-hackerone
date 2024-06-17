# pylint: disable=R1705
"""
This is the main file for the webserver. It contains the Flask app and the webhook endpoint.
"""

import os
import hmac
from flask import Flask, request

app = Flask(__name__)

def validate_request(data, signature):
    """
    Validate the request
    """
    [ _, digest ] = signature.split('=')
    generated_digest = hmac.new(
        os.environ.get("WEBHOOK_SECRET").encode(),
        str(data).encode(),
        "sha256"
    ).hexdigest()

    return hmac.compare_digest(digest, generated_digest)

@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Webhook endpoint
    """
    data = request.get_json()
    body = request.data.decode()
    if 'X-H1-signature' in request.headers:
        if validate_request(body, request.headers['X-H1-signature']):
            report_id = data.get('data', {}).get('report', {}).get('id')

            if report_id:
                with open('/hai-on-hackerone/webserver/data/report_ids.txt', 'a', encoding='UTF-8') as file:
                    file.write(f'{report_id}\n')

            return {"success": True}, 200
        else:
            return {"success": False, "error": "Incorrect signature"}, 401
    else:
        return {"success": False, "error": "Missing 'X-H1-Signature' header"}, 400
