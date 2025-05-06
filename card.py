@app.route('/create-card', methods=['POST'])
def create_card():
    try:
        # Parse input
        data = request.get_json()
        cookie_value = data.get('cookie')
        body = data.get('body')
        access_token = data.get('access_token')
        refer = data.get('refer')

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
        
        # Check for JSON response
        if domo_response.headers.get('Content-Type', '').startswith('application/json'):
            domo_response_json = domo_response.json()
        else:
            domo_response_json = domo_response.text  # For non-JSON responses
        
        # Return response
        return jsonify({
            "status": domo_response.status_code,
            "response": domo_response_json
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
