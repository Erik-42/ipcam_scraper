import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

# URL de base de la caméra
BASE_URL = "http://192.168.0.234"
DUMP_DIR = "dump"
LOG_FILE = "log.txt"

# Chargement des wordlists
with open("wordlist.txt", "r") as f:
    WORDLIST = [line.strip() for line in f if line.strip()]
with open("paths.txt", "r") as f:
    DEFAULT_PATHS = [line.strip() for line in f if line.strip()]

# Pour éviter les doublons
visited_urls = set()

# Initialisation du log
def log_info(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}"
    print(full_message)
    with open(LOG_FILE, "a") as log:
        log.write(full_message + "\n")

# Sauvegarde d’un fichier
def save_file(url, content):
    path = urlparse(url).path.lstrip("/")
    local_path = os.path.join(DUMP_DIR, path)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(content)
    log_info(f"[✓] Fichier sauvegardé: {local_path}")

# Téléchargement et parsing HTML
def fetch_html(url):
    try:
        response = requests.get(url, timeout=5)
        if "text/html" in response.headers.get("Content-Type", ""):
            save_file(url, response.content)
            return response.text
    except Exception as e:
        log_info(f"[!] Erreur lors du chargement de {url}: {e}")
    return None

# Exploration automatique depuis le HTML
def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    found = set()

    for tag in soup.find_all(["a", "link", "script", "img", "iframe"]):
        for attr in ["href", "src"]:
            link = tag.get(attr)
            if link:
                full_url = urljoin(base_url, link)
                if BASE_URL in full_url and full_url not in visited_urls:
                    found.add(full_url)
    return found

# Récupération d’un fichier brut
def try_download(url):
    if url in visited_urls:
        return
    visited_urls.add(url)
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200 and r.content:
            save_file(url, r.content)
        elif r.status_code == 403:
            log_info(f"[×] Accès interdit: {url}")
        elif r.status_code == 404:
            log_info(f"[×] Non trouvé: {url}")
    except Exception as e:
        log_info(f"[!] Exception: {url} => {e}")

# Bruteforce à partir de la wordlist
def brute_force(base_path):
    for word in WORDLIST:
        full_url = urljoin(BASE_URL, f"{base_path}/{word}")
        try_download(full_url)

# Scan d’un répertoire en profondeur
def deep_scan(base_path):
    log_info(f"[*] Scan du répertoire: {base_path}")
    url = urljoin(BASE_URL, base_path)
    html = fetch_html(url)
    if not html:
        return
    links = extract_links(html, url)
    for link in links:
        if link.endswith("/") or any(x in link for x in [".html", ".cgi", ".js", ".css", ".jpg", ".png", ".ico"]):
            try_download(link)
        if link.endswith("/") or "/cgi/" in link or "/eng/" in link:
            deep_scan(urlparse(link).path)

# Script principal
def main():
    os.makedirs(DUMP_DIR, exist_ok=True)
    open(LOG_FILE, "w").close()

    log_info("[*] Démarrage du script IPCam Scraper")
    # Étape 1 - Récupérer la page principale
    homepage = fetch_html(BASE_URL + "/")
    if homepage:
        log_info("[✓] Page d’accueil téléchargée")

        links = extract_links(homepage, BASE_URL)
        for link in links:
            try_download(link)

    # Étape 2 - Bruteforce sur les paths
    log_info("[*] Bruteforce sur les chemins à partir de paths.txt")
    for path in DEFAULT_PATHS:
        full_url = urljoin(BASE_URL, path)
        try_download(full_url)
        brute_force(path)
        deep_scan(path)

    log_info("[✓] Scan terminé.")

if __name__ == "__main__":
    main()

