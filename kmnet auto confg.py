import subprocess

def list_ethernet_devices():
    # Comando per elencare le interfacce di rete
    command = "netsh interface ipv4 show interfaces"
    try:
        # Esecuzione del comando
        output = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Stampa dell'output
        print("Elenco delle interfacce di rete disponibili:")
        print(output.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Errore nell'elencare le interfacce di rete: {e}")

# Nome dell'interfaccia come appare in Windows, ad esempio "Ethernet 2"
interface_name = "Ethernet 2"

# Indirizzo IP da assegnare
ip_address = "192.168.2.187"

# Subnet mask
subnet_mask = "255.255.255.0"

# Gateway predefinito
#gateway = "192.168.1.1"

# Prima stampa la lista dei dispositivi Ethernet
list_ethernet_devices()

# Costruzione del comando per impostare l'indirizzo IP statico
command = f"netsh interface ipv4 set address name=\"{interface_name}\" static {ip_address} {subnet_mask} "

# Esecuzione del comando per impostare l'indirizzo IP
try:
    subprocess.run(command, check=True, shell=True)
    print(f"Indirizzo IP {ip_address} impostato con successo su {interface_name}.")
except subprocess.CalledProcessError as e:
    print(f"Errore nell'impostazione dell'indirizzo IP: {e}")
