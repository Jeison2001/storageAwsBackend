# Usa una imagen base de Python 3.8
FROM python:3.8

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY main.py .
COPY models.py .
COPY requirements.txt .

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone el puerto 80
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
