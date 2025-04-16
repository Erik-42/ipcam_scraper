# 📷 Vilar IP Camera File Scraper

Un outil de scraping et d'exploration des fichiers web embarqués sur les caméras IP **Vilar VS-IPC1002**, tournant sous **Linux 2.6 (no-MMU)** avec un serveur web **BOA**.

---

## 🚀 Fonctionnalités

- 🔍 **Exploration automatique** de la page d'accueil (HTML, CSS, JS, images, favicon…)
- 🗂️ **Brute-force intelligent** de chemins via `paths.txt` et de fichiers via `wordlist.txt`
- 🧠 **Détection manuelle** : intégration de chemins trouvés dans DevTools
- 📁 **Téléchargement complet** dans un répertoire local `dump/`
- 📋 **Affichage détaillé** : logs clairs des fichiers détectés (chemin, statut HTTP, taille…)
- 🧪 **Tests étendus sur `/eng`, `/cgi`, `/cgi/ieng`** pour découvrir tous les sous-dossiers et fichiers accessibles
- 🛠️ **Modularité** : facile à personnaliser, adaptable à d'autres caméras similaires

---

## 📂 Structure du projet
```bash
├── ipcam_scraper.py # Script principal 
├── wordlist.txt # Liste de fichiers à tester (config, js, html…) 
├── paths.txt # Liste de chemins/répertoires à brute-force 
├── dump/ # Contient tous les fichiers récupérés 
└── README.md # Ce fichier
```
---

## 🧾 Exemple de fichiers testés

### `paths.txt`
/eng 
/eng/view 
/eng/setup 
/cgi 
/cgi/ieng 
/cgi-bin

### `wordlist.txt`
index.html 
indexjava.html 
setup.html 
javascript.js 
style.css 
favicon.ico 
config.dat 
backup.cfg

---

## ▶️ Utilisation

Installe les dépendances si nécessaire :
```bash
pip install requests beautifulsoup4
```
   
Lancement du script :
```bash
python3 ipcam_scraper.py
```
Les fichiers récupérés seront disponibles dans le dossier `dump/`.

