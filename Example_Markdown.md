
# Pipefy
  
Módulo para trabajar con la plataforma de Pipefy  
  
![banner](img/Banner_Pipefy.jpg)
## Como instalar este módulo
  
__Descarga__ e __instala__ el contenido en la carpeta 'modules' en la ruta de rocketbot.
## Como usar este module
  
Eiusmod veniam ut nisi minim in. Do et deserunt eiusmod veniam sint aliqua nulla adipisicing laboris voluptate fugiat 
ullamco elit do. Sint amet cillum fugiat excepteur mollit voluptate reprehenderit nisi commodo sint minim.
## Descripción de los comandos

### Conectar a pipefy
  
Con este comando se establece la autenticación con Pipefy
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Sesión|Identificador para cuando conectas con más de una cuenta|cuenta1|
|Token|Token obtenido en https//app.pipefy.com/tokens|eyJ1c2VyIjp7ImlkIjozMDEzMDY4NzYsImVtYWls.eyJ1c2VyIjp7ImlkIjozMDEzMDY4NzYsImVtYWlseyJ1c2VyIjp7ImlkIjozMDEzMDY4NzYsImVtYWlsIeyJ1c2VyIjp7ImlkIjozMDEzMDY4NzYsImVtYWlseyJ1c2VyIjp7ImlkIjozMDEzMDY4NzYsImVtYWlsa_kYAjHu7vN8k4_KKRcM7hVivhR1sr7RnCA|

### Crear Tarjeta
  
Con este comando puedes crear una tarjeta
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Sesión|Identificador para cuando conectas con más de una cuenta|cuenta1|
|Pipe Id|obten el id en la url del pipe |301741450|
|Campo de atributos|Lista de input para completar los campos de la tarjeta. Puedes obtener los field_id con el comando Obtener pipe por id|[{ 'field_id': 'nome_do_solicitante','field_value': 'Lucas'},{'field_id': 'e_mail_do_solicitante','field_value': 'user@email.com', |
|Archivo Adjunto|Ruta del archivo que se quiere adjuntar a la card|C:\User\Desktop\test.txt|
|Asignar a Variable|Nombre de variable sin llaves {}|variable|

### Obtener Pipe por ID
  
Con este comando puedes obtener información de los campos de un pipe desde su id
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Sesión|Identificador para cuando conectas con más de una cuenta|cuenta1|
|Pipe Id|obten el id en la url del pipe |301741450|
|Asignar a Variable|Nombre de variable sin llaves {}|variable|

### Subir archivo
  
Con este comando puedes subir un arhcivo a Pipefy y usar el nombre de archivo resultante en otro comando
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Sesión|Identificador para cuando conectas con más de una cuenta|cuenta1|
|Asignar a Variable|Nombre de variable sin llaves {}|variable|
|Archivo Adjunto|Ruta del archivo que se quiere adjuntar a la card|C:\User\Desktop\test.txt|
