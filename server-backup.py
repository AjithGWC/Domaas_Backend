from flask import Flask, jsonify
from flask_cors import CORS
from tableauhyperapi import HyperProcess, Connection, Telemetry
import tableauserverclient as TSC
import os
import zipfile
import tempfile

app = Flask(__name__)
CORS(app)

# 🔐 Tableau Server Credentials
TABLEAU_USERNAME = "lkfdztyuhj123@gmail.com"
TABLEAU_PASSWORD = ".RM675bEg^eX4sH"
TABLEAU_SITE = ""  # Empty for default site
TABLEAU_SERVER_URL = "https://prod-apnortheast-a.online.tableau.com"

def download_first_hyper():
    tableau_auth = TSC.TableauAuth(TABLEAU_USERNAME, TABLEAU_PASSWORD, site_id=TABLEAU_SITE)
    server = TSC.Server(TABLEAU_SERVER_URL, use_server_version=True)

    with server.auth.sign_in(tableau_auth):
        datasources, _ = server.datasources.get()
        if not datasources:
            raise Exception("No datasources found on Tableau Server.")

        # Download first datasource
        print("...........",datasources[0])
        ds = datasources[0]

        file_path = os.path.abspath(f"{ds.name}")

        print("📥 Downloading TDSX to:", file_path)
        server.datasources.download(ds.id, filepath=file_path, include_extract=True)
        
        # if not os.path.exists(file_path):
        #     raise FileNotFoundError(f"Downloaded file not found: {file_path}")
        
        return file_path

def read_table_data_from_hyper(file_path):
    print(f" Trying to open hyper file at: {file_path}")
    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        print(" HyperProcess started", hyper.endpoint)
        with Connection(endpoint=hyper.endpoint, database=file_path) as connection:
            print(" Connection established to hyper file")
            tables = connection.catalog.get_table_names()
            print(tables)
            if not tables:
                raise Exception("No tables found in .hyper file.")

            table = tables[0]  # Get first table
            print("table...........", table)
            rows = connection.execute_list_query(f"SELECT * FROM {table}")
            return [list(row) for row in rows]

@app.route("/api/fetchData", methods=["GET"])
def fetch_data():
    try:
        hyper_file = download_first_hyper()
        print("hyper_file////////////", hyper_file)
        table_data = read_table_data_from_hyper(hyper_file)
        return jsonify(table_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "✅ Flask server is running. Hit /api/fetchData to get table data."

if __name__ == "__main__":
    app.run(debug=True, port=5000)










step - 2: 
=== HYPER READER ===
def read_hyper_data(hyper_path):
    data = {}
    try:
        with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(endpoint=hyper.endpoint, database=hyper_path) as connection:
                schema = "Extract"
                tables = connection.catalog.get_table_names(schema=schema)
                print("tables-------", tables)

                for table in tables:
                    table_name = TableName(schema, table.name)
                    query = f'SELECT * FROM {table_name}'
                    rows = connection.execute_list_query(query)

                    # Convert non-serializable values to strings
                    cleaned_rows = [
                        [str(cell) if not isinstance(cell, (str, int, float, bool, type(None))) else cell for cell in row]
                        for row in rows
                    ]

                    data[str(table.name)] = cleaned_rows
    except Exception as e:
        data["error"] = str(e)
    return data