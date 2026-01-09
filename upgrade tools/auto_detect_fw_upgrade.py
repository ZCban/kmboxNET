import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re

URL_PAGINA = "https://www.kmbox.top/Net_firmware.html"
CARTELLA_DOWNLOAD = "firmware"
CARTELLA_NOTE = "note_firmware"

# ---------------- Utility ----------------
def normalizza_nome(filename: str) -> str:
    """Rimuove i caratteri cinesi (range Unicode CJK)"""
    return re.sub(r'[\u4e00-\u9fff]+', '', filename)

def estrai_data(filename: str) -> str:
    """Estrae sequenza di 8 cifre (YYYYMMDD) dal nome file"""
    match = re.search(r'(\d{8})', filename)
    return match.group(1) if match else None

def firmware_gia_presente(data_file: str) -> bool:
    """Controlla se nella cartella di download esiste già un file con questa data"""
    return any(data_file in f for f in os.listdir(CARTELLA_DOWNLOAD))

def scarica_file(firmware_url: str, filename_pulito: str):
    """Scarica il file .bin"""
    print(f"[*] Download in corso: {filename_pulito}")
    with requests.get(firmware_url, stream=True, headers={"User-Agent": "Mozilla/5.0"}) as fw:
        fw.raise_for_status()
        path = os.path.join(CARTELLA_DOWNLOAD, filename_pulito)
        with open(path, "wb") as f:
            for chunk in fw.iter_content(8192):
                f.write(chunk)
    print(f"[✔] Download completato: {path}\n")

def salva_note_update(soup):
    """Salva le note di aggiornamento in un file .txt solo se non esiste già"""
    os.makedirs(CARTELLA_NOTE, exist_ok=True)

    update_sec = soup.find("div", class_="net_update_detail_title")
    if not update_sec:
        print("❌ Sezione note aggiornamento non trovata")
        return

    versione_div = update_sec.find("div", class_="net_update_items")
    if not versione_div:
        print("❌ Versione firmware non trovata")
        return

    versione_testo = versione_div.get_text(strip=True)
    versione_data = re.sub(r'[^0-9]', '', versione_testo)
    if not versione_data:
        versione_data = "update_note"

    nome_file_note = f"{versione_data}.txt"
    path_note = os.path.join(CARTELLA_NOTE, nome_file_note)

    # 🔹 Salta se il file esiste già
    if os.path.exists(path_note):
        print(f"[✔] Note aggiornamento {nome_file_note} già presenti, salto\n")
        return

    # Raccogli tutte le note
    note = []
    for div in update_sec.find_all("div", class_="net_update_items"):
        testo = div.get_text(" ", strip=True)
        if testo:
            note.append(testo)

    # Scrive il file di testo
    with open(path_note, "w", encoding="utf-8") as f:
        f.write("\n".join(note))

    print(f"[✔] Note aggiornamento salvate: {path_note}\n")

# ---------------- Main ----------------
def scarica_firmware_completo():
    os.makedirs(CARTELLA_DOWNLOAD, exist_ok=True)

    print("[*] Scarico la pagina...")
    r = requests.get(URL_PAGINA, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    r.raise_for_status()
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")

    # --- Firmware più recente ---
    firmware_sec = soup.find("div", class_="net-firmware-update-sec")
    if firmware_sec:
        link = firmware_sec.find("a", href=lambda x: x and x.endswith(".bin"))
        if link:
            href = link["href"]
            firmware_url = urljoin(URL_PAGINA, href)
            filename_originale = os.path.basename(href)
            filename_pulito = normalizza_nome(filename_originale)
            data_file = estrai_data(filename_pulito)
            if data_file:
                if firmware_gia_presente(data_file):
                    print(f"[✔] Firmware recente {data_file} già presente, salto\n")
                else:
                    print(f"[+] Firmware recente trovato: {filename_originale}")
                    print(f"[+] Salvato come: {filename_pulito}")
                    scarica_file(firmware_url, filename_pulito)
            else:
                print(f"[⚠] Impossibile estrarre la data dal firmware recente {filename_originale}")

    # --- Firmware storici ---
    history_sec = soup.find("div", id="NetHistory")
    if history_sec:
        download_section = history_sec.find_next("div", class_="net_download_detail_sec")
        if download_section:
            links = download_section.find_all("a", href=lambda x: x and x.endswith(".bin"))
            for link in links:
                href = link["href"]
                firmware_url = urljoin(URL_PAGINA, href)
                filename_originale = os.path.basename(href)
                filename_pulito = normalizza_nome(filename_originale)
                data_file = estrai_data(filename_pulito)
                if not data_file:
                    print(f"[⚠] Impossibile estrarre la data dal firmware storico {filename_originale}, salto")
                    continue
                if firmware_gia_presente(data_file):
                    print(f"[✔] Firmware storico {data_file} già presente, salto")
                    continue
                print(f"[+] Firmware storico trovato: {filename_originale}")
                print(f"[+] Salvato come: {filename_pulito}")
                scarica_file(firmware_url, filename_pulito)

    # --- Salva note aggiornamento solo se non presenti ---
    salva_note_update(soup)

# ---------------- Esecuzione ----------------
if __name__ == "__main__":
    scarica_firmware_completo()

