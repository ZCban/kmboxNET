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
        # Percorso di ricerca nella cartella 'C:\' per la cartella 'PYD'
        search_path = "C:"
        pyd_folder = None
        for root, dirs, files in os.walk(search_path):
            if 'PYD' in dirs:
                pyd_folder = os.path.join(root, 'PYD')
                break

        if not pyd_folder:
            print("Cartella 'PYD' non trovata.")
            return

        # Cerca il file .pyd per la versione corretta di Python
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
                        # Rimuove eventuali moduli esistenti con lo stesso nome
                        if os.path.exists(destination_file):
                            os.remove(destination_file)
                        if os.path.exists(renamed_file):
                            os.remove(renamed_file)

                        # Copia il file e lo rinomina
                        shutil.copy(source_file, destination_file)
                        os.rename(destination_file, renamed_file)
                        print(f"File '{file_name}' copiato con successo e rinominato in '{renamed_file}'.")
                        return
                    except Exception as e:
                        print(f"Errore durante la copia o la rinomina del file: {e}")
                        return

        print("File trovati:", found_files)
        print("Nessun file .pyd corrispondente alla versione di Python trovato.")




class DriverInstaller:
    def __init__(self, driver_name, exe_name, main_window_name):
        self.driver_name = driver_name
        self.exe_name = exe_name
        self.main_window_name = main_window_name

    def is_driver_installed(self):
        try:
            result = subprocess.run(['powershell', '-Command', 'Get-WindowsDriver -Online'], capture_output=True, text=True, check=True)
            output = result.stdout
            return self.driver_name.lower() in output.lower()
        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'esecuzione del comando: {e}")
            return False

    def search_and_run_exe(self):
        for root, dirs, files in os.walk("C:\\"):
            if self.exe_name in files:
                exe_path = os.path.join(root, self.exe_name)
                try:
                    subprocess.Popen([exe_path])
                    return True
                except Exception as e:
                    print(f"Errore durante l'avvio del file {self.exe_name}: {e}")
                    return False
        return False

    def press_enter(self):
        VK_RETURN = 0x0D
        KEYEVENTF_KEYUP = 0x0002
        ctypes.windll.user32.keybd_event(VK_RETURN, 0, 0, 0)
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)

    def list_open_windows(self):
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW

        titles = []

        def foreach_window(hwnd, lParam):
            if ctypes.windll.user32.IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    GetWindowText(hwnd, buff, length + 1)
                    if buff.value:
                        titles.append((hwnd, buff.value))
            return True

        EnumWindows(EnumWindowsProc(foreach_window), 0)
        return titles

    def close_windows_with_title(self, title):
        for hwnd, window_title in self.list_open_windows():
            if title.lower() in window_title.lower():
                ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)

    def bring_window_to_foreground(self, hwnd):
        """Mettere la finestra in primo piano"""
        try:
            # Ripristinare la finestra se è minimizzata
            if ctypes.windll.user32.IsIconic(hwnd):
                ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE = 9
            
            # Portare la finestra in primo piano
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            time.sleep(0.2)
            
        except Exception as e:
            print(f"Errore nel mettere la finestra in primo piano: {e}")

    def install_driver(self):
        if self.search_and_run_exe():
            print(f"Avviato il file {self.exe_name}.")
            
            # Attesa per la prima finestra con timeout
            start_time = time.time()
            timeout = 60  # 60 secondi di timeout
            
            while time.time() - start_time < timeout:
                open_windows = self.list_open_windows()
                main_window_found = False
                main_hwnd = None
                
                # Cerca la finestra principale e ottieni il suo handle
                for hwnd, window in open_windows:
                    if self.main_window_name in window:
                        main_window_found = True
                        main_hwnd = hwnd
                        break
                
                if main_window_found:
                    print(f"La finestra '{self.main_window_name}' è aperta. Metto in primo piano e premo Invio...")
                    
                    # Mettere la finestra in primo piano
                    self.bring_window_to_foreground(main_hwnd)
                    time.sleep(0.5)
                    
                    # Premere Invio due volte
                    self.press_enter()
                    time.sleep(0.5)
                    self.press_enter()
                    break
                    
                time.sleep(1)
            else:
                print(f"Timeout: finestra '{self.main_window_name}' non trovata entro {timeout} secondi")
                return False

            # Attesa per la seconda finestra (completamento installazione) con timeout
            start_time = time.time()
            timeout = 300  # 5 minuti di timeout
            
            while time.time() - start_time < timeout:
                open_windows = self.list_open_windows()
                driver_setup_windows = [window for hwnd, window in open_windows if self.main_window_name in window]
                
                if len(driver_setup_windows) >= 2:
                    print(f"Sono aperte due finestre '{self.main_window_name}'. Le chiudo tutte...")
                    self.close_windows_with_title(self.main_window_name)
                    time.sleep(2)  # Attendi che le finestre vengano chiuse
                    break
                else:
                    print(f"In attesa che si apra la seconda finestra '{self.main_window_name}'...")
                time.sleep(2)
            else:
                print(f"Timeout: installazione non completata entro {timeout} secondi")
                return False

            # Verifica installazione
            time.sleep(1)  # Attendi ulteriormente per assicurarsi che l'installazione sia completa
            if self.is_driver_installed():
                print(f"Il driver {self.driver_name} è stato installato correttamente.")
                return True
            else:
                print(f"Il driver {self.driver_name} non è stato installato correttamente.")
                return False
        else:
            print(f"Il file {self.exe_name} non è stato trovato sul disco C:.")
            return False

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

# installa driver
driver_installer = DriverInstaller("WCHUSBNIC.INF", "WCHUSBNIC.EXE", "DriverSetup")
driver_installer.install_driver()

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
