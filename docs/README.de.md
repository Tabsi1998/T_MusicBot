# Discord Music Bot 🎶

Ein funktionsreicher Discord-Musikbot, der Songs und Playlists von YouTube und Spotify abspielen kann. Er unterstützt mehrere Sprachen, interaktive Steuerungen direkt in Discord und bietet ein modernes, benutzerfreundliches Design.

## Funktionen

- **Musik abspielen**: Streame hochwertige Audiodateien von YouTube und Spotify direkt in deinen Sprachkanal.
- **Playlist-Unterstützung**: Lade ganze Playlists oder einzelne Songs von YouTube und Spotify.
- **Mehrsprachigkeit**: Unterstützung für mehrere Sprachen (Deutsch, Englisch, Italienisch, Französisch) mit leicht editierbaren Sprachdateien.
- **Interaktive Steuerung**: Verwende Reaktions-Emojis, um die Wiedergabe direkt aus der "Jetzt spielt"-Nachricht zu steuern (Play/Pause, Nächstes Lied, Vorheriges Lied, Stop).
- **Warteschlangen-System**: Füge Songs zur Warteschlange hinzu und zeige die aktuelle Warteschlange an.
- **Lautstärkeregelung**: Passe die Wiedergabelautstärke an; die Einstellungen werden zwischen den Sitzungen gespeichert.
- **Song-Historie**: Gehe zu vorherigen Songs zurück und höre sie erneut.
- **Fortschrittsanzeige**: Zeigt einen modernen Fortschrittsbalken für den aktuellen Song an.
- **Persistente Einstellungen**: Lautstärkeeinstellungen werden gespeichert und bleiben nach einem Neustart erhalten.
- **Fehlerlogging**: Alle Fehler werden in einer `error.log`-Datei protokolliert.

## Inhaltsverzeichnis

- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Verwendung](#verwendung)
- [Befehle](#befehle)
- [Sprachunterstützung](#sprachunterstützung)
- [Abhängigkeiten](#abhängigkeiten)
- [Mitwirken](#mitwirken)
- [Lizenz](#lizenz)

## Installation

Für eine detaillierte Anleitung zur Installation auf einem Ubuntu-Server, siehe [Ubuntu-Server_Install.md](Ubuntu-Server_Install.md).

### Voraussetzungen

- **Python 3.8** oder höher
- **FFmpeg**: Muss auf dem System installiert sein und der Pfad sollte bekannt sein.

### Schritte

1. **Repository klonen:**

   ```bash
   git clone https://github.com/deinbenutzername/dein-repo-name.git
   cd dein-repo-name
   ```

2. **Erforderliche Python-Pakete installieren:**

   Stelle sicher, dass du alle benötigten Pakete installiert hast.

   ```bash
   pip install -r requirements.txt
   ```

3. **FFmpeg installieren:**

   - **Windows:** Lade FFmpeg von [ffmpeg.org](https://ffmpeg.org/download.html) herunter und füge es deinem System-PATH hinzu oder gib den Pfad in der `config.json` an.
   - **Linux:** Installiere es über den Paketmanager, z.B. `sudo apt-get install ffmpeg`.
   - **macOS:** Installiere es über Homebrew, z.B. `brew install ffmpeg`.

## Konfiguration

1. **Erstelle einen Discord-Bot-Account:**

   - Gehe zum [Discord Developer Portal](https://discord.com/developers/applications) und erstelle eine neue Anwendung.
   - Navigiere zu **"Bot"** und erstelle einen Bot-Benutzer.
   - Kopiere den **Bot-Token**.

2. **Spotify-API-Anmeldedaten einrichten (optional, für Spotify-Unterstützung):**

   - Erstelle eine neue App im [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Kopiere die **Client-ID** und das **Client Secret**.

3. **`config.json` bearbeiten:**

   Benenne `config.example.json` in `config.json` um und fülle die erforderlichen Details aus:

   ```json
   {
     "bot_token": "DEIN_DISCORD_BOT_TOKEN",
     "spotify_client_id": "DEINE_SPOTIFY_CLIENT_ID",
     "spotify_client_secret": "DEIN_SPOTIFY_CLIENT_SECRET",
     "language": "de",
     "command_prefix": "!",
     "default_volume": 50,
     "ffmpeg_path": "ffmpeg",
     "embed_settings": {
       "footer": "Viel Spaß mit der Musik!"
     },
     "commands": {
       "play": {
         "name": "play",
         "aliases": ["p", "spielen", "abspielen"]
       },
       "pause": {
         "name": "pause",
         "aliases": ["pausieren"]
       },
       "resume": {
         "name": "resume",
         "aliases": ["continue", "fortsetzen"]
       },
       "stop": {
         "name": "stop",
         "aliases": ["s", "halt", "anhalten"]
       },
       "skip": {
         "name": "skip",
         "aliases": ["next", "überspringen", "weiter"]
       },
       "volume": {
         "name": "volume",
         "aliases": ["vol", "lautstärke"]
       },
       "queue": {
         "name": "queue",
         "aliases": ["q", "warteschlange"]
       },
       "help": {
         "name": "help",
         "aliases": ["h", "hilfe"]
       },
       "loop": {
         "name": "loop",
         "aliases": ["repeat", "wiederholen"]
       },
       "setlang": {
         "name": "setlang",
         "aliases": ["language"]
       }
     }
   }
   ```

   **Hinweise:**

   - **`bot_token`**: Dein Discord-Bot-Token.
   - **`spotify_client_id` & `spotify_client_secret`**: Deine Spotify-API-Anmeldedaten.
   - **`language`**: Der Sprachcode für die gewünschte Sprache (`de`, `en`, `it`, `fr`).
   - **`command_prefix`**: Das Präfix für Bot-Befehle (z.B. `?`).
   - **`default_volume`**: Standardlautstärke (1-100).
   - **`ffmpeg_path`**: Pfad zur FFmpeg-Installation (`"ffmpeg"`, wenn es im System-PATH ist).
   - **`embed_settings`**: Einstellungen für die Einbettungen (Embeds), z.B. der Footer-Text.

4. **`lang.json` sicherstellen:**

   Stelle sicher, dass die `lang.json`-Datei im Projektverzeichnis vorhanden ist und die notwendigen Übersetzungen enthält.

## Verwendung

Starte den Bot mit:

```bash
python python/T_MusicBot.py
```

### Den Bot zu deinem Server hinzufügen

1. Gehe zum Discord Developer Portal, wähle deine Anwendung und navigiere zu **"OAuth2" > "URL Generator"**.
2. Wähle die Scopes **"bot"** und **"applications.commands"**.
3. Unter **Bot Permissions** wähle die erforderlichen Berechtigungen:
   - **General Permissions**:
     - Lesen von Nachrichten/Verlauf
     - Nachrichten senden
     - Nachrichten verwalten
     - Reaktionen hinzufügen
   - **Voice Permissions**:
     - Sprachkanäle betreten
     - Sprachübertragung
4. Kopiere die generierte URL und öffne sie in deinem Browser, um den Bot zu deinem Server hinzuzufügen.

## Befehle

- **`!play <URL oder Suchbegriff>`**: Spielt einen Song oder eine Playlist von YouTube oder Spotify ab.
  - Unterstützt YouTube- und Spotify-Links sowie direkte Suchbegriffe.
- **`!pause`**: Pausiert die aktuelle Wiedergabe.
- **`!resume`**: Setzt die Wiedergabe fort, falls pausiert.
- **`!skip`**: Überspringt den aktuellen Song.
- **`!stop`**: Stoppt die Wiedergabe, leert die Warteschlange und trennt die Verbindung.
- **`!volume <1-100>`**: Stellt die Wiedergabelautstärke ein.
- **`!queue`**: Zeigt die aktuelle Song-Warteschlange an.
- **`!help`**: Zeigt die Hilfenachricht mit allen verfügbaren Befehlen an.
- **`!loop`**: Aktiviert oder deaktiviert die Schleife für den aktuellen Song.
- **`!setlang <sprachcode>`**: Setzt die Sprache des Bots (z.B. `en`, `de`, `it`, `fr`).

### Interaktive Steuerung über Reaktionen

- **⏮️**: Vorheriger Song
- **⏯️**: Pause/Fortsetzen
- **⏭️**: Nächster Song
- **⏹️**: Stoppt die Wiedergabe und trennt die Verbindung

## Sprachunterstützung

Der Bot unterstützt mehrere Sprachen. Die verfügbaren Sprachcodes sind:

- **Deutsch**: `de`
- **Englisch**: `en`
- **Italienisch**: `it`
- **Französisch**: `fr`

### Sprache einstellen

Ändere das Feld `"language"` in deiner `config.json`, um die gewünschte Sprache zu verwenden:

```json
{
  "language": "de"
}
```

### Eigene Übersetzungen hinzufügen

1. Öffne die `lang.json`-Datei.
2. Füge einen neuen Sprachabschnitt mit dem entsprechenden Sprachcode hinzu.
3. Übersetze die Texte oder passe sie an deine Bedürfnisse an.

Beispiel:

```json
{
  "es": {
    "no_voice_channel": "¡Debes estar en un canal de voz para que el bot se una!",
    // ... weitere Schlüssel
  }
}
```

## Abhängigkeiten

Der Bot benötigt folgende Python-Pakete:

- **discord.py**
- **yt-dlp**
- **spotipy**
- **PyNaCl**

Installiere alle Abhängigkeiten mit:

```bash
pip install -r requirements.txt
```

**Inhalt der `requirements.txt`:**

```
discord.py
yt-dlp
spotipy
PyNaCl
```

## Mitwirken

Beiträge sind willkommen! Bitte folge diesen Schritten:

1. **Repository forken:**

   Klicke auf **"Fork"**, um eine Kopie des Repositories in deinem GitHub-Konto zu erstellen.

2. **Neuen Branch erstellen:**

   ```bash
   git checkout -b feature/mein-neues-feature
   ```

3. **Änderungen vornehmen und committen:**

   ```bash
   git commit -m "Füge mein neues Feature hinzu"
   ```

4. **Branch pushen:**

   ```bash
   git push origin feature/mein-neues-feature
   ```

5. **Pull Request öffnen:**

   Gehe zu deinem Repository auf GitHub und öffne einen neuen Pull Request.

## Lizenz

Dieses Projekt ist unter der [MIT-Lizenz](LICENSE) lizenziert. Weitere Informationen findest du in der `LICENSE`-Datei.

---

**Viel Spaß mit der Musik!** Wenn du Probleme hast oder Vorschläge für neue Features hast, öffne gerne ein Issue oder einen Pull Request.

---

**Hinweis**

Dieser Bot wurde mit Fokus auf Benutzerfreundlichkeit und Erweiterbarkeit entwickelt. Bei der Implementierung wurden bewährte Praktiken berücksichtigt, um einen stabilen und zuverlässigen Musikbot für deine Discord-Community bereitzustellen.

**Vielen Dank für die Nutzung dieses Bots!**