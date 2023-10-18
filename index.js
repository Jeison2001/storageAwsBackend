const express = require('express');
const AWS = require('aws-sdk');
const multer = require('multer');
const multerS3 = require('multer-s3');
const pg = require('pg');

const app = express();

// Configuración de AWS S3
AWS.config.update({
  accessKeyId: 'AKIAT4VAMP5WTUBCNQPK',
  secretAccessKey: '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',
  region: 'us-east-1',
});
const s3 = new AWS.S3();

// Configuración de PostgreSQL
const pgConfig = {
  host: 'databaseprojectuploaddownload.cckcb0zakvdq.us-east-1.rds.amazonaws.com',
  database: 'databaseprojectuploaddownload',
  user: 'postgres',
  password: 'jeison12',
  port: 5432, // El puerto por defecto de PostgreSQL
};

const client = new pg.Client(pgConfig);

client.connect();

// Crear la tabla 'filelist' si no existe
client.query('CREATE TABLE IF NOT EXISTS filelist (id SERIAL PRIMARY KEY, filename VARCHAR(255), urlfile VARCHAR(255))', (err, result) => {
  if (err) {
    console.error('Error al crear la tabla:', err);
  }
});

// Configurar el almacenamiento con Multer y S3
const upload = multer({
  storage: multerS3({
    s3: s3,
    bucket: 'bucketforprojectuploaddownload',
    acl: 'public-read', // Puedes ajustar los permisos según tus necesidades
    key: (req, file, cb) => {
      cb(null, 'uploads/' + Date.now() + file.originalname);
    },
  }),
});

// Ruta para cargar archivos
app.post('/upload', upload.single('file'), (req, res) => {
  if (req.file) {
    const { filename, location: urlfile } = req.file;
    
    // Guardar los datos en la base de datos
    client.query('INSERT INTO filelist (filename, urlfile) VALUES ($1, $2)', [filename, urlfile], (err, result) => {
      if (err) {
        console.error('Error al insertar en la base de datos:', err);
        res.status(500).send('Error interno del servidor');
      } else {
        res.status(200).send('Archivo subido y registrado correctamente');
      }
    });
  } else {
    res.status(400).send('Falta el archivo en la solicitud');
  }
});

// Ruta para obtener la lista de archivos
app.get('/list', (req, res) => {
  client.query('SELECT * FROM filelist', (err, result) => {
    if (err) {
      console.error('Error al consultar la base de datos:', err);
      res.status(500).send('Error interno del servidor');
    } else {
      res.status(200).json(result.rows);
    }
  });
});

// Puerto en el que el servidor escuchará
const port = process.env.PORT || 80;

app.listen(port, () => {
  console.log(`Servidor en ejecución en el puerto ${port}`);
});