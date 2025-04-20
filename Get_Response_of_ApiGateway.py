import requests

# URL base de la API
url = "URL BASE API"

# Parámetros de la consulta
params = {'file': '1037671417_200425_010456_input'}

# Encabezados de la solicitud
headers = {
    'Content-Type': 'application/json',
    'x-api-key': 'API-KEY'
}

# Realizar la solicitud GET
response = requests.get(url, headers=headers, params=params)

# Imprimir la respuesta
print(response.text)
