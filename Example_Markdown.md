
Outlook365
==========
Módulo para realizar acciones en Outlook Office 365  

# Commands

## Configurar Servidor
Configurar Servidor
### inputs

|Input|Description|example|
| :---: | :---: | :---: |
|User|add description here|user@example.com|
|Timeout|add description here|99|
|Contraseña|add description here|******|
|Asignar resultado a variable|add description here|Variable|

## Enviar Email
Envia un email, previamente debe configurar el servidor
### inputs

|Input|Description|example|
| :---: | :---: | :---: |
|Para|add description here|to@mail.com, to2@mail.com|
|Copia|add description here|cc@mail.com, cc2@mail.com|
|Asunto|add description here|Nuevo mail|
|Mensaje|add description here|Esto es una prueba|
|Archivo Adjunto|add description here|C:\User\Desktop\test.txt|
|Carpeta (Varios archivos)|add description here|C:\User\Desktop\Files|

## Lista todos los email
Lista todos los email, se puede especificar un filtro
### inputs

|Input|Description|example|
| :---: | :---: | :---: |
|Filtro|add description here|SUBJECT "COMPRA*"|
|Carpeta|add description here|345|
|Asignar a variable|add description here|Variable|

## Lista emails no leídos
Lista emails no leídos
### inputs

|Input|Description|example|
| :---: | :---: | :---: |
|Filtro|add description here|SUBJECT "COMPRA*"|
|Carpeta|add description here|inbox|
|Asignar a variable|add description here|Variable|

## Leer email por ID
Leer email por ID
### inputs

|Input|Description|example|
| :---: | :---: | :---: |
|ID del email|add description here|345|
|Carpeta|add description here|inbox|
|Asignar a variable|add description here|Variable|
|Ruta para descargar adjuntos|add description here|C:\User\Desktop|

## Crear Carpeta
Crea una carpeta
### inputs

|Input|Description|example|
| :---: | :---: | :---: |
|Nombre Carpeta|add description here|Ingrese nombre de la carpeta|

## Mover email a carpeta
Mueve email a carpeta
### inputs

|Input|Description|example|
| :---: | :---: | :---: |
|ID del email|add description here|Ingrese ID del email|
|Carpeta de destino|add description here|test|
|Nombre de la carpeta de origen|add description here|test|
|Asignar resultado a variable|add description here|Variable|

## Responder email por ID
Responder email por ID
### inputs

|Input|Description|example|
| :---: | :---: | :---: |
|ID Email|add description here|355|
|Carpeta del mail a responder|add description here|inbox|
|Mensaje|add description here|Esto es una prueba|
|Archivo Adjunto|add description here|C:\User\Desktop\test.txt|

## Reenviar email por ID
Reenviar email por ID
### inputs

|Input|Description|example|
| :---: | :---: | :---: |
|ID Email|add description here|355|
|Email|add description here|test@email.com|

## Listar Carpetas
Devuelve todas las carpetas
### inputs

|Input|Description|example|
| :---: | :---: | :---: |
|Asignar resultado a variable|add description here|Variable|

## Marcar email como no leído
Marcar email como no leído
### inputs

|Input|Description|example|
| :---: | :---: | :---: |
|Nombre Carpeta|add description here|inbox|
|ID del email|add description here|Ingrese ID del email|

## Cerrar Conexión
Cierra la conexión del servidor
### inputs

|Input|Description|example|
| :---: | :---: | :---: |
