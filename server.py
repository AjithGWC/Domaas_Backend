import os
import zipfile
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tableauserverclient as TSC
from tableauhyperapi import HyperProcess, Connection, Telemetry, TableName

# === CONFIGURATION ===
TOKEN_NAME = 'test'
SITE_ID = ''  # use '' for default site
TABLEAU_URL = 'https://prod-apnortheast-a.online.tableau.com'
DOWNLOAD_DIR = 'downloads'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 Allow all origins. Replace with specific origins for security.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === TABLEAU AUTH SETUP ===
tableau_auth = TSC.PersonalAccessTokenAuth(
    token_name=TOKEN_NAME,
    # personal_access_token=TOKEN_VALUE,
    site_id=SITE_ID
)
server = TSC.Server(TABLEAU_URL, use_server_version=True)

# def read_hyper_data(hyper_path):
    #     data = {}
    #     try:
    #         with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    #             with Connection(endpoint=hyper.endpoint, database=hyper_path) as connection:
    #                 schema = "Extract"
    #                 tables = connection.catalog.get_table_names(schema=schema)
    #                 print("tables-------", tables)

    #                 for table in tables:
    #                     table_name = TableName(schema, table.name)
    #                     query = f'SELECT * FROM {table_name}'
    #                     rows = []
    #                     with connection.execute_query(query) as result:
    #                         for row in result:
    #                             cleaned_row = [
    #                                 str(cell) if not isinstance(cell, (str, int, float, bool, type(None))) else cell
    #                                 for cell in row
    #                             ]
    #                             rows.append(cleaned_row)

    #                     data[str(table.name)] = rows
    #     except Exception as e:
    #         data["error"] = str(e)
    #     return data

def read_hyper_data(hyper_path):
    data = {}
    try:
        with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(endpoint=hyper.endpoint, database=hyper_path) as connection:
                schema = "Extract"
                tables = connection.catalog.get_table_names(schema=schema)
                # print("tables-------", tables)

                for table in tables:
                    table_name = TableName(schema, table.name)
                    query = f'SELECT * FROM {table_name}'

                    with connection.execute_query(query) as result:
                        columns = [str(col.name) for col in result.schema.columns]
                        rows = []
                        for row in result:
                            cleaned_row = [
                                str(cell) if not isinstance(cell, (str, int, float, bool, type(None))) else cell
                                for cell in row
                            ]
                            rows.append(cleaned_row)

                    data[str(table.name)] = {
                        "columns": columns,
                        "rows": rows
                    }

    except Exception as e:
        data["error"] = str(e)
    return data

def extract_hyper_from_tdsx(tdsx_path, extract_dir):
    os.makedirs(extract_dir, exist_ok=True)
    try:
        with zipfile.ZipFile(tdsx_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # Search for .hyper file
        for root, _, files in os.walk(extract_dir):
            for file in files:
                if file.endswith('.hyper'):
                    return os.path.join(root, file)

        return None  # No hyper found

    except Exception as e:
        raise RuntimeError(f"Failed to extract .tdsx: {e}")

# === API ENDPOINT ===
@app.get("/download-datasources")
def download_all_datasources():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    summary = []

    try:
        with server.auth.sign_in(tableau_auth):
            all_datasources, _ = server.datasources.get()
            # print("all_datasources//////////////", all_datasources)

            for ds in all_datasources:
                tdsx_path = os.path.join(DOWNLOAD_DIR, f"{ds.name.replace(' ', '_')}.tdsx")

                try:
                    filepath = server.datasources.download(
                        ds.id,
                        filepath=tdsx_path,
                        include_extract=True
                    )

                    if not filepath.endswith('.tdsx') or not os.path.exists(filepath):
                        summary.append({
                            "name": ds.name,
                            "id": ds.id,
                            "note": "Failed to download .tdsx file"
                        })
                        continue

                    extract_dir = os.path.join(DOWNLOAD_DIR, ds.name.replace(' ', '_'))
                    hyper_file_path = extract_hyper_from_tdsx(filepath, extract_dir)

                    if not hyper_file_path or not os.path.exists(hyper_file_path):
                        summary.append({
                            "name": ds.name,
                            "id": ds.id,
                            "note": "No .hyper file found inside .tdsx"
                        })
                        continue

                    hyper_data = read_hyper_data(hyper_file_path)

                    summary.append({
                        "name": ds.name,
                        "id": ds.id,
                        "path": hyper_file_path,
                        "preview": hyper_data
                    })

                except Exception as e:
                    summary.append({
                        "name": ds.name,
                        "id": ds.id,
                        "error": str(e)
                    })

        return JSONResponse(content={"status": "success", "datasources": summary})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

