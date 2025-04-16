import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "http://192.168.0.234"
START_PATHS = ["/eng", "/cgi", "/setup", "/"]
DUMP_FOLDER = "dump"
WORDLIST_FILE = "wordlist.txt"
PATHS_FILE = "paths.txt"
COMMON_EXTENSIONS = ["", ".html", ".htm", ".js", ".cgi", ".jpg", ".png", ".gif", ".css",".png", ".bin", ".cfg", ".php", ".dat", ".mp3", ".mp4", ".avi", ".log", ".*"]

def save_file(url, local_path):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f"[+] Fichier sauvegardé: {local_path}")
        else:
            print(f"[-] Échec ({response.status_code}) pour {url}")
    except requests.RequestException as e:
        print(f"[!] Erreur lors de la requête vers {url}: {e}")

def load_lines_from_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []

def brute_force_paths(base_path):
    wordlist = load_lines_from_file(WORDLIST_FILE)
    found_urls = set()
    for word in wordlist:
        for ext in COMMON_EXTENSIONS:
            test_path = f"{base_path}/{word}{ext}".replace("//", "/")
            full_url = urljoin(BASE_URL, test_path)
            try:
                r = requests.get(full_url, timeout=5)
                if r.status_code == 200:
                    found_urls.add(full_url)
                    print(f"[✓] Trouvé: {full_url}")
                    save_file(full_url, os.path.join(DUMP_FOLDER, test_path.lstrip('/')))
            except:
                continue
    return found_urls

def crawl_html(url):
    print(f"[*] Crawl de: {url}")
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            save_file(url, os.path.join(DUMP_FOLDER, url.replace(BASE_URL, '').lstrip('/')))
            for tag in soup.find_all(['a', 'link', 'script', 'img']):
                attr = 'href' if tag.name in ['a', 'link'] else 'src'
                if tag.has_attr(attr):
                    file_url = urljoin(url, tag[attr])
                    if file_url.startswith(BASE_URL):
                        local_path = os.path.join(DUMP_FOLDER, file_url.replace(BASE_URL, '').lstrip('/'))
                        save_file(file_url, local_path)
    except Exception as e:
        print(f"[!] Erreur lors du crawl de {url}: {e}")

def full_recursive_scan():
    visited = set()
    paths = set(load_lines_from_file(PATHS_FILE)) | set(START_PATHS)

    for base in paths:
        print(f"\n[→] Scanning: {base}")
        full_url = urljoin(BASE_URL, base)
        crawl_html(full_url)
        visited |= brute_force_paths(base)

    print("\n[✓] Scan complet terminé.")

if __name__ == "__main__":
    print("[*] Lancement de l'analyse de la caméra...")
    full_recursive_scan()

