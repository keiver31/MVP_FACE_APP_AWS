# LAMBDA ENVIO DE RESPUESTA A API GATEWAY

Importante: 
- Antes de iniciar la configuración descrita en esta sección, se deben realizar los pasos de [Save and Validation USER](./Lambda_SaveAndValidation_UserID.md)
- Despues de terminar de realizar la configuración descrita en esta sección, se deben realizar los pasos de [SEND LOGS TO DYNAMODB README](./Send_Logs_to_DynamoDB.md)

Siguiendo el orden correcto, se pueden realizar los ajustes correspondientes para la configuración de esta lambda, la cual consiste en capturar la información que se guardo en el archivo ".json" de la ruta "<NOMBRE-BUCKET/uploads/<user-id>/logs/file.json">, y entregar esta información a la API que se creo en el servicio API GATEWAY, cada vez que un usuario realice una solicitud HTTP.

## Manual Paso a Paso(Configuración AWS Lambda)

#### 1. Creación de la Lambda

- En AWS buscar el servicio "Lambda", dar clic en "Crear una función" y realizar las siguientes parametrizaciones:
- Crear desde cero
- Nombre de la función: "Test_Response_FaceApp"
- Tiempo de ejecución: Seleccionar "Python 3.13" o la versión más reciente.
- Arquitectura: x86_64
- Rol de ejecución: Seleccionar "Uso de un rol existente" y seleccionar "Nombre del rol". (Revisar sección "Configuraciones Adicionales/Creación del Rol")
- Dar clic en "Crear una función"
- Revisar en "Lambda/Funciones" la visualización de "Test_Response_FaceApp"


#### 2. Configuración de la Lambda

- En AWS ingresar a "Lambda/Funciones" y dar clic en "Test_Response_FaceApp".


#### 2.1 Configuración Parametros

- Dar clic en "Configuración" y en "Editar" (Modificaciónd de los parametros iniciales)
- Modificar el "Tiempo de espera", por defecto es "3 seg", se sugiere aumentarlo de 3-5 minutos.
- Dar clic en "Guardar"

#### 3. Código de la Lambda

- Revisar el script [Lambda_SendResponse_to_ApiGateway.py](../scripts/Lambda_SendResponse_to_ApiGateway.py)


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
          "name": "<NOMBRE-BUCKET>"
        },
        "object": {
          "key": "uploads/1037671417/images/1037671417_100425_011256_input.png"
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
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<NOMBRE-BUCKET>/uploads/*/logs/*"
        }
    ]
}
```

- Asignar nombre de "get_response_face-app"
- Dar clic en "Crear rol"