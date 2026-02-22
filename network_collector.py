from netmiko import ConnectHandler, NetmikoTimeoutException
import requests
import re
import json

API_URL = "https://votresite.fr/api/receive.php"
TOKEN = "votretoken"

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
        net = ConnectHandler(**DEVICE)
        # show version
        version_output = net.send_command("show version")
        hostname = re.search(r"(\S+) uptime", version_output)
        uptime = re.search(r"uptime is (.+)", version_output)
        os_version = re.search(r"Version ([^,]+)", version_output)

        hostname = hostname.group(1) if hostname else host
        uptime = uptime.group(1) if uptime else "N/A"
        os_version = os_version.group(1) if os_version else "N/A"

        # show ip interface brief
        interfaces_output = net.send_command("show ip interface brief")
        interfaces = []
        for line in interfaces_output.splitlines():
            if "Ethernet" in line or "Gigabit" in line:
                parts = line.split()
                if len(parts) >= 6:
                    interfaces.append({
                        "name": parts[0],
                        "ip": parts[1],
                        "status": parts[4],
                        "protocol": parts[5]
                    })

        payload = {
            "token": TOKEN,
            "hostname": hostname,
            "ip": host,
            "version": os_version,
            "uptime": uptime,
            "interfaces": interfaces
        }
        net.disconnect()
        print(f"✅ {host} récupéré avec succès.")

    except (NetmikoTimeoutException, Exception) as e:
        # Si l'équipement n'est pas joignable → mock
        payload = mock_device(host)
        payload["token"] = TOKEN
        print(f"⚠️ {host} non joignable. Utilisation des données mockées.")

    # Envoi à l'API
    try:
        r = requests.post(API_URL, json=payload)
        print(f"{host} -> API: {r.text}")
    except Exception as e:
        print(f"❌ Erreur API pour {host}: {e}")