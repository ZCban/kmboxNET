import subprocess
import os
import time
import ctypes
from ctypes import wintypes
import win32com.client
import random
import sys
import os
import shutil
import site


class InstallationModule:
    def __init__(self):
        self.version = sys.version_info
        self.version_str = f"cp{self.version.major}{self.version.minor}"
        self.site_packages = site.getsitepackages()
        if not self.site_packages or len(self.site_packages) < 2:
            raise ValueError("Impossibile trovare la directory dei moduli di Python.")
        self.target_folder = self.site_packages[1]  # Usa il secondo percorso (Lib/site-packages)

        if not os.path.exists(self.target_folder):
            raise ValueError("Impossibile trovare la directory dei moduli di Python.")

    def execute(self):
        print(self.get_python_version())
        print(site.getsitepackages())
        self.find_and_copy_pyd_file()

    def get_python_version(self):
        return f"Python {self.version.major}.{self.version.minor}"

    def find_and_copy_pyd_file(self):
        # Percorsi di ricerca nella root di ciascuna unità
        search_drives = ["C:\\", "D:\\", "E:\\"]  # Drive separati

        pyd_folder = None
        for drive in search_drives:
            for root, dirs, files in os.walk(drive):
                if 'PYD' in dirs:
                    pyd_folder = os.path.join(root, 'PYD')
                    break
            if pyd_folder:
                break  # Se ha trovato la cartella, interrompe la ricerca

        if not pyd_folder:
            print("Cartella 'PYD' non trovata.")
            return

        print(f"Cercando i file .pyd nella cartella: {pyd_folder}")
        found_files = []
        for file_name in os.listdir(pyd_folder):
            if file_name.endswith(".pyd"):
                found_files.append(file_name)
                if self.version_str in file_name:
                    source_file = os.path.join(pyd_folder, file_name)
                    destination_file = os.path.join(self.target_folder, file_name)
                    renamed_file = os.path.join(self.target_folder, "kmNet.pyd")
                    try:
                        # Rimuove eventuali file esistenti
                        if os.path.exists(destination_file):
                            os.remove(destination_file)
                        if os.path.exists(renamed_file):
                            os.remove(renamed_file)

                        # Copia e rinomina il file
                        shutil.copy(source_file, destination_file)
                        os.rename(destination_file, renamed_file)
                        print(f"File '{file_name}' copiato e rinominato in '{renamed_file}'.")
                        return
                    except Exception as e:
                        print(f"Errore durante la copia o la rinomina del file: {e}")
                        return

        print("File trovati:", found_files)
        print("Nessun file .pyd corrispondente alla versione di Python trovato.")




class NetworkConfigurator:
    def list_ethernet_devices(self):
        command = "netsh interface ipv4 show interfaces"
        try:
            output = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            #print("Elenco delle interfacce di rete disponibili:")
            #print(output.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Errore nell'elencare le interfacce di rete: {e}")

    def get_interface_name(self, description):
        try:
            wmi = win32com.client.GetObject("winmgmts:")
            adapters = wmi.InstancesOf("Win32_NetworkAdapter")
            for adapter in adapters:
                if description in adapter.Description:
                    return adapter.NetConnectionID
            print(f"Nessuna interfaccia trovata con la descrizione '{description}'")
            return None
        except Exception as e:
            print(f"Errore nell'interrogare WMI: {e}")
            return None

    def set_static_ip(self, interface_name, ip_address, subnet_mask):
        command = f"netsh interface ipv4 set address name=\"{interface_name}\" static {ip_address} {subnet_mask}"
        try:
            subprocess.run(command, check=True, shell=True)
            print(f"Indirizzo IP {ip_address} impostato con successo su {interface_name}.")
            print('Configurazione Pronta')
        except subprocess.CalledProcessError as e:
            print(f"Errore nell'impostazione dell'indirizzo IP: {e}")

    def ping_ip(self, ip_address):
        command = f"ping {ip_address}"
        try:
            output = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if "TTL=" in output.stdout:
                print(f"Ping verso {ip_address} riuscito.")
            else:
                print(f"Ping verso {ip_address} fallito.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante il ping dell'indirizzo IP {ip_address}: {e}")

import os
import subprocess
import time
import pyautogui
import pygetwindow as gw

class DriverInstaller:
    def __init__(self, folder_name="upgrade_tools"):
        self.folder_name = folder_name
        self.driver_folder = self.find_folder(folder_name)
        if not self.driver_folder:
            raise FileNotFoundError(f"❌ Cartella {folder_name} non trovata")
        print(f"✅ Cartella trovata: {self.driver_folder}")

    # --- Funzioni di utilità ---
    def find_folder(self, folder_name, start_path="C:\\"):
        """Trova la cartella ricorsivamente"""
        for root, dirs, files in os.walk(start_path):
            if folder_name in dirs:
                return os.path.join(root, folder_name)
        return None

    def bring_window_to_front(self, title):
        """Porta la finestra con il titolo specifico in primo piano"""
        windows = gw.getWindowsWithTitle(title)
        if windows:
            windows[0].activate()
            return True
        return False

    def close_window(self, title):
        """Chiude la finestra con il titolo specifico"""
        windows = gw.getWindowsWithTitle(title)
        if windows:
            for w in windows:
                w.close()
            return True
        return False

    # --- Metodi principali ---
    def uninstall_driver_gui(self):
        """Avvia l'exe e automatizza la GUI per disinstallare"""
        setup_exe = os.path.join(self.driver_folder, "WCHUSBNIC.EXE")
        if not os.path.exists(setup_exe):
            print("❌ SETUP.exe non trovato")
            return

        print(f"✅ Avvio SETUP.exe da: {setup_exe}")
        proc = subprocess.Popen([setup_exe])

        time.sleep(2)

        window_title = "DriverSetup(X64)"
        brought = self.bring_window_to_front(window_title)
        if not brought:
            print("⚠️ Non sono riuscito a portare la finestra in primo piano. Continua comunque...")

        time.sleep(1)

        pyautogui.press('tab', presses=1, interval=0.5)
        pyautogui.press('enter')
        print("✅ Comando di Uninstall inviato")

        proc.wait()
        print("✅ Disinstallazione completata")


        # Elimina i file residui .sys e .cat se presenti
        residual_files = ["WCHUSBNIC.sys", "WCHUSBNICA64.sys", "WCHUSBNIC.CAT"]
        for f in residual_files:
            file_path = os.path.join(self.driver_folder, f)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"✅ Eliminato file residuo: {file_path}")
                except Exception as e:
                    print(f"⚠️ Impossibile eliminare {file_path}: {e}")
            else:
                print(f"ℹ️ File non trovato (saltato): {file_path}")

        # Aspetta e chiudi la finestra 'DriverSetup'
        print("⌛ Attendo la comparsa della finestra 'DriverSetup' per chiuderla...")
        while True:
            time.sleep(1)
            if self.close_window("DriverSetup"):
                print("✅ Finestra 'DriverSetup' chiusa correttamente")
                break

    def install_driver_gui(self):
        """Avvia l'exe e automatizza la GUI per installare"""
        setup_exe = os.path.join(self.driver_folder, "WCHUSBNIC.EXE")
        if not os.path.exists(setup_exe):
            print("❌ SETUP.exe non trovato")
            return

        print(f"✅ Avvio SETUP.exe da: {setup_exe}")
        proc = subprocess.Popen([setup_exe])

        time.sleep(2)

        window_title = "DriverSetup(X64)"
        brought = self.bring_window_to_front(window_title)
        if not brought:
            print("⚠️ Non sono riuscito a portare la finestra in primo piano. Continua comunque...")

        time.sleep(1)
        pyautogui.press('enter')
        print("✅ Comando di Install inviato")

        proc.wait()
        print("✅ Installazione completata")

        # Aspetta e chiudi la finestra 'DriverSetup'
        print("⌛ Attendo la comparsa della finestra 'DriverSetup' per chiuderla...")
        while True:
            time.sleep(2)
            if self.close_window("DriverSetup"):
                print("✅ Finestra 'DriverSetup' chiusa correttamente")
                break


# --- Main ---
installer = DriverInstaller()
installer.uninstall_driver_gui()
installer.install_driver_gui()


# installa modulo
try:
    handler = InstallationModule()
    handler.execute()
    print('Modulo kmNet installato con successo in python')
except ValueError as e:
    print(e)

# configura rete di comunicazione
network_configurator = NetworkConfigurator()
network_configurator.list_ethernet_devices()
interface_name = network_configurator.get_interface_name("USB2.0 Ethernet Adapter")
if not  interface_name:
    interface_name = network_configurator.get_interface_name("USB 2.0 Ethernet Adapter")
if interface_name:
    random_ip = f"192.168.2.{random.randint(200, 240)}"
    network_configurator.set_static_ip(interface_name, random_ip, "255.255.255.0")
    print('verifico connessione,attendere')
    network_configurator.ping_ip(random_ip)
time.sleep(2)



