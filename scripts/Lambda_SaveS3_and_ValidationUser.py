import json
import boto3
import os
import uuid
from datetime import datetime, timedelta

s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')

BUCKET_NAME = "<NOMBRE-BUCKET>"

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            s3_info = record['s3']
            bucket = s3_info['bucket']['name']
            object_key = s3_info['object']['key']  # uploads/USER_ID/1037671417_030425_211356_input.png

            parts = object_key.split('/')
            if len(parts) < 3:
                return {"statusCode": 400, "body": "Formato incorrecto de key en S3"}

            user_id = parts[1]
            uploaded_image_key = object_key
            reference_image_key = f"users/{user_id}/reference.png"

            print(f"Comparando: {uploaded_image_key} vs {reference_image_key}")

            # === EXTRAER INFO DEL NOMBRE DEL ARCHIVO ===
            filename = os.path.basename(uploaded_image_key).replace('.png', '')  # ej. 1037671417_030425_211356_input
            filename_parts = filename.split('_')

            if len(filename_parts) < 4:
                return {"statusCode": 400, "body": "Nombre del archivo no cumple con el formato esperado."}

            file_user_id = filename_parts[0]
            fecha_raw = filename_parts[1]  # 030425
            hora_raw = filename_parts[2]   # 211356
            movimiento = filename_parts[3] # input

            fecha = f"{fecha_raw[:2]}/{fecha_raw[2:4]}/{fecha_raw[4:]}"
            hora = f"{hora_raw[:2]}:{hora_raw[2:4]}:{hora_raw[4:]}"


            # === LLAMADA A REKOGNITION ===
            response = rekognition_client.compare_faces(
                SourceImage={'S3Object': {'Bucket': BUCKET_NAME, 'Name': reference_image_key}},
                TargetImage={'S3Object': {'Bucket': BUCKET_NAME, 'Name': uploaded_image_key}},
                SimilarityThreshold=70
            )

            if 'FaceMatches' in response and response['FaceMatches']:
                similarity = response['FaceMatches'][0]['Similarity']
                message = f"✅ Usuario reconocido con {similarity:.2f}% de similitud."
                match_status = "MATCH"
            else:
                message = "❌ Usuario no reconocido o no coincide."
                match_status = "NO MATCH"

            print(message)

            # === GENERAR UUID ===
            user_uuid = str(uuid.uuid4())

            # === CONSTRUIR JSON CON LOS NUEVOS CAMPOS ===
            result_data = {
                "uuid": user_uuid,
                "user_id": file_user_id,
                "fecha": fecha,
                "hora": hora,
                "movimiento": movimiento,
                "resultado": match_status,
                "mensaje": message,
                "timestamp": (datetime.utcnow() - timedelta(hours=5)).isoformat() + "Z"
            }

            log_filename = filename.replace('.png', '') + '.json'
            log_path = f"uploads/{user_id}/logs/{log_filename}"

            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=log_path,
                Body=json.dumps(result_data),
                ContentType='application/json'
            )

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": message,
                    "log_path": log_path,
                    "resultado": match_status
                })
            }

    except Exception as e:
        print(f"Error en la Lambda: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Error interno", "detalle": str(e)})
        }
