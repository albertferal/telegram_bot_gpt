# Proyecto de Bot de Telegram y Aplicación Flask

Este proyecto consiste en dos partes principales:

1. **Bot de Telegram**: Un bot que utiliza la API de OpenAI para responder mensajes y guarda las conversaciones en una base de datos MySQL.
2. **Aplicación Flask**: Una interfaz web para visualizar los mensajes guardados en la base de datos.

## Estructura del Proyecto
```
telegram_bot/
└── bot.py
flask_app/
├── app.py
└── templates/
└── index.html
```

## Requisitos

Para ejecutar este proyecto, asegúrate de tener instalados los siguientes paquetes:

- **Python 3.x**
- **pip** (gestor de paquetes de Python)

### Dependencias

El bot de Telegram y la aplicación Flask requieren las siguientes bibliotecas:

- `python-telegram-bot`
- `openai`
- `mysql-connector-python`
- `python-dotenv`
- `Flask`
- `markupsafe`

Puedes instalar las dependencias necesarias con:

```
pip install -r requirements.txt
```


## Archivos de Entorno
Debes crear un archivo .env en el directorio raíz del proyecto con las siguientes variables de entorno:


#### Variables para el bot de Telegram
```
TELEGRAM_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
```
#### Variables para la base de datos
```
DB_HOST=localhost
DB_DATABASE=mydatabase
DB_USER=root
DB_PASSWORD=your_mysql_password_here
```
#### Variables para la autenticación básica en la aplicación Flask
```
AUTH_USER=your_user_here
AUTH_PASSWORD=your_password_here
```

Reemplaza todos los valores con tus propias credenciales.

## Uso del Bot de Telegram
Asegúrate de que el archivo .env esté correctamente configurado.

Ejecuta el bot con el siguiente comando:
```
python telegram_bot/bot.py
```
El bot responderá a los mensajes enviados y almacenará las conversaciones en la base de datos.

## Aplicación Flask
1. Asegúrate de que el archivo .env esté correctamente configurado.

Ejecuta la aplicación Flask con:
```
python flask_app/app.py
```

2. Abre tu navegador web y visita http://localhost:5000.

3. Inicia sesión con las credenciales especificadas en el archivo .env.

### Documentación de referencia:
- Telegram bots: https://core.telegram.org/bots/api
- OpenAI APIS: https://openai.com/index/openai-api/
- Python: https://docs.python.org/3/
- MySQL: https://dev.mysql.com/doc/


#### || Autor: Albert Fernández || Web personal: https://aferal.es ||
