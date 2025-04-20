import json
import boto3
import urllib.parse
import os
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Extraer info del evento
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

        print(f"Nuevo archivo subido: {key}")

        # Extraer user_id del key
        parts = key.split('/')
        user_id = parts[0]
        filename = parts[-1]

        if not filename.endswith('.json') or 'logs/' not in key:
            print("Archivo no válido. Se ignora.")
            return

        # Obtener el contenido del JSON desde S3
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)

        # Timestamp por nombre de archivo o current timestamp
        timestamp = datetime.utcnow().isoformat()

        # Insertar en DynamoDB
        item = {
        'uuid': data['uuid'],
        'user_id': data['user_id'],
        'fecha': data['fecha'],
        'hora': data['hora'],
        'movimiento': data['movimiento'],
        'resultado': data['resultado'],
        'mensaje': data['mensaje'],
        'timestamp': data['timestamp']
        }


        table.put_item(Item=item)
        print("Item guardado exitosamente")

        return {
            'statusCode': 200,
            'body': 'JSON insertado en DynamoDB'
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }

