# Network Monitoring Script

[![Built with Love](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com) 
[![Powered by Electricity](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com) 
[![Uses HTML](http://forthebadge.com/images/badges/uses-html.svg)](http://forthebadge.com)

Ce projet permet de surveiller vos appareils réseau et leurs interfaces avec Python, stocker les données dans MySQL et les afficher via PHP.

---

<details>
<summary>Introduction</summary>

Ce script récupère automatiquement les informations de vos appareils réseau et de leurs interfaces. Vous pouvez ensuite visualiser toutes les données depuis un navigateur.
</details>

<details>
<summary>Pré-requis</summary>

- PHP ≥ 7.4  
- Python ≥ 3.8  
- Serveur web (Apache, Nginx)  
- Base de données MySQL ≥ 5.7  
- Accès SSH sur vos appareils réseau
</details>

<details>
<summary>Installation</summary>

### Base de données

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
```

### Fichiers PHP

- Placez `receive.php` dans le dossier `/api`  
- Configurez `config.php` :

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
```

### Tokens de sécurité

```bash
openssl rand -hex 32
```

### Script Python

```bash
pip install -r requirements.txt
```

Configurez vos appareils réseau et le chemin vers `/api/receive.php` pour l’envoi des données.

### Visualisation

Ouvrez `index.php` dans votre navigateur pour visualiser les données.
</details>

<details>
<summary>Démarrage</summary>

1. Assurez-vous que votre serveur web et MySQL fonctionnent.  
2. Exécutez le script Python pour envoyer les données.  
3. Accédez à `index.php` pour voir les informations en temps réel.
</details>

<details>
<summary>Structure des fichiers</summary>

```
/ (racine)
- config.php       # Configuration base de données
- index.php        # Affichage des données
- /api
  - receive.php    # Endpoint pour recevoir les données
```
</details>

<details>
<summary>Fabriqué avec</summary>

| Technologie       | Rôle |
|------------------|--------------------------------|
| PHP               | Langage côté serveur |
| Python            | Collecte des données |
| MySQL             | Base de données |
| TailwindCSS       | Stylisation interface (optionnel) |
| Visual Studio Code| Éditeur recommandé |
</details>

<details>
<summary>Contributing</summary>

1. Fork le projet  
2. Créez une branche pour vos modifications  
3. Envoyez un Pull Request
</details>

<details>
<summary>Versions</summary>

- Dernière version stable : 1.0  
- Liste des versions : voir le changelog
</details>

<details>
<summary>Auteurs</summary>

**Steven Prit** alias `@stevenprit`  
Consultez la liste des contributeurs pour voir qui a aidé au projet.
</details>

<details>
<summary>License</summary>

Ce projet est sous licence **MIT** – voir le fichier `LICENSE.md`.
</details>
