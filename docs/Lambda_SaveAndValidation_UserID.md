# LAMBDA ALMACENAMIENTO EN S3 Y VALIDACIÓN DE IDENTIDAD

Importante: 
- Antes de iniciar la configuración descrita en esta sección, se deben realizar los pasos de [Creación Bucket S3 README](./Create_Bucket_S3.md)
- Despues de terminar de realizar la configuración descrita en esta sección, se deben realizar los pasos de [SEND RESPONSE TO API GATEWAY README](./Send_Response_to_ApiGateway.md)

Siguiendo el orden correcto, se pueden realizar los ajustes correspondientes para la configuración de esta lambda, la cual consiste en almacenar las imagenes de cada USUARIO en S3 y realizar la validación, respecto al archivo de referencia que se tiene en cada folder, esta validación se guarda en un archivo "json", el cual se carga posteriormente en el folder "logs" de cada Usuario.  
Se cuenta con un trigger el cual, cada vez que se recibe un ".png", se encarga de capturarlo y enviarlo hacia la Lambda.

## Manual Paso a Paso(Configuración AWS Lambda)

#### 1. Creación de la Lambda

- En AWS buscar el servicio "Lambda", dar clic en "Crear una función" y realizar las siguientes parametrizaciones:
- Crear desde cero
- Nombre de la función: "Test_FaceApp"
- Tiempo de ejecución: Seleccionar "Python 3.13" o la versión más reciente.
- Arquitectura: x86_64
- Rol de ejecución: Seleccionar "Uso de un rol existente" y seleccionar "Nombre del rol". (Revisar sección "Configuraciones Adicionales/Creación del Rol")
- Dar clic en "Crear una función"
- Revisar en "Lambda/Funciones" la visualización de "Test_FaceApp"


#### 2. Configuración de la Lambda

- En AWS ingresar a "Lambda/Funciones" y dar clic en "Test_FaceApp".


#### 2.1 Configuración Parametros

- Dar clic en "Configuración" y en "Editar" (Modificaciónd de los parametros iniciales)
- Modificar el "Tiempo de espera", por defecto es "3 seg", se sugiere aumentarlo de 3-5 minutos.
- Dar clic en "Guardar"

#### 3. Código de la Lambda

- Revisar el script [Lambda_SaveS3_and_ValidationUser.py](../scripts/Lambda_SaveS3_and_ValidationUser.py)


#### 4. Ejecución de la Lambda

- Dar clic en "Deploy", esperar al mensaje de confirmación.
- Dar clic en "Test", esperar el mensaje de confirmación.

#### 5. Validación del proceso

- Event JSON:
```json
{
  "queryStringParameters": {
    "file": "1037671417_100425_011256_input"
  }
}
```


- En la pestaña "OUTPUT", debe aparecer el siguiente mensaje:

Response:
```json
{
  "statusCode": 200,
  "body": "{\"message\": \"\\u2705 Usuario reconocido con 99.99% de similitud.\", \"log_path\": \"uploads/1037671417/logs/1037671417_100425_011256_input.json\", \"resultado\": \"MATCH\"}"
}
```

- Validar en el BUCKET de S3, la existencia del archivo json y comprobar manualmente que la validación que se esta realizando,corresponde a la respuesta entregada por la lambda.




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
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::<NOMBRE-BUCKET>/uploads/*",
                "arn:aws:s3:::<NOMBRE-BUCKET>/users/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": "rekognition:CompareFaces",
            "Resource": "*"
        }
    ]
}
```

- Asignar nombre de "face-verification-lambda-role"
- Dar clic en "Crear rol"