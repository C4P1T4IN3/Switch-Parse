<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

require_once __DIR__ . '/config.php';

$conn = new mysqli($db_host, $db_user, $db_pass, $db_name);
if ($conn->connect_error) {
    die("Erreur BDD : " . $conn->connect_error);
}

// Récupérer les équipements pour le filtre
$devicesList = $conn->query("SELECT id, hostname FROM devices ORDER BY hostname");

// Filtre sélectionné
$filter = isset($_GET['device']) ? (int)$_GET['device'] : 0;

// Requête principale
$sql = "SELECT * FROM devices";
if ($filter > 0) {
    $sql .= " WHERE id = $filter";
}
$sql .= " ORDER BY created_at DESC";

$res = $conn->query($sql);
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Network Monitoring</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">

<div class="container my-5">
    <h1 class="mb-4">📡 Network Monitoring</h1>

    <!-- FILTRE -->
    <form method="get" class="mb-4">
        <label class="form-label">Filtrer par équipement :</label>
        <select name="device" class="form-select" onchange="this.form.submit()">
            <option value="0">Tous les équipements</option>
            <?php while ($d = $devicesList->fetch_assoc()): ?>
                <option value="<?= $d['id'] ?>" <?= $filter == $d['id'] ? 'selected' : '' ?>>
                    <?= htmlspecialchars($d['hostname']) ?>
                </option>
            <?php endwhile; ?>
        </select>
    </form>

    <?php if ($res->num_rows === 0): ?>
        <div class="alert alert-warning">Aucun équipement trouvé.</div>
    <?php endif; ?>

    <?php while ($device = $res->fetch_assoc()): ?>
        <div class="card mb-4 shadow-sm">
            <div class="card-body">
                <h4 class="card-title">
                    <?= htmlspecialchars($device['hostname']) ?>
                    <small class="text-muted">(<?= $device['ip_address'] ?>)</small>
                </h4>

                <p class="mb-1"><strong>Version :</strong> <?= $device['os_version'] ?></p>
                <p class="mb-1"><strong>Uptime :</strong> <?= $device['uptime'] ?></p>
                <p class="text-muted">
                    <strong>Dernière collecte :</strong>
                    <?= date("d/m/Y H:i:s", strtotime($device['created_at'])) ?>
                </p>

                <?php
                $ints = $conn->query(
                    "SELECT * FROM interfaces WHERE device_id=" . (int)$device['id']
                );
                ?>

                <table class="table table-bordered table-sm mt-3">
                    <thead class="table-dark">
                        <tr>
                            <th>Interface</th>
                            <th>IP</th>
                            <th>Status</th>
                            <th>Protocol</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php while ($i = $ints->fetch_assoc()): ?>
                            <?php
                            $statusClass = ($i['status'] === 'up') ? 'text-success fw-bold' : 'text-danger fw-bold';
                            $protoClass  = ($i['protocol'] === 'up') ? 'text-success' : 'text-danger';
                            ?>
                            <tr>
                                <td><?= $i['interface_name'] ?></td>
                                <td><?= $i['ip_address'] ?></td>
                                <td class="<?= $statusClass ?>"><?= strtoupper($i['status']) ?></td>
                                <td class="<?= $protoClass ?>"><?= strtoupper($i['protocol']) ?></td>
                            </tr>
                        <?php endwhile; ?>
                    </tbody>
                </table>
            </div>
        </div>
    <?php endwhile; ?>

</div>

</body>
</html>