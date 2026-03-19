import os
import io
import json
import time
import pandas as pd
import azure.functions as func
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="diet-dashboard", methods=["GET"])
def diet_dashboard(req: func.HttpRequest) -> func.HttpResponse:
    start_time = time.time()

    try:
        connection_string = os.getenv("BLOB_CONNECTION_STRING")
        if not connection_string:
            raise ValueError("BLOB_CONNECTION_STRING is not set")
        container_name = os.getenv("BLOB_CONTAINER_NAME", "datasets")
        blob_name = os.getenv("BLOB_FILE_NAME", "All_Diets.csv")

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        stream = blob_client.download_blob().readall()
        df = pd.read_csv(io.BytesIO(stream))

        rename_columns = {
            "Protein(g)": "Protein",
            "Carbs(g)": "Carbs",
            "Fat(g)": "Fat",
            "Cuisine_type": "Cuisine",
        }
        df = df.rename(columns=rename_columns)
        df = df.dropna(subset=["Protein", "Carbs", "Fat", "Diet_type"])

        avg_macros = (
            df.groupby("Diet_type")[["Protein", "Carbs", "Fat"]]
            .mean()
            .reset_index()
            .to_dict(orient="records")
        )

        top_protein = (
            df.sort_values(by="Protein", ascending=False)
            .head(10)[["Recipe_name", "Diet_type", "Cuisine", "Protein"]]
            .to_dict(orient="records")
        )

        cuisine_counts = (
            df["Cuisine"]
            .value_counts()
            .head(10)
            .reset_index()
        )
        cuisine_counts.columns = ["Cuisine", "Count"]
        cuisine_counts = cuisine_counts.to_dict(orient="records")

        execution_time_ms = round((time.time() - start_time) * 1000, 2)

        response_data = {
            "avg_macros": avg_macros,
            "top_protein": top_protein,
            "cuisine_counts": cuisine_counts,
            "execution_time_ms": execution_time_ms
        }

        return func.HttpResponse(
            json.dumps(response_data),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )