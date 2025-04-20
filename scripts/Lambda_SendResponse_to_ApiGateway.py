import json
import boto3
import os

s3 = boto3.client('s3')
BUCKET_NAME = "<NOMBRE-BUCKET>"

def lambda_handler(event, context):
    # Validación del parámetro de entrada
    file_param = event.get("queryStringParameters", {}).get("file")
    
    if not file_param:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Parámetro 'file' es requerido"})
        }
    
    try:
        # Extraer user_id (asumimos que es la primera parte antes del primer '_')
        user_id = file_param.split("_")[0]
        object_key = f"uploads/{user_id}/logs/{file_param}.json"

        # Leer el objeto JSON desde S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key=object_key)
        file_content = response['Body'].read().decode('utf-8')
        json_data = json.loads(file_content)

        return {
            "statusCode": 200,
            "body": json.dumps(json_data),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except s3.exceptions.NoSuchKey:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": f"Archivo '{file_param}' no encontrado."})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Error interno", "detalle": str(e)})
        }

