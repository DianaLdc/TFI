README – Instrucciones de Ejecución de la Aplicación Web
1. Requisitos del sistema

Para ejecutar correctamente la aplicación web es necesario contar con los siguientes componentes instalados:

Sistema operativo Linux (Ubuntu o similar)

Python 3.10 o superior

Navegador web moderno (Chrome, Firefox, etc.)

No se utilizan frameworks externos para el backend.

2. Estructura del proyecto

El proyecto presenta la siguiente estructura de archivos y carpetas:

TFI/
│
├── server.py
├── index.html
├── assets/
│   ├── css/
│   │   └── main.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── (imágenes del sitio)
│
└── contacto.db

3. Ejecución del servidor

Abrir una terminal y ubicarse en la carpeta raíz del proyecto:

cd Documentos/TFI


Ejecutar el servidor con el siguiente comando:

python3 server.py


El servidor se iniciará en la siguiente dirección:

http://localhost:8000

4. Uso de la aplicación

Para acceder a la página principal:

http://localhost:8000


Para enviar un mensaje:

Ingresar a la sección de contacto.

Completar el formulario con los datos solicitados.

Presionar el botón “Enviar”.

Para visualizar los mensajes almacenados:

http://localhost:8000/mensajes


Se solicitarán credenciales de acceso:

Usuario: admin

Contraseña: 1234

5. Base de datos

La aplicación utiliza una base de datos local (contacto.db) que se crea automáticamente al iniciar el servidor por primera vez. En ella se almacenan los mensajes enviados desde el formulario de contacto.

6. Observaciones

El backend fue desarrollado utilizando Python puro mediante el módulo http.server.

El manejo de rutas y formularios se realiza manualmente, sin el uso de frameworks.

El acceso a los mensajes se encuentra protegido mediante autenticación básica.
