from netmiko import ConnectHandler, NetmikoTimeoutException
import paramiko
import requests
import re
import json

# 🔹 Forcer Paramiko à accepter les anciens algos SSH
paramiko.Transport._preferred_kex = (
    'diffie-hellman-group1-sha1',
    'diffie-hellman-group14-sha1',
)
paramiko.Transport._preferred_ciphers = ('aes128-cbc', '3des-cbc', 'aes192-cbc', 'aes256-cbc')
paramiko.Transport._preferred_keys = ('ssh-rsa',)

API_URL = "https://dev.elaaria.space/api/receive.php"
TOKEN = "ce2b439378006a5556fe09cafcb53b85d1318f3d12903cefa0beb353095024a0"

# Liste des équipements (IP + credentials)
with open("devices.json") as f:
    DEVICES = json.load(f)

def mock_device(host):
    """Retourne des données simulées si l'équipement n'est pas joignable"""
    return {
        "hostname": f"MOCK-{host.replace('.', '-')}",
        "ip": host,
        "version": "Cisco IOS 15.7(3)M",
        "uptime": "N/A",
        "interfaces": [
            {"name": "GigabitEthernet0/0", "ip": "192.168.1.1", "status": "up", "protocol": "up"},
            {"name": "GigabitEthernet0/1", "ip": "unassigned", "status": "down", "protocol": "down"}
        ]
    }

for DEVICE in DEVICES:
    host = DEVICE["host"]
    print(f"\n=== Traitement de {host} ===")

    payload = {}
    try:
        # 🔹 Ajouter global_delay_factor pour vieux IOS
        DEVICE["global_delay_factor"] = 2

        net = ConnectHandler(**DEVICE)
        net.enable()  # mode enable pour commandes complètes

        # show version
        version_output = net.send_command("show version")
        print(f"\n--- show version ---\n{version_output}\n-------------------")

        hostname_match = re.search(r"(\S+) uptime", version_output)
        uptime_match = re.search(r"uptime is (.+)", version_output)
        os_version_match = re.search(r"Version ([^,]+)", version_output)

        hostname = hostname_match.group(1) if hostname_match else host
        uptime = uptime_match.group(1) if uptime_match else "N/A"
        os_version = os_version_match.group(1) if os_version_match else "N/A"

        # show ip interface brief
        interfaces_output = net.send_command("show ip interface brief")
        print(f"\n--- show ip interface brief ---\n{interfaces_output}\n-------------------")

        vlan_ip = None
        interfaces = []
        for line in interfaces_output.splitlines():
            parts = line.split()
            if len(parts) >= 6:
                iface_name = parts[0]
                ip = parts[1]
                status = parts[4]
                proto = parts[5]

                # récupérer l'IP du VLAN actif
                if iface_name.lower().startswith("vlan") and ip != "unassigned":
                    vlan_ip = ip

                interfaces.append({
                    "name": iface_name,
                    "ip": ip,
                    "status": status,
                    "protocol": proto
                })
            else:
                print(f"⚠️ Ligne ignorée (colonnes insuffisantes): {line}")

        payload = {
            "token": TOKEN,
            "hostname": hostname,
            "ip": vlan_ip if vlan_ip else host,  # IP principale = IP du VLAN si disponible
            "version": os_version,
            "uptime": uptime,
            "interfaces": interfaces
        }

        net.disconnect()
        print(f"✅ {host} récupéré avec succès.")

    except (NetmikoTimeoutException, Exception) as e:
        print(f"⚠️ Erreur Netmiko pour {host}: {e}")
        payload = mock_device(host)
        payload["token"] = TOKEN
        print(f"⚠️ {host} non joignable. Utilisation des données mockées.")

    # Envoi à l'API
    try:
        r = requests.post(API_URL, json=payload)
        print(f"{host} -> API: {r.text}")
    except Exception as e:
        print(f"❌ Erreur API pour {host}: {e}")