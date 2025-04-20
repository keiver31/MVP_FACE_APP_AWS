
# Creación Bucket S3

Importante: 

- Despues de terminar de realizar la configuración descrita en esta sección, se deben realizar los pasos de [Api Gateway  README](./ApiGateway_to_HTTP.md)

Siguiendo el orden correcto, se pueden realizar los ajustes correspondientes para la configuración del bucket y de los permisos correspondientes.

## Manual Paso a Paso(Creación del Bucket)

#### 1. Creación del Bucket

- En AWS buscar el servicio "S3", dar clic en "Crear bucket" y realizar las siguientes parametrizaciones:
- Tipo de bucket: Uso general
- Nombre del bucket: "<NOMBRE-BUCKET>"
- Propiedad de objetos: ACL deshabilitadas (recomendado)
- Configuración de bloqueo de acceso público para este bucket: No seleccionar la opción "Bloquear todo el acceso público"
- Control de versiones de buckets: Desactivar
- Tipo de cifrado: Cifrado del servidor con claves administradas de Amazon S3 (SSE-S3)
- Clave de bucket: Habilitar
- Dar clic en "Crear bucket"
- Revisar en "S3/Buckets" la visualización de "<NOMBRE-BUCKET>"


#### 2. Modificación de permisos 


##### 2.1 Permisos del bucket (Bucket Policy)    

Path: Amazon S3 / Buckets / <TU-BUCKET> / Permissions / Bucket policy

Para permitir el acceso adecuado al bucket de S3, se configuró una Bucket Policy personalizada en la sección Permissions. Esta política define qué servicios o usuarios pueden interactuar con el bucket, estableciendo reglas de lectura, escritura o acceso público según sea necesario.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowPresignedUploads",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::<NOMBRE-BUCKET>/uploads/*",
            "Condition": {
                "StringEquals": {
                    "s3:authType": "REST-HEADER"
                }
            }
        }
    ]
}
```


##### 2.2 Configuración de CORS en Amazon S3
  

Path: Amazon S3 / Buckets / face-verification-bucket-app / Permissions / Cross-origin resource sharing (CORS)


Se configuró una política de Cross-Origin Resource Sharing (CORS) en el bucket de Amazon S3 para permitir solicitudes desde cualquier origen (*) utilizando los métodos HTTP GET, POST y PUT. Además, se aceptan todos los encabezados (*) en las solicitudes. Esta configuración es especialmente útil para habilitar la interacción de aplicaciones web alojadas en diferentes dominios con los recursos del bucket, facilitando operaciones como cargas de archivos, formularios o consultas desde navegadores.​

A continuación, se muestra la configuración aplicada:  

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["PUT", "POST", "GET"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": []
  }
]


```


##### 2.3 Configuración de Triggers en S3


Se configuró una notificación de eventos en el bucket de Amazon S3 para automatizar acciones en respuesta a eventos específicos de acciones que se realizan en el proceso e interfieren o se llevan a cabo en los otros servicios de AWS.

Path: Amazon S3 / Buckets / face-verification-bucket-app / Permissions / Create event notification


- Seleccionar "Create event notification".
- Asignar "face-verification-trigger" y "json-log-to-dynamo" para cada Trigger.
- En prefijo registrar "uploads" que hace parte de la ruta "face-verification-bucket-app/uploads/" del bucket creado, esto para cada Trigger.
- En sufijo registrar ".png" y ".json" para cada Trigger.
- En ""Event types" se va a seleccionar el método "Put" de la opción "Object creation"
- Seleccionar el destino de la notificación: "AWS Lambda: Para ejecutar funciones sin servidor.​"
- Seleccionar la lambda "Test_FaceApp" y "log-json-to-dynamodb-faceapp" (Revisar documentación)
- Guardar la configuración.


## Configuraciones Adicionales

#### 1. Creación del Usuario en IAM

##### 1.1 Ingresar al servicio de AWS "IAM"
##### 1.2 Seleccionar "Users" y dar clic en "Crear Usuario"
##### 1.3 Realizar la siguiente parametrización.

- Username: "s3-uploader"
- Permissions options: Dar clic en "Attach policies directly" y luego dar clic en "Create policy", se abre un nueva ventana, en la cual se crea la politica "Put-Image-S3" con las siguientes caracteristicas:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::<NOMBRE-BUCKET>/uploads/*"
        }
    ]
}

```

- Se da clic en "Create user" y se valida que el usuario se haya creado de manera exitosa.


##### 1.4 Creacción de Access Key para peticiones HTTP

- Dar clic en el user "s3-uploader", ingresar a la sección "Security credentials" y dar clic en "Create Access key".
- Seleccionar el caso de uso(Command Line Interface (CLI), Local Code, otros) correspondiente, ingresar la descripción solicitada(opcional) y dar clic en "Crear Access Key".
- Guardar las credenciales del "Access Key" que se genero, ya que estas son las que se van a configurar en POSTMAN.


## 📂 Estructura del Bucket S3

```plaintext
<NOMBRE-BUCKET>/
├── uploads/
│   └── <USER-ID>/
│       ├── images/
│       └── logs/
└── users/
    └── <USER-ID>/
        └── reference.png

```

- uploads/<USER-ID>/images/ → Carpeta donde se almacenan las imágenes subidas por el usuario.

- uploads/<USER-ID>/logs/ → Carpeta para almacenar logs individuales de cada usuario y la respuesta que entrego Rekognition en su proceso de identificación.

- users/<USER-ID>/reference.png → Imagen de referencia asociada al usuario (ej.: para reconocimiento facial).