import os
import json
import subprocess
import paramiko  # Biblioteca para SFTP
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Cargar configuración desde archivo externo
CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config = json.load(file)

# Configuración del directorio temporal
TEMP_FOLDER = "tmp"
TRANSFERWEE_FOLDER = "transferwee"
TRANSFERWEE_SCRIPT = os.path.join(TRANSFERWEE_FOLDER, 'transferwee.py')

# Configuración del SFTP desde el archivo JSON
SFTP_CONFIG = config["sftp"]
SFTP_HOST = SFTP_CONFIG["host"]
SFTP_PORT = SFTP_CONFIG["port"]
SFTP_USERNAME = SFTP_CONFIG["username"]
SFTP_PASSWORD = SFTP_CONFIG["password"]
SFTP_TARGET_FOLDER = SFTP_CONFIG["target_folder"]

# Función para manejar el comando /wt
async def handle_wt_command(update: Update, context: CallbackContext):
    # Verifica si el usuario proporcionó un enlace
    if len(context.args) != 1:
        await update.message.reply_text("Uso correcto: /wt <enlace de WeTransfer>")
        return

    text = context.args[0]  # Obtiene el enlace proporcionado

    # Verifica si el enlace parece ser de WeTransfer
    if "we.tl" not in text:
        await update.message.reply_text("Por favor, proporciona un enlace válido de WeTransfer.")
        return

    await update.message.reply_text("Enlace de WeTransfer detectado. Descargando el archivo...")

    # Verifica si la carpeta temporal y transferwee existen
    if not os.path.exists(TEMP_FOLDER):
        await update.message.reply_text(f"La carpeta {TEMP_FOLDER} no existe. Por favor, verifica la configuración.")
        return
    if not os.path.exists(os.path.join(TEMP_FOLDER, TRANSFERWEE_SCRIPT)):
        await update.message.reply_text(f"El script {TRANSFERWEE_SCRIPT} no existe en {TEMP_FOLDER}.")
        return

    # Ejecuta transferwee dentro de la carpeta temporal
    result = subprocess.run(
        ['python3', TRANSFERWEE_SCRIPT, 'download', text],
        capture_output=True,
        text=True,
        cwd=TEMP_FOLDER
    )

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    if result.returncode == 0:
        downloaded_files = [
            os.path.join(TEMP_FOLDER, f) for f in os.listdir(TEMP_FOLDER)
            if os.path.isfile(os.path.join(TEMP_FOLDER, f)) and not f.startswith("transferwee") and not f == ".DS_Store"
        ]

        if downloaded_files:
            for file_path in downloaded_files:
                try:
                    # Subir archivo al servidor SFTP
                    remote_path = upload_to_sftp(file_path)
                    # Formatear la ruta como monospaciado
                    formatted_path = f"`{remote_path}`"
                    await update.message.reply_text(
                        f"Archivo subido correctamente al servidor SFTP:\n{formatted_path}",
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    await update.message.reply_text(f"Error al subir el archivo al servidor SFTP: {e}")
                finally:
                    # Verificar y eliminar archivo
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                            print(f"Archivo {file_path} eliminado correctamente.")
                        except Exception as e:
                            print(f"Error al eliminar archivo {file_path}: {e}")
                    else:
                        print(f"El archivo {file_path} no existe o ya fue eliminado.")
        else:
            await update.message.reply_text("No se encontraron archivos en la carpeta temporal.")
    else:
        await update.message.reply_text(f"Error al descargar el archivo. Verifica el enlace.\n{result.stderr}")

# Función para subir un archivo al servidor SFTP
def upload_to_sftp(file_path):
    try:
        # Conexión al servidor SFTP
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Subir archivo
        remote_path = os.path.join(SFTP_TARGET_FOLDER, os.path.basename(file_path))
        sftp.put(file_path, remote_path)
        print(f"Archivo {file_path} subido a {remote_path}")

        # Cerrar conexión
        sftp.close()
        transport.close()
        return remote_path
    except Exception as e:
        print(f"Error al subir archivo al servidor SFTP: {e}")
        raise

# Configurar el bot
def main():
    TOKEN = config["telegram_token"]  # Cargar token del archivo de configuración

    application = Application.builder().token(TOKEN).build()

    # Maneja el comando /wt
    application.add_handler(CommandHandler("wt", handle_wt_command))

    # Inicia el bot
    application.run_polling()

if __name__ == "__main__":
    main()