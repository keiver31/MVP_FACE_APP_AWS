# CREACIÓN DE TABLA EN DYNAMO DB

Importante: 
- Antes de iniciar la configuración descrita en esta sección, se deben realizar los pasos de [SEND RESPONSE TO API GATEWAY README](./Send_Response_to_ApiGateway.md)


Siguiendo el orden correcto, se pueden realizar los ajustes correspondientes para la configuración de esta tabla en DynamoDB, la cual consiste en crear la tabla correspondiente y será el lugar, en donde se van a almacenar los diversos registros.

## Manual Paso a Paso(Configuración DynamoDB)

#### 1. Creación de la Tabla

##### 1.1. Acceder al servicio DynamoDB
- En la barra de búsqueda, escriir DynamoDB.
- Hacer clic en el servicio DynamoDB.

##### 1.2. Crear una nueva tabla
- En el panel lateral izquierdo, seleccionar "Tables".
- Presiona el botón "Create table".
- Configurar los detalles de la tabla

-> Table name: faceapp-verification-logs  
-> Partition key (clave de partición): uuid, String.  
-> Sort key (clave de ordenación): timestamp, String

##### 1.3. Crear la tabla

- Hacer clic en el botón "Create table".
- La tabla debe aparecer en la lista de Tables.
- Usar el botón "Explore table items" para insertar o consultar registros desde la consola.
