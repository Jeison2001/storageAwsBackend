import boto3, os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import FileRecord
from models import Base

app = FastAPI()

# Configura la conexión a la base de datos
db_uri = "postgresql://postgres:jeison12@databaseprojectuploaddownload.cckcb0zakvdq.us-east-1.rds.amazonaws.com/databaseprojectuploaddownload"
engine = create_engine(db_uri)

# Credenciales de AWS
aws_access_key_id = "AKIAT4VAMP5W77H6YL7K"
aws_secret_access_key = "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"

# Configura las credenciales de AWS
os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key

# Configura la región de AWS
aws_region = 'us-east-1'

# Crea una sesión de base de datos
Session = sessionmaker(bind=engine)

# Configura el cliente de S3 con la región especificada
s3 = boto3.client('s3', region_name=aws_region)

# Crear la tabla si no existe
Base.metadata.create_all(engine)

# Ruta para cargar un archivo
@app.post("/upload/")
async def upload_file(file: UploadFile):
    # Registra el archivo en la base de datos
    db_session = Session()
    file_record = FileRecord(descripcion=file.filename, url=f"https://bucketforprojectuploaddownload.s3.amazonaws.com/{file.filename}")
    db_session.add(file_record)
    db_session.commit()
    db_session.close()

    # Carga el archivo en S3
    s3.upload_fileobj(file.file, 'bucketforprojectuploaddownload', file.filename)
    return {"message": "File uploaded and recorded successfully"}

# Ruta para listar los archivos registrados en la base de datos
@app.get("/list")
async def list_files():
    db_session = Session()
    files = db_session.query(FileRecord).all()
    db_session.close()
    return files

# Ruta para descargar un archivo desde S3
@app.get("/download/")
async def download_file(file: int):
    # Recuperar el registro por el nuevo campo 'id'
    db_session = Session()
    file_record = db_session.query(FileRecord).filter(FileRecord.id == file).first()
    db_session.close()
    
    if file_record:
        s3.download_file('bucketforprojectuploaddownload', file_record.url, file_record.descripcion)
        return FileResponse(file_record.descripcion)
    else:
        return {"message": "File not found"}
