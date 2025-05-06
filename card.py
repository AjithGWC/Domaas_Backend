from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

@app.route('/create-card', methods=['POST'])
def create_card():
    try:
        print("1")
        # Parse input
        data = request.get_json()
        cookie_value = data.get('cookie')
        body = data.get('chartBody')
        access_token = data.get('access_token')
        refer = data.get('refer')
        print(".........",cookie_value)
        print(body)
        print(access_token)
        print(refer)

        if not cookie_value or not body:
            return jsonify({"error": "Both 'cookie' and 'body' fields are required"}), 400

        # Target endpoint
        url = "https://gwcteq-partner.domo.com/api/content/v3/cards/kpi?pageId=-100000"

        # Headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Origin": refer,
            "Referer": refer,
            "x-domo-requestcontext": '{"clientToe":"HI1KFS4VEI-6L56F"}',
            "Content-Type": "application/json",
            "Cookie": cookie_value
        }

        # Send request 
        domo_response = requests.put(url, headers=headers, data=json.dumps(body))
        print("....", domo_response.json())

        # Return response
        return jsonify({
            "status": domo_response.status_code,
            "response": domo_response.json() if domo_response.headers.get('Content-Type', '').startswith('application/json') else domo_response.text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
