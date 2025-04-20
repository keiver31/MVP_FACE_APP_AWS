# LAMBDA ALMACENAMIENTO DE LOGS EN DYNAMODB

Importante: 
- Antes de iniciar la configuración descrita en esta sección, se deben realizar los pasos de [SEND RESPONSE TO API GATEWAY README](./Send_Response_to_ApiGateway.md) y [CREATION TABLE DYNAMODB README](./Creation_Table_DynamoDB.md)


Siguiendo el orden correcto, se pueden realizar los ajustes correspondientes para la configuración de esta lambda, la cual consiste en capturar la información que se guardo en los archivos ".json" de la ruta "<NOMBRE-BUCKET/uploads/<user-id>/logs/file.json">, y guardar esta información en la tabla "faceapp-verification-logs" de DynamoDB.  
Se cuenta con un trigger el cual, cada vez que se crea un ".json", se encarga de capturarlo y enviarlo hacia la Lambda.

## Manual Paso a Paso(Configuración AWS Lambda)

#### 1. Creación de la Lambda

- En AWS buscar el servicio "Lambda", dar clic en "Crear una función" y realizar las siguientes parametrizaciones:
- Crear desde cero
- Nombre de la función: "log-json-to-dynamodb-faceapp"
- Tiempo de ejecución: Seleccionar "Python 3.13" o la versión más reciente.
- Arquitectura: x86_64
- Rol de ejecución: Seleccionar "Uso de un rol existente" y seleccionar "Nombre del rol". (Revisar sección "Configuraciones Adicionales/Creación del Rol")
- Dar clic en "Crear una función"
- Revisar en "Lambda/Funciones" la visualización de "log-json-to-dynamodb-faceapp"


#### 2. Configuración de la Lambda

- En AWS ingresar a "Lambda/Funciones" y dar clic en "log-json-to-dynamodb-faceapp".


#### 2.1 Configuración Parametros

- Dar clic en "Configuración" y en "Editar" (Modificaciónd de los parametros iniciales)
- Modificar el "Tiempo de espera", por defecto es "3 seg", se sugiere aumentarlo de 3-5 minutos.
- Dar clic en "Guardar"  

  
- En "Environment variables", crear una variable de entorno, llamada "TABLE_NAME", la cual contiene el valor de la tabla creada en DynamoDB.

#### 3. Código de la Lambda

- Revisar el script [Lambda_SendResponse_to_ApiGateway.py](../scripts/Send_Logs_to_DynamoDB.py)


#### 4. Ejecución de la Lambda

- Dar clic en "Deploy", esperar al mensaje de confirmación.
- Dar clic en "Test", esperar el mensaje de confirmación.

#### 5. Validación del proceso

- Event JSON:
```json
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "face-verification-bucket-app"
        },
        "object": {
          "key": "uploads/1037671417/logs/1037671417_060425_235056_input.json"
        }
      }
    }
  ]
}

```

- En la pestaña "OUTPUT", debe aparecer el siguiente mensaje:

Response:
```json
{
  "statusCode": 200,
  "body": "{\"uuid\": \"68cd1e69-7692-4682-99af-811c6a65e829\", \"user_id\": \"1037671417\", \"fecha\": \"10/04/25\", \"hora\": \"01:12:56\", \"movimiento\": \"input\", \"resultado\": \"MATCH\", \"mensaje\": \"\\u2705 Usuario reconocido con 99.99% de similitud.\", \"timestamp\": \"2025-04-19T22:46:23.481376Z\"}",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

- Validar mediante una solicitud HTTP, la respuesta de la Lambda, para esto se debe tener la certeza de que ya se cargo un archivo en S3.




## Configuraciones Adicionales

#### 1. Creación del Rol

##### 1.1 Ingresar al servicio de AWS "IAM"
##### 1.2 Seleccionar "Roles" y dar clic en "Crear rol"
##### 1.3 Realizar la siguiente parametrización.

- Tipo de entidad de confianza: "Servicio de AWS"
- Caso de uso: "Lambda" y dar clic en "Siguiente"
- Politica de permisos: Seleccionar "Create policy" y establecer la siguiente información:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem"
            ],
            "Resource": "arn:aws:dynamodb:us-east-1:<ID-TABLE-DYNAMODB>/<NOMBRE-BUCKET>"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::<NOMBRE-BUCKET>/*"
        }
    ]
}
```

- Asignar nombre de "log-json-to-dynamodb-faceapp-role-n3c2ttho"
- Dar clic en "Crear rol"