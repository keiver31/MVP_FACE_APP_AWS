# CREACIÓN E INTEGRACIÓN DESDE API GATEWAY

Importante: 
- Antes de iniciar la configuración descrita en esta sección, se deben realizar los pasos de [Creación Bucket S3 README](./Create_Bucket_S3.md) y [Save and Validation USER](./Lambda_SaveAndValidation_UserID.md)


Siguiendo el orden correcto, se pueden realizar los ajustes correspondientes para la configuración del API GATEWAY.

## Manual Paso a Paso(Creación API)

#### 1. Creación API

- En AWS buscar el servicio "API Gateway", dar clic en "API Gateway", y realizar las siguientes parametrizaciones:
- Dar clic en "Build" en la opción "REST API"
- Seleccionar "NEW API", nombrar la API, asiggnar una descripción para la API,  seleccionar la opción "Regional" en "API endpoint type" y "IPv4" en "IP address type". Después de esto, dar clic en "Create API"
- Asignar el nombre de "etl_s3_to_rds_v2.0".
- IAM Role: Seleccionar el rol o realizar la creación del rol(Revisar sección "Configuraciones Adicionales/Creación del Rol")
- Requested number of workers: Ingresar 10(se pueden seleccionar más o menos de acuerdo a la necesidad)

#### 1.1. Configuración API KEYS

- En el menú izquierdo, ir a "API Keys".
- Hacer clic en el botón "Create API Key".
- Completar los campos:
Name: Nombre descriptivo de la clave.  
API Key: (Opcional) (Se puede personalizar o autogenerar)
- Activar la opción "Enabled".
- Hacer clic en "Save".
- Guardar el "API Key"(Este se configurara en la solicitud HTTP que se va a realizar)


#### 1.2. Configuración de los Usage Plans


- Ir a la sección "Usage Plans" en el menú lateral.
- Crear un nuevo plan de uso (Create usage plan) o editar uno existente.
- Establecer límites si es necesario:
Rate (solicitudes por segundo)  
Burst (número máximo de solicitudes instantáneas permitidas)  

- En la sección "Associated API stages", vincular la API y su etapa (dev, prod, etc.).
- Guardar el plan.

#### 1.3. Asociar la API Key al Usage Plan

- En el Usage Plan creado, ir a la pestaña "API Keys" o "Associated API keys".
- Hacer clic en "Add API Key".
- Seleccionar la API Key que se creó previamente y guardarla.

#### 1.4. Configuración API

- En la parte izquierda, ingresar a la opción "APIs" y dar clic en la API que se creo.
- Para este caso se creo un recurso en la opción "Create resource", el cual contiene un método "GET".
- Se debe crear un método "GET" para este proyecto, ya que en este se consulta el estado de la solicitud HTTP que se envio.
- Dar clic en la opción "GET" y realizar las siguientes configuraciones:

Method request:  
→ API key required: True  

Integration request:  
→ Integration type: Lambda  
→ Lambda proxy integration: True  
→ Lambda function: Test_Response_FaceApp(Revisar el documento [Creación RDS_MySQL README](./RDS_MySQL.md))


## 

