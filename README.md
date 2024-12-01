
# WeTransfer to SFTP Bot

Este proyecto es un bot de Telegram que permite descargar archivos de enlaces de **WeTransfer** y subirlos automáticamente a un servidor **SFTP**. Está diseñado para ser fácil de usar y configurable mediante un archivo `config.json`.

## Características

- Descarga archivos desde enlaces de **WeTransfer**.
- Sube automáticamente los archivos descargados a un servidor **SFTP**.
- Elimina los archivos locales después de subirlos.
- Configuración flexible mediante un archivo externo (`config.json`).
- Soporte para comandos específicos como `/wt <enlace>`.

---

## Requisitos

1. **Python 3.7+**.
2. Librerías de Python:
   - `python-telegram-bot`
   - `paramiko`
3. **Transferwee** para manejar los enlaces de WeTransfer.
4. Acceso a un servidor **SFTP**.
5. Una cuenta de **Telegram Bot** configurada con el token.

---

## Instalación

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/tuusuario/wetransfer-sftp-bot.git
   cd wetransfer-sftp-bot
   ```

2. **Crea un entorno virtual (opcional):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instala Transferwee:**
   - Clona el repositorio de Transferwee dentro de la carpeta `tmp`:
     ```bash
     git clone https://github.com/iamleot/transferwee.git
     ```
   - Instala Transferwee:
     ```bash
     cd transferwee
     python setup.py install
     ```
   - Verifica la instalación:
     ```bash
     transferwee --help
     ```
     Deberías ver las opciones y comandos disponibles de **Transferwee**.

5. **Configura `config.json`:**
   Crea un archivo `config.json` en el directorio raíz del proyecto con el siguiente contenido:
   ```json
   {
       "telegram_token": "TU_TELEGRAM_TOKEN",
       "sftp": {
           "host": "tu.sftp.server",
           "port": 22,
           "username": "tu_usuario",
           "password": "tu_contraseña",
           "target_folder": "/ruta/destino"
       }
   }
   ```
   - Reemplaza `TU_TELEGRAM_TOKEN` con el token de tu bot de Telegram.
   - Configura las credenciales y la ruta de destino del servidor SFTP.

---

## Uso

1. **Ejecuta el bot:**
   ```bash
   python script.py
   ```

2. **Comando disponible:**
   - `/wt <enlace>`: Proporciona un enlace de **WeTransfer** válido para descargar y subir al servidor SFTP.

   Ejemplo:
   ```
   /wt https://we.tl/t-47ebDDjQXX
   ```

   - El bot descargará el archivo y responderá con un mensaje confirmando la subida al servidor SFTP. La ruta del archivo se mostrará en formato monospaciado.

---

## Mensajes de Respuesta

### Éxito

- Si el archivo se descarga y se sube correctamente, el bot responderá con:
  ```
  Archivo subido correctamente al servidor SFTP:
  `/ruta/destino/nombre_archivo`
  ```

### Errores Comunes

1. **Sin enlace válido:**
   ```
   Por favor, proporciona un enlace válido de WeTransfer.
   ```

2. **Error en la descarga:**
   ```
   Error al descargar el archivo. Verifica el enlace.
   ```

3. **Error al subir al servidor SFTP:**
   ```
   Error al subir el archivo al servidor SFTP: <detalles del error>
   ```

4. **Archivos no encontrados:**
   ```
   No se encontraron archivos en la carpeta temporal.
   ```

---

## Estructura del Proyecto

```
wetransfer-sftp-bot/
├── config.json         # Configuración del bot y SFTP
├── script.py           # Código principal del bot
├── README.md           # Documentación del proyecto
├── requirements.txt    # Dependencias de Python
├── tmp/                # Carpeta temporal para descargas
     └── transferwee/   # Biblioteca para manejar enlaces de WeTransfer
```

---

## Configuración Avanzada

### Cambiar el Directorio Temporal
Por defecto, los archivos se descargan en la carpeta `tmp/`. Puedes cambiar esto modificando la variable `TEMP_FOLDER` en el script principal:

```python
TEMP_FOLDER = "nuevo_directorio"
```

### Modificar la Carpeta de Destino en el Servidor SFTP
La carpeta de destino en el servidor SFTP se configura en `config.json` bajo el campo `target_folder`.

---

## Desarrollo y Contribución

1. Haz un fork del proyecto.
2. Crea una rama para tus cambios:
   ```bash
   git checkout -b mi-nueva-funcionalidad
   ```
3. Realiza los cambios y crea un commit:
   ```bash
   git commit -m "Añadida mi nueva funcionalidad"
   ```
4. Sube los cambios a tu fork:
   ```bash
   git push origin mi-nueva-funcionalidad
   ```
5. Abre un pull request.

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.

---

## Créditos

- Este proyecto utiliza la biblioteca [Transferwee](https://github.com/iamleot/transferwee), desarrollada por **iamleot**, para manejar enlaces de WeTransfer.
- Usa [python-telegram-bot](https://python-telegram-bot.org/) para la integración con Telegram.
- Conexión SFTP implementada con [Paramiko](http://www.paramiko.org/).

---
