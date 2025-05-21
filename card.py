from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import tempfile
import json
import base64, os, zipfile, uuid, shutil
from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, TableDefinition, SqlType, TableName, Date, Name
from tableauhyperapi import HyperException
import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

@app.route('/create-card', methods=['POST'])
def create_card():
    try:
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
            "accept-language":"en",
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

# @app.post("/extract-data")
# def extract_data():
#     try:
#         data = request.get_json()
#         filesDatas = data.get('filesData')

#         if not filesDatas:
#             return jsonify(status_code=400, content={"error": "No filesData found in the request"})

#         all_results  = []

#         for filesData in filesDatas:
#             filename = filesData.get('filename')
#             base64_string = filesData.get('content')

#             if not filename or not base64_string:
#                 return jsonify(status_code=400, content={"error": "Missing 'filename' or 'content' in filesData"})

#             try:
#                 # Decode base64 to binary content
#                 file_content = base64.b64decode(base64_string)

#                 # Create a temp directory for extraction
#                 with tempfile.TemporaryDirectory() as temp_dir:
#                     # Save decoded file to temp file
#                     tdsx_path = os.path.join(temp_dir, filename)
#                     with open(tdsx_path, "wb") as f:
#                         f.write(file_content)

#                     # Extract .hyper file from the TDSX
#                     hyper_path = extract_hyper_from_tdsx(tdsx_path, temp_dir)

#                     if not hyper_path or not os.path.exists(hyper_path):
#                         all_results .append({
#                             "name": filename,
#                             "note": "No .hyper file found inside provided .tdsx"
#                         })
#                         continue

#                     # Read .hyper file
#                     hyper_data = read_hyper_data(hyper_path)

#                     all_results  .append({
#                         "name": filename,
#                         "preview": hyper_data
#                     })

#                     if os.path.exists(tdsx_path):
#                         os.remove(tdsx_path)

#             except Exception as e:
#                 all_results .append({
#                     "name": filename,
#                     "error": str(e)
#                 })

#         return jsonify(content={"status": "success", "results": all_results })

#     except Exception as e:
#         return jsonify(status_code=500, content={"status": "error", "message": str(e)})

def extract_hyper_from_tdsx(tdsx_path, extract_to_dir):
    with zipfile.ZipFile(tdsx_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith('.hyper'):
                zip_ref.extract(file_name, path=extract_to_dir)
                return os.path.join(extract_to_dir, file_name)
    return None

def serialize_value(value):
    if isinstance(value, (datetime.date, datetime.datetime, Date)):
        return str(value)
    elif isinstance(value, Name):  # column name objects
        return str(value)
    return value

def read_hyper_data(hyper_path):
    results = []
    try:
        with HyperProcess(telemetry=True) as hyper:
            with Connection(endpoint=hyper.endpoint, database=hyper_path) as connection:
                table_names = connection.catalog.get_table_names("Extract")
                for table in table_names:
                    table_data = []
                    with connection.execute_query(f"SELECT * FROM {table}") as result:
                        # Use result.schema.column_names to extract column names
                        # print(",,,,,",result.schema)
                        column_names = [str(col) for col in result.schema.columns]  # This will give the column names
                        for row in result:
                            serialized_row = [serialize_value(v) for v in row]
                            table_data.append(dict(zip(column_names, serialized_row)))
                    results.append({str(table): table_data})
    except Exception as e:
        raise ValueError(f"Error reading .hyper file: {str(e)}")
    return results

@app.post("/extract-data")
def extract_data():
    try:
        data = request.get_json()
        filesDatas = data.get('filesData')

        if not filesDatas:
            return jsonify({"error": "No filesData found in the request"}), 400

        all_results = []

        for filesData in filesDatas:
            filename = filesData.get('filename')
            base64_string = filesData.get('content')

            if not filename or not base64_string:
                return jsonify({"error": "Missing 'filename' or 'content' in filesData"}), 400

            try:
                file_content = base64.b64decode(base64_string)

                # Create a temp directory for extraction
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Save decoded file to temp file
                    tdsx_path = os.path.join(temp_dir, filename)
                    with open(tdsx_path, "wb") as f:
                        f.write(file_content)

                    # Extract .hyper file from the TDSX
                    hyper_path = extract_hyper_from_tdsx(tdsx_path, temp_dir)

                    if not hyper_path or not os.path.exists(hyper_path):
                        all_results.append({
                            "name": filename,
                            "note": "No .hyper file found inside provided .tdsx"
                        })
                        continue

                    # Read .hyper file
                    hyper_data = read_hyper_data(hyper_path)
                    # print(",,,,,",hyper_data)

                    all_results.append({
                        "name": filename,
                        "data": hyper_data
                    })

            except Exception as e:
                all_results.append({
                    "name": filename,
                    "error": str(e)
                })

        return jsonify({"status": "success", "results": all_results})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/extract-table', methods=['POST'])
def upload_hyper():
    try:
        # Check if file part present
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        # Accept both .tdsx and .twbx files
        if not (file.filename.endswith('.tdsx') or file.filename.endswith('.twbx')):
            return jsonify({"error": "Only .tdsx or .twbx files are supported"}), 400

        file_data = file.read()

        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = os.path.join(tmpdir, file.filename)
            with open(archive_path, 'wb') as f:
                f.write(file_data)

            # Extract archive
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            # Find all .hyper files inside extracted folder
            hyper_files = []
            for root, _, files in os.walk(tmpdir):
                for f in files:
                    if f.endswith('.hyper'):
                        hyper_files.append(os.path.join(root, f))

            if not hyper_files:
                return jsonify({"error": "No .hyper files found in the uploaded file"}), 404

            result = []

            # Open each hyper file and extract tables
            with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
                for hyper_path in hyper_files:
                    with Connection(endpoint=hyper.endpoint, database=hyper_path) as connection:
                        schema_names = connection.catalog.get_schema_names()
                        for schema in schema_names:
                            tables = connection.catalog.get_table_names(schema)
                            for table in tables:
                                # Clean schema and table names:
                                schema_name = str(schema.name).strip('"')
                                table_name_raw = str(table.name).strip('"')
                                # Extract prefix before first underscore in table name
                                table_name = table_name_raw.split('_')[0]
                                result.append({
                                    "schema": schema_name,
                                    "table": table_name
                                })

            return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
