# Network Monitoring Script

[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)  [![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)  [![forthebadge](http://forthebadge.com/images/badges/uses-html.svg)](http://forthebadge.com)

Un script simple et efficace pour surveiller vos appareils réseau et leurs interfaces, avec collecte via Python, stockage en MySQL et affichage via PHP.

---

## Pour commencer

Ce projet vous permet de récupérer automatiquement les informations de vos appareils réseau et de leurs interfaces. Vous pouvez ensuite visualiser toutes les données depuis un navigateur.  

---

### Pré-requis

Avant de commencer, vous aurez besoin de :  

- PHP ≥ 7.4  
- Python ≥ 3.8  
- Serveur web (Apache, Nginx…)  
- Base de données MySQL ≥ 5.7  
- Accès SSH sur vos appareils réseau (pour la collecte via Python)  

---

### Installation

1. **Base de données**

   Créez la base et les tables nécessaires :

   ```sql
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

## Fichiers PHP

- Placez `receive.php` dans le dossier `/api` de votre hébergement.
- Configurez `config.php` à la racine pour la connexion MySQL :

```php
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
## Tokens de sécurité

- Mettez à jour les tokens dans vos fichiers PHP et Python.
- Pour générer un token sécurisé :

```bash
openssl rand -hex 32
Script Python

Installez les dépendances nécessaires :

pip install -r requirements.txt

Configurez vos appareils réseau et le chemin vers /api/receive.php pour l’envoi des données.

Visualisation

Ouvrez index.php dans un navigateur pour voir toutes les informations en temps réel.

Démarrage

Pour lancer le projet :

Assurez-vous que votre serveur web et MySQL fonctionnent.

Exécutez le script Python pour envoyer les données à votre endpoint PHP.

Accédez à index.php pour visualiser vos appareils et interfaces.

Structure des fichiers
/ (racine)
├─ config.php       # Configuration base de données
├─ index.php        # Affichage des données
└─ /api
   └─ receive.php   # Endpoint pour recevoir les données
Fabriqué avec

PHP - Langage côté serveur

Python - Langage pour la collecte des données

MySQL - Base de données

TailwindCSS - Pour styliser l’interface (optionnel)

Visual Studio Code - Éditeur recommandé

Contributing

Si vous souhaitez contribuer :

Fork le projet

Créez une branche pour vos modifications

Envoyez un pull request

Versions

Dernière version stable : 1.0
Liste des versions : Cliquer pour afficher

Auteurs

Steven Prit alias @stevenprit

Consultez la liste des contributeurs
 pour voir qui a aidé au projet !

License

Ce projet est sous licence MIT - voir le fichier LICENSE.md
 pour plus d’informations.
