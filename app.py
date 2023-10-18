from flask import Flask, request
import boto3
import psycopg2
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

# Configuración de AWS S3
s3 = boto3.client(
    's3',
    aws_access_key_id='AKIAT4VAMP5WTUBCNQPK',
    aws_secret_access_key='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',
    region_name='us-east-1'
)

# Configuración de PostgreSQL
conn = psycopg2.connect(
    host='databaseprojectuploaddownload.cckcb0zakvdq.us-east-1.rds.amazonaws.com',
    database='databaseprojectuploaddownload',
    user='postgres',
    password='jeison12',
    port=5432  # El puerto por defecto de PostgreSQL
)

cur = conn.cursor()

# Crear la tabla 'filelist' si no existe
try:
    cur.execute('CREATE TABLE IF NOT EXISTS filelist (id SERIAL PRIMARY KEY, filename VARCHAR(255), urlfile VARCHAR(255))')
    conn.commit()
except Exception as e:
    print(f'Error {e}')
    conn.rollback()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Falta el archivo en la solicitud', 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    
    # Guardar el archivo en S3
    s3.upload_fileobj(
        file,
        'bucketforprojectuploaddownload',
        'uploads/' + filename,
        ExtraArgs={'ACL': 'public-read'}
    )

    urlfile = f'https://bucketforprojectuploaddownload.s3.amazonaws.com/uploads/{filename}'

    # Guardar los datos en la base de datos
    try:
        cur.execute('INSERT INTO filelist (filename, urlfile) VALUES (%s, %s)', (filename, urlfile))
        conn.commit()
    except Exception as e:
        print(f'Error {e}')
        conn.rollback()

    return 'Archivo subido y registrado correctamente', 200

@app.route('/list', methods=['GET'])
def list_files():
    try:
        cur.execute('SELECT * FROM filelist')
        rows = cur.fetchall()
        return {'files': rows}, 200
    except Exception as e:
        print(f'Error {e}')
        conn.rollback()
        return 'Error interno del servidor', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

