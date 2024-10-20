################
# EN # IT
################

The kmboxNet library provides an interface for programming physical keyboard and mouse input controls over the network, usable in Python environments. This guide offers an overview of how to set up and use kmboxNet for your projects.

# Introduction
kmboxNet is designed to enable Python programmers to programmatically simulate physical actions of a keyboard and mouse. Whether you're developing automations for testing or creating complex interactions for applications, kmboxNet offers the necessary tools to integrate physical controls into your software.

# Physical Installation and Initial Configuration
To use kmboxNet, you need to follow some initial steps to correctly configure the device with your PC. These steps ensure that the device is ready to communicate with your Python scripts.

# Hardware Connection
Cable Connection: Connect the two blue cables provided by the device to your PC. These cables are essential for establishing the connection between the kmboxNet device and the PC.
Input Devices Connection: Connect the mouse, keyboard, or both to the kmboxNet device according to your operational needs.
Software Configuration
The first time the device is connected to the PC, it will be recognized as a storage device. Follow these steps to configure the necessary software:

# Software Installation: Open the storage device in your file explorer and find the provided executable (e.g., setup.exe or a similar name). Run this file to install the necessary software for kmboxNet on your PC.

# Automatic Configuration: After completing the installation, start kmNet auto config to automatically configure the device. This step is crucial to ensure that the device is ready to be used with your Python scripts.

# Installation Verification
Once the software configuration is complete, the kmboxNet device is ready for use. You can begin integrating the library's functions into your Python projects to automate and control physical input devices. You can verify the installation in the command prompt using the command “ping 192.168.2.188”.

# Configuration
Before starting, make sure to copy the kmNet_xxxxx.pyd file into your project's source code directory, where xxxxx indicates the specific version and Python platform you are using.

# Requirements
Python 3.x
Windows OS (64 bit)
Installation
Rename the kmNet.cp311-win_amd64.pyd file to kmNet.pyd to match your Python environment. Ensure all cables are correctly connected before proceeding.

# Detailed Functions
Below, you'll find a detailed overview of the functions available in kmboxNet and how to use them in your Python project.

# Initialization
init(ip, port, UUID): Initializes the connection to the device. Must be called once at the beginning.

ip: Device's IP address.
port: Port number.
UUID: Unique identifier of the device.

# Mouse Control
move(x, y): Moves the mouse relative to the specified coordinates.

move_auto(x, y, duration): Moves the mouse towards the specified coordinates with a motion that simulates human action, within the time (in milliseconds) defined by duration.

move_beizer(x, y, duration, cx1, cy1, [cx2, cy2]): Moves the mouse along a specified Bézier curve through control points.

left(state): Controls the state of the left mouse button (state can be 0 for release or 1 for press).

right(state): Controls the state of the right mouse button.

middle(state): Controls the state of the middle mouse button.

wheel(direction): Simulates the movement of the mouse wheel. Positive values for scrolling up, negative for down.

# Keyboard Control
keydown(key): Simulates pressing a keyboard key.
keyup(key): Simulates releasing a keyboard key.

# Monitoring and Locking
monitor(enable): Enables or disables monitoring of the physical state of keys and mouse (enable can be 0 or 1).
isdown_left(), isdown_right(), isdown_middle(), isdown_side1(), isdown_side2(): Checks if the respective mouse button is pressed at the time of the call.

Examples of how to use the main functions:

python

# Initialization
kmNet.init('192.168.1.100', '8080', 'UNIQUE-DEVICE-UUID')

# Mouse movement
kmNet.move(100, 100)  # Immediate movement
kmNet.move_auto(1920, 1080, 200)  # Movement simulates human action

# Mouse button press and release
kmNet.left(1)  # Press
kmNet.left(0)  # Release

# Keyboard key press and release
kmNet.keydown(0x04)  # Key 'A'
kmNet.keyup(0x04)

# Monitoring and locking
kmNet.monitor(1)  # Enable monitoring
print(kmNet.isdown_left())  # Check left button state

Make sure to replace values like the IP address, port number, and UUID with those specific to your device.

## Net spoofer (New 05/09/2024)

- Load and save configuration (IP, port, and UUID) from a configuration file (`device_config.txt`).
- Prompt the user for device configuration **only on the first run** if no configuration file is found. After the first run, the configuration is handled dynamically using the file.
- Initialize the device using the provided configuration.
- Automatically generate new IP and port, configure the device, and reboot it.
- Randomize the `VID` and `PID` values for each execution.
- Print the generated `VID` and `PID` values.
- Auto close after 10s

Example Output:
- Configurazione caricata: IP = 192.168.1.100, Porta = 8080, UUID = 9FC05414
- Tentativo di connessione al dispositivo su 192.168.1.100:8080...
- KmBoxNet Inizializzato correttamente.
- Nuova configurazione generata - IP: 192.168.2.153, Porta: 32451
- Nuova configurazione di IP e Porta impostata con successo.
- Dispositivo in fase di riavvio...
- Dispositivo riavviato correttamente.
- VID randomizzato: 0x3e8f
- PID randomizzato: 0x7d52
- VID e PID impostati con successo.
- Dispositivo completamente configurato e riavviato con le nuove impostazioni.

## Kmnet auto confg.py (new 20/10/20204)
- aggiunginto controllo del ping dopo aver configurato ip di kmbox in windows consente una facile interpretazione per capire se il collegamento funziona
- added ping control after configuring ip of kmbox in windows allows easy interpretation to understand if the connection works
- aggiunta autoinstallazione del modulo pyd di kmboxnet nei moduli python (potrai importare kmboxNet nei tuoi codici senza dover avere il file pyd nella cartella del codice)
- added self-installation of the kmboxnet pyd module in python modules (you can import kmboxNet into your codes without having to have the pyd file in the code folder)

