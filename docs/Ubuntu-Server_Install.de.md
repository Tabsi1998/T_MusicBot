## **Schritt-für-Schritt-Anleitung zur Installation des Discord-Musikbots auf einem Ubuntu-Server**

### **Voraussetzungen**

- **Ubuntu-Server** mit SSH-Zugriff.
- **Discord-Bot-Token**: Stelle sicher, dass du ein gültiges Bot-Token von [Discord Developer Portal](https://discord.com/developers/applications) hast.
- **Spotify API Zugangsdaten**: Spotify `client_id` und `client_secret`, erhältlich unter [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).

---

### **1. Server vorbereiten**

#### **1.1 System aktualisieren**

Aktualisiere zuerst dein System, um sicherzustellen, dass alle Pakete auf dem neuesten Stand sind:

```bash
sudo apt update && sudo apt upgrade -y
```

---

### **2. Notwendige Pakete installieren**

#### **2.1 Git installieren**

Falls Git nicht bereits installiert ist, installiere es mit:

```bash
sudo apt install git -y
```

#### **2.2 Python und Pip installieren**

Installiere Python 3 und Pip:

```bash
sudo apt install python3 python3-pip -y
```

#### **2.3 FFmpeg installieren**

FFmpeg wird für die Audioverarbeitung benötigt:

```bash
sudo apt install ffmpeg -y
```

#### **2.4 Zusätzliche Bibliotheken installieren**

Einige Python-Pakete benötigen zusätzliche Systembibliotheken:

```bash
sudo apt install build-essential libffi-dev python3-dev -y
```

---

### **3. Projekt klonen**

Wechsle in das Verzeichnis, in dem du den Bot installieren möchtest, und klone das Git-Repository:

```bash
cd /pfad/zu/deinem/verzeichnis
git clone https://github.com/Tabsi1998/T_MusicBot.git
cd T_MusicBot
```

---

### **5. Python-Abhängigkeiten installieren**

#### **5.1 Anforderungen installieren**

Stelle sicher, dass eine `requirements.txt`-Datei vorhanden ist. Installiere die Python-Abhängigkeiten mit:

```bash
pip install -r requirements.txt --break-system-packages
```


### **6. Bot konfigurieren**

#### **6.1 `config.json` erstellen**

Erstelle eine `config.json`-Datei im Projektverzeichnis und füge deine Konfigurationsparameter hinzu:

```json
{
  "bot_token": "DEIN_DISCORD_BOT_TOKEN",
  "spotify_client_id": "DEIN_SPOTIFY_CLIENT_ID",
  "spotify_client_secret": "DEIN_SPOTIFY_CLIENT_SECRET",
  "command_prefix": "!",
  "language": "en",
  "default_volume": 50,
  "ffmpeg_path": "/usr/bin/ffmpeg",
  "embed_settings": {
    "footer": "Dein Bot-Name"
  },
  "commands": {
    "play": {
      "name": "play",
      "aliases": ["p"]
    },
    "volume": {
      "name": "volume",
      "aliases": ["vol"]
    },
    "pause": {
      "name": "pause",
      "aliases": ["pa"]
    },
    "resume": {
      "name": "resume",
      "aliases": ["res"]
    },
    "skip": {
      "name": "skip",
      "aliases": ["s"]
    },
    "stop": {
      "name": "stop",
      "aliases": ["st"]
    },
    "queue": {
      "name": "queue",
      "aliases": ["q", "list"]
    },
    "help": {
      "name": "help",
      "aliases": ["h"]
    },
    "loop": {
      "name": "loop",
      "aliases": ["repeat"]
    }
  }
}
```

**Hinweis:** Ersetze die Platzhalter mit deinen tatsächlichen Zugangsdaten und gewünschten Einstellungen.

#### **6.2 `lang.json` überprüfen oder erstellen**

Stelle sicher, dass eine `lang.json`-Datei vorhanden ist und die benötigten Sprachstrings für Deutsch (`"de"`) enthält.

---

### **7. FFmpeg-Pfad überprüfen**

Vergewissere dich, dass der `ffmpeg_path` in der `config.json` korrekt ist. Standardmäßig sollte FFmpeg unter `/usr/bin/ffmpeg` installiert sein.

---

### **8. Bot starten**


#### **8.1 Bot ausführen**

Starte den Bot mit:

```bash
python3 T_MusicBot.py
```

**Hinweis:** Ersetze `T_MusicBot.py` durch den Namen deiner Haupt-Python-Datei, falls er anders lautet.

---

### **9. Bot im Hintergrund ausführen (optional)**

Damit der Bot weiterläuft, auch wenn du die SSH-Verbindung trennst, kannst du `screen` oder `tmux` verwenden.

#### **9.1 Screen installieren**

```bash
sudo apt install screen -y
```

#### **9.2 Neue Screen-Session starten**

```bash
screen -S musikbot
```

#### **9.3 Bot in Screen-Session starten**

```bash
source venv/bin/activate
python3 T_MusicBot.py
```

#### **9.4 Screen-Session trennen**

Drücke `Ctrl + A`, dann `D`, um die Session zu trennen.

#### **9.5 Zur Screen-Session zurückkehren**

```bash
screen -r musikbot
```

---

### **10. Automatisches Starten des Bots beim Systemstart (optional)**

Du kannst den Bot so konfigurieren, dass er beim Hochfahren des Servers automatisch startet, indem du einen Systemd-Service erstellst.

#### **10.1 Systemd-Service-Datei erstellen**

```bash
sudo nano /etc/systemd/system/musikbot.service
```

#### **10.2 Folgenden Inhalt einfügen**

```ini
[Unit]
Description=Discord Musikbot
After=network.target

[Service]
User=DEIN_BENUTZERNAME
Group=DEINE_GRUPPE
WorkingDirectory=/pfad/zu/deinem/projektverzeichnis
ExecStart=/pfad/zu/deinem/projektverzeichnis/venv/bin/python3 /pfad/zu/deinem/projektverzeichnis/T_MusicBot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Hinweis:** Ersetze `DEIN_BENUTZERNAME`, `DEINE_GRUPPE` und die Pfade entsprechend deiner Umgebung.

#### **10.3 Service laden und starten**

```bash
sudo systemctl daemon-reload
sudo systemctl enable musikbot.service
sudo systemctl start musikbot.service
```

#### **10.4 Status des Services überprüfen**

```bash
sudo systemctl status musikbot.service
```

---

### **11. Fehlerbehebung**

- **Logs überprüfen:** Falls der Bot nicht wie erwartet funktioniert, überprüfe die `error.log`-Datei im Projektverzeichnis.
- **Abhängigkeiten prüfen:** Stelle sicher, dass alle Python-Abhängigkeiten korrekt installiert sind.
- **Bot-Permissions:** Vergewissere dich, dass dein Discord-Bot die erforderlichen Berechtigungen hat, um Nachrichten zu lesen, zu schreiben und Sprachkanälen beizutreten.

---

### **12. Zusammenfassung der wichtigsten Befehle**

- **Bot starten:** `python3 T_MusicBot.py`
- **Virtuelle Umgebung aktivieren:** `source venv/bin/activate`
- **Screen-Session starten:** `screen -S musikbot`
- **Systemd-Service verwalten:**
  - **Starten:** `sudo systemctl start musikbot.service`
  - **Stoppen:** `sudo systemctl stop musikbot.service`
  - **Status überprüfen:** `sudo systemctl status musikbot.service`
