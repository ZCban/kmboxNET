#include <string>
#include <fstream>
#include <random>
#include <chrono>
#include <thread>
#include "NetConfig/kmboxNet.h"
#include <iostream>

const std::string configFileName = "device_config.txt";

void saveConfig(const std::string& ip, int port, const std::string& uuid) {
    std::ofstream configFile(configFileName);
    if (configFile.is_open()) {
        configFile << ip << std::endl;
        configFile << port << std::endl;
        configFile << uuid << std::endl;
        configFile.close();
        std::cout << "Configurazione salvata: IP = " << ip << ", Porta = " << port << ", UUID = " << uuid << std::endl;
    }
    else {
        std::cout << "Impossibile aprire il file per salvare la configurazione." << std::endl;
    }
}

bool loadConfig(std::string& ip, int& port, std::string& uuid) {
    std::ifstream configFile(configFileName);
    if (configFile.is_open()) {
        if (getline(configFile, ip) && (configFile >> port) && getline(configFile >> std::ws, uuid)) {
            configFile.close();
            std::cout << "Configurazione caricata: IP = " << ip << ", Porta = " << port << ", UUID = " << uuid << std::endl;
            return true;
        }
        configFile.close();
    }
    std::cout << "Caricamento configurazione fallito. Inserisci i dati manualmente." << std::endl;
    return false;
}

bool initializeAndConfigureDevice(const std::string& deviceIP, int devicePort, const std::string& uuid) {
    std::cout << "Tentativo di connessione al dispositivo su " << deviceIP << ":" << devicePort << "..." << std::endl;

    char* ipBuffer = new char[deviceIP.length() + 1];
    std::strcpy(ipBuffer, deviceIP.c_str());

    std::string portStr = std::to_string(devicePort);
    char* portBuffer = new char[portStr.length() + 1];
    std::strcpy(portBuffer, portStr.c_str());

    char* uuidBuffer = new char[uuid.length() + 1];
    std::strcpy(uuidBuffer, uuid.c_str());

    if (kmNet_init(ipBuffer, portBuffer, uuidBuffer) != 0) {
        std::cout << "KmBoxNet Inizializzazione fallita." << std::endl;
        delete[] ipBuffer;
        delete[] portBuffer;
        delete[] uuidBuffer;
        return false;
    }

    delete[] ipBuffer;
    delete[] portBuffer;
    delete[] uuidBuffer;

    std::cout << "KmBoxNet Inizializzato correttamente." << std::endl;
    return true;
}

bool setDeviceVIDPID(unsigned short vid, unsigned short pid) {
    int result = kmNet_setvidpid(vid, pid);
    if (result != 0) {
        std::cout << "Impossibile impostare VID e PID. Codice errore: " << result << std::endl;
        return false;
    }

    std::cout << "VID e PID impostati con successo." << std::endl;
    return true;
}

bool configureAndRebootDevice(std::string& newIP, int& newPort) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> ipDistrib(150, 199);
    std::uniform_int_distribution<> portDistrib(1024, 65535);

    newIP = "192.168.2." + std::to_string(ipDistrib(gen));
    newPort = portDistrib(gen);
    std::cout << "Nuova configurazione generata - IP: " << newIP << ", Porta: " << newPort << std::endl;

    char* newIPBuffer = new char[newIP.length() + 1];
    std::strcpy(newIPBuffer, newIP.c_str());

    if (kmNet_setconfig(newIPBuffer, static_cast<unsigned short>(newPort)) != 0) {
        std::cout << "Impossibile impostare la nuova configurazione di IP e Porta." << std::endl;
        delete[] newIPBuffer;
        return false;
    }

    delete[] newIPBuffer;

    std::cout << "Nuova configurazione di IP e Porta impostata con successo." << std::endl;

    saveConfig(newIP, newPort, "9FC05414"); // Salva la configurazione con un UUID esistente o nuovo

    if (kmNet_reboot() != 0) {
        std::cout << "Impossibile riavviare il dispositivo." << std::endl;
        return false;
    }

    std::cout << "Dispositivo in fase di riavvio..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(5)); // Attendere che il dispositivo si riavvii
    std::cout << "Dispositivo riavviato correttamente." << std::endl;

    return true;
}

int main() {
    std::string deviceIP;
    int devicePort;
    std::string deviceUUID;

    // 1. Caricare o chiedere all'utente la configurazione del dispositivo
    if (!loadConfig(deviceIP, devicePort, deviceUUID)) {
        std::cout << "Inserisci l'IP del dispositivo: ";
        std::cin >> deviceIP;
        std::cout << "Inserisci la porta del dispositivo: ";
        std::cin >> devicePort;
        std::cout << "Inserisci il codice UUID (autorizzazione): ";
        std::cin >> deviceUUID;
    }

    // 2. Inizializzare il dispositivo
    if (!initializeAndConfigureDevice(deviceIP, devicePort, deviceUUID)) {
        return 1; // Uscita in caso di fallimento nell'inizializzazione
    }

    // 3. Configurare nuovo IP, Porta e riavviare il dispositivo
    std::string newIP;
    int newPort;
    if (!configureAndRebootDevice(newIP, newPort)) {
        return 1; // Uscita in caso di fallimento nella configurazione
    }

    // 4. Re-inizializzare il dispositivo con la nuova configurazione
    if (!initializeAndConfigureDevice(newIP, newPort, deviceUUID)) {
        return 1; // Uscita in caso di fallimento nella re-inizializzazione
    }

    // 4.5 Wait for the device to be fully ready
    std::cout << "Waiting for the device to be fully ready..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(3)); // Wait a few seconds

    // 5. Impostare il VID e PID randomizzati
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<unsigned short> distrib(0x0000, 0xFFFF); // Genera un valore tra 0x0000 e 0xFFFF

    unsigned short vid = distrib(gen); // Randomizza il Vendor ID (VID)
    unsigned short pid = distrib(gen); // Randomizza il Product ID (PID)

    std::cout << "New VID:" << std::hex << vid << std::endl;
    std::cout << "New PID:" << std::hex << pid << std::endl;

    if (!setDeviceVIDPID(vid, pid)) {
        return 1; // Uscita in caso di fallimento nell'impostazione di VID e PID
    }

    std::cout << "Dispositivo completamente configurato e riavviato con le nuove impostazioni." << std::endl;

    // Wait 10 seconds before the program exits automatically
    std::cout << "Il programma si chiuderà automaticamente in 10 secondi." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(10));
    return 0;
}
