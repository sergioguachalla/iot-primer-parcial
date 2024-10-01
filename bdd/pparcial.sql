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
