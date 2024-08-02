import openai
import logging
import mysql.connector
from mysql.connector import Error
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Reemplaza 'TU_TOKEN_AQUI' con tu token de bot de Telegram
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Reemplaza 'TU_API_KEY_OPENAI' con tu clave API de OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Configuración de la base de datos
DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Configura tu clave API de OpenAI
openai.api_key = OPENAI_API_KEY

def chatgpt_response(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Cambiado a un modelo compatible
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,  # Ajustado para respuestas más largas
            temperature=0.7  # Añadido para respuestas más naturales
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Perdona, parece que me ha dado un pequeño shock404, podrías repetir la pregunta?: {str(e)}"

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,           # Usa la variable de entorno para el host de la base de datos
            database=DB_DATABASE,   # Usa la variable de entorno para el nombre de la base de datos
            user=DB_USER,           # Usa la variable de entorno para el usuario de MySQL
            password=DB_PASSWORD    # Usa la variable de entorno para la contraseña de MySQL
        )
        if connection.is_connected():
            print('Conexión exitosa a la base de datos')
            return connection
    except Error as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None

def save_to_database(user_message: str, bot_response: str):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO messages (user_message, bot_response)
            VALUES (%s, %s)
            """
            cursor.execute(insert_query, (user_message, bot_response))
            connection.commit()
            print("Mensaje guardado en la base de datos")
        except Error as e:
            print(f'Error al guardar en la base de datos: {e}')
        finally:
            cursor.close()
            connection.close()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¡Hola! Soy tu bot de confianza. Si quieres charlar o tienes alguna duda sobre algo, envíame un mensaje y te responderé lo mejor que pueda.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Envíame cualquier mensaje y te responderé gracias a mi gemelo ChatGPT.')

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = chatgpt_response(user_message)
    
    # Guardar en la base de datos
    save_to_database(user_message, response)
    
    # Dividir la respuesta en partes de máximo 4096 caracteres para Telegram
    for i in range(0, len(response), 4096):
        update.message.reply_text(response[i:i+4096])

def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
