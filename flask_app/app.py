from flask import Flask, render_template, request, Response
from markupsafe import Markup
import mysql.connector
from functools import wraps
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

def authenticate(username, password):
    """ Verifica el nombre de usuario y la contraseña """
    return username == os.getenv('AUTH_USER') and password == os.getenv('AUTH_PASSWORD')

def requires_auth(f):
    """ Decorador que protege las rutas con autenticación básica """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not authenticate(auth.username, auth.password):
            return Response(
                'Acceso denegado', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
        return f(*args, **kwargs)
    return decorated

def highlight_search_term(text, search_term):
    if not search_term:
        return Markup(text)
    highlighted = text.replace(search_term, f'<mark>{search_term}</mark>')
    return Markup(highlighted)

def get_data(search_query=None, start_date=None, end_date=None):
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_DATABASE'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM messages"
    params = []
    
    if search_query:
        query += " WHERE (user_message LIKE %s OR bot_response LIKE %s)"
        params.extend(['%' + search_query + '%', '%' + search_query + '%'])
    
    if start_date and end_date:
        if params:
            query += " AND (timestamp BETWEEN %s AND %s)"
        else:
            query += " WHERE (timestamp BETWEEN %s AND %s)"
        params.extend([start_date, end_date])
    
    query += " ORDER BY timestamp DESC"
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    if search_query:
        for row in data:
            row['user_message'] = highlight_search_term(row['user_message'], search_query)
            row['bot_response'] = highlight_search_term(row['bot_response'], search_query)
    
    cursor.close()
    conn.close()
    
    if not data:
        if search_query:
            return [], "No se encuentran mensajes que incluyan estas palabras"
        elif start_date and end_date:
            return [], "No se encuentran mensajes en las fechas especificadas"
    
    return data, None

@app.route('/')
@requires_auth
def index():
    search_query = request.args.get('search')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    data, message = get_data(search_query, start_date, end_date)
    return render_template('index.html', data=data, search_query=search_query, start_date=start_date, end_date=end_date, message=message)

if __name__ == '__main__':
    app.run(debug=True)
