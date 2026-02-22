Pour faire fonctionnr ce script c'est très simple.

Mettre sur votre hebergement web dans un dossier /api le fichier receive.php 
Configurer donc un config.php a la racine pour joindre votre base de donner

CREATE DATABASE network_monitoring;
USE network_monitoring;

CREATE TABLE devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hostname VARCHAR(100),
    ip_address VARCHAR(50),
    os_version VARCHAR(255),
    uptime VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE interfaces (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id INT,
    interface_name VARCHAR(50),
    status VARCHAR(50),
    protocol VARCHAR(50),
    ip_address VARCHAR(50),
    FOREIGN KEY (device_id) REFERENCES devices(id)
);

Mettre les tokens a jours dans les fichiers
Installer les dépendences de python si besoins et voila
vous aurez sur le index toutes les informations 
