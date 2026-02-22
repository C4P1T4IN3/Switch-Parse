Network Monitoring Script

Un script simple pour surveiller vos appareils réseau et leurs interfaces via Python et PHP, avec stockage des données dans une base MySQL.

Fonctionnalités

Collecte automatique des informations des appareils réseau :

Nom d’hôte (hostname)

Adresse IP

Version de l’OS

Temps de fonctionnement (uptime)

Collecte des informations des interfaces réseau :

Nom de l’interface

Statut et protocole

Adresse IP

Stockage des données dans MySQL

Interface simple pour visualiser les données depuis un index HTML/PHP

Prérequis

PHP ≥ 7.4

Python ≥ 3.8

Serveur web (Apache, Nginx…)

Base de données MySQL

Accès SSH sur vos équipements réseau (pour la collecte via Python, si besoin)

Installation

Base de données

Créez une base de données et les tables nécessaires :

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

Fichiers PHP

Placez receive.php dans le dossier /api de votre hébergement web.

Configurez config.php à la racine pour connecter votre script à la base MySQL.

Exemple minimal config.php :

<?php
$host = "localhost";
$db   = "network_monitoring";
$user = "votre_utilisateur";
$pass = "votre_mot_de_passe";

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db;charset=utf8", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Erreur de connexion : " . $e->getMessage());
}
?>

Tokens de sécurité

Mettez à jour les tokens dans vos fichiers PHP et Python.

Pour générer un token sécurisé :

openssl rand -hex 32

Script Python

Installez les dépendances Python si nécessaire :

pip install -r requirements.txt

Configurez les informations de connexion aux appareils réseau et la cible /api/receive.php pour envoyer les données.

Accéder à l’interface

Après avoir tout configuré et lancé les scripts Python, ouvrez votre index.php dans un navigateur.

Vous devriez voir toutes les informations collectées en temps réel.

Structure des fichiers
/ (racine)
├─ config.php           # Configuration base de données
├─ index.php            # Affichage des données
└─ /api
   └─ receive.php       # Endpoint pour recevoir les données
Sécurité

Ne partagez jamais vos tokens ni identifiants de base de données.

Si vous exposez receive.php sur internet, assurez-vous que l’accès est limité à vos scripts ou IPs autorisées.

Licence

Ce projet est sous licence MIT.
