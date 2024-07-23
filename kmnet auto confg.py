import subprocess
import os
import time
import ctypes
from ctypes import wintypes
import win32com.client

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
        EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW

        titles = []

        def foreach_window(hwnd, lParam):
            if ctypes.windll.user32.IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
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

    def install_driver(self):
        if self.is_driver_installed():
            print(f"Il driver {self.driver_name} è già installato.")
        else:
            print(f"Il driver {self.driver_name} non è installato. Cerco il file {self.exe_name}...")
            if self.search_and_run_exe():
                print(f"Avviato il file {self.exe_name}.")
                while True:
                    open_windows = self.list_open_windows()
                    if any(self.main_window_name in window for hwnd, window in open_windows):
                        print(f"La finestra '{self.main_window_name}' è aperta. Premo Invio...")
                        self.press_enter()
                        break
                    time.sleep(1)

                while True:
                    open_windows = self.list_open_windows()
                    driver_setup_windows = [window for hwnd, window in open_windows if self.main_window_name in window]
                    if len(driver_setup_windows) >= 2:
                        print(f"Sono aperte due finestre '{self.main_window_name}'. Le chiudo tutte...")
                        self.close_windows_with_title(self.main_window_name)
                        break
                    else:
                        print(f"In attesa che si apra la seconda finestra '{self.main_window_name}'...")
                    time.sleep(1)

                if self.is_driver_installed():
                    print(f"Il driver {self.driver_name} è stato installato correttamente.")
                else:
                    print(f"Il driver {self.driver_name} non è stato installato correttamente.")
            else:
                print(f"Il file {self.exe_name} non è stato trovato sul disco C:.")


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

# Utilizzo delle classi
driver_installer = DriverInstaller("WCHUSBNIC.INF", "WCHUSBNIC.EXE", "DriverSetup")
driver_installer.install_driver()

network_configurator = NetworkConfigurator()
network_configurator.list_ethernet_devices()
interface_name = network_configurator.get_interface_name("USB 2.0 Ethernet Adapter")
if interface_name:
    network_configurator.set_static_ip(interface_name, "192.168.2.187", "255.255.255.0")


