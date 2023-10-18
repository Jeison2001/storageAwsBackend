# Usar una imagen de Node.js
FROM node:20.8.0

# Crear un directorio de trabajo
WORKDIR /usr/src/app

# Copiar los archivos de configuración del paquete
COPY package*.json ./

# Instalar las dependencias
RUN npm install

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto que usa la aplicación
EXPOSE 80

# Comando para iniciar la aplicación
CMD [ "node", "index.js" ]
