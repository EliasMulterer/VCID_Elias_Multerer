# Anleitung um die Applikation zu Deployen

Git Installieren auf Host
```bash
sudo apt install -y git
```
Repository auf Host Klonen
```bash
git clone https://github.com/EliasMulterer/VCID_Elias_Multerer.git
```

## Installation
In neu erstelltes Verzeichnis wechseln
```bash
# Datei ausführbar machen
chmod +x install_app.sh
# Install script ausführen
./install_app.sh
```

## Starten der Applikation
```bash
# App starten
./app_start.sh
```

Auf die App kann nun über den Port 8080 via http zugegriffen werden.
Anhand Google Cloud installation:
http://34.34.148.252:8080
