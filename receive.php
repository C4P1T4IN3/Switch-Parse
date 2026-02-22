<?php
// DEBUG (à enlever en prod)
ini_set('display_errors', 1);
error_reporting(E_ALL);

// Connexion BDD
require_once __DIR__ . '/../config.php';

$conn = new mysqli($db_host, $db_user, $db_pass, $db_name);
if ($conn->connect_error) {
    http_response_code(500);
    exit("DB Error");
}

// Lire le JSON
$data = json_decode(file_get_contents("php://input"), true);
if (!$data) {
    http_response_code(400);
    exit("Invalid JSON");
}

// Sécurité par token
$API_TOKEN = "VOTRETOKENICI";

if (!isset($data['token']) || $data['token'] !== $API_TOKEN) {
    http_response_code(403);
    exit("Forbidden");
}

// Insertion device
$stmt = $conn->prepare(
    "INSERT INTO devices (hostname, ip_address, os_version, uptime)
     VALUES (?,?,?,?)"
);
$stmt->bind_param(
    "ssss",
    $data['hostname'],
    $data['ip'],
    $data['version'],
    $data['uptime']
);
$stmt->execute();

$device_id = $stmt->insert_id;

// Insertion interfaces
foreach ($data['interfaces'] as $int) {
    $stmt = $conn->prepare(
        "INSERT INTO interfaces
        (device_id, interface_name, status, protocol, ip_address)
        VALUES (?,?,?,?,?)"
    );
    $stmt->bind_param(
        "issss",
        $device_id,
        $int['name'],
        $int['status'],
        $int['protocol'],
        $int['ip']
    );
    $stmt->execute();
}

echo "OK";