-- Crear base de datos
CREATE DATABASE IF NOT EXISTS pparcial;
USE pparcial;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Crear tabla para la primera serie de aproximación trigonométrica
CREATE TABLE IF NOT EXISTS serie_trig_1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    valor_aproximado FLOAT NOT NULL,
    valor_real FLOAT NOT NULL,
    error FLOAT NOT NULL
);

-- Crear tabla para la segunda serie de aproximación trigonométrica
CREATE TABLE IF NOT EXISTS serie_trig_2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    valor_aproximado FLOAT NOT NULL,
    valor_real FLOAT NOT NULL,
    error FLOAT NOT NULL
);

-- Crear tabla para la tercera serie de aproximación trigonométrica
CREATE TABLE IF NOT EXISTS serie_trig_3 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    valor_aproximado FLOAT NOT NULL,
    valor_real FLOAT NOT NULL,
    error FLOAT NOT NULL
);

-- Modificar las tablas de series trigonométricas para que incluyan el usuario que ingresó los datos
ALTER TABLE serie_trig_1 ADD COLUMN usuario_id INT;
ALTER TABLE serie_trig_2 ADD COLUMN usuario_id INT;
ALTER TABLE serie_trig_3 ADD COLUMN usuario_id INT;

-- Añadir la clave foránea a las tablas de series trigonométricas
ALTER TABLE serie_trig_1 ADD CONSTRAINT fk_usuario_serie_trig_1 FOREIGN KEY (usuario_id) REFERENCES usuarios(id);
ALTER TABLE serie_trig_2 ADD CONSTRAINT fk_usuario_serie_trig_2 FOREIGN KEY (usuario_id) REFERENCES usuarios(id);
ALTER TABLE serie_trig_3 ADD CONSTRAINT fk_usuario_serie_trig_3 FOREIGN KEY (usuario_id) REFERENCES usuarios(id);