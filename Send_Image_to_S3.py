import sys
import datetime
import hashlib
import hmac
import requests

# ========== CONFIGURA ESTOS VALORES ==========
access_key = 'ACCESS KEY'
secret_key = 'SECRET KEY'
region = 'us-east-1'
bucket = 'BUCKET NAME'
object_key = 'uploads/1037671417/images/1037671417_200425_010456_input.png'  # cambia esto
file_path = '1037671416.png'  # ruta local del archivo que vas a subir
# =============================================

service = 's3'
host = f'{bucket}.s3.{region}.amazonaws.com'
endpoint = f'https://{host}/{object_key}'

# Fecha y hora actual (UTC)
t = datetime.datetime.utcnow()
amz_date = t.strftime('%Y%m%dT%H%M%SZ')        # Ej: 20250410T120000Z
date_stamp = t.strftime('%Y%m%d')              # Ej: 20250410

# Funciones para la firma
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing

# Lee el archivo
with open(file_path, 'rb') as f:
    payload = f.read()

payload_hash = hashlib.sha256(payload).hexdigest()

canonical_uri = '/' + object_key
canonical_querystring = ''
canonical_headers = f'host:{host}\n' + f'x-amz-content-sha256:{payload_hash}\n' + f'x-amz-date:{amz_date}\n'
signed_headers = 'host;x-amz-content-sha256;x-amz-date'
canonical_request = f'PUT\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}'

# String to sign
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = f'{date_stamp}/{region}/{service}/aws4_request'
string_to_sign = f'{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()}'

# Firma
signing_key = get_signature_key(secret_key, date_stamp, region, service)
signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

# Header de autorización
authorization_header = f'{algorithm} Credential={access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}'

# Headers finales
headers = {
    'x-amz-date': amz_date,
    'x-amz-content-sha256': payload_hash,
    'Authorization': authorization_header,
    'Content-Type': 'image/jpeg'
}

# Envía el PUT
response = requests.put(endpoint, data=payload, headers=headers)

# Resultado
print('Código de respuesta:', response.status_code)
print('Contenido:', response.text)
