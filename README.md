```markdown
# Discord Music Bot 🎶

Ein funktionsreicher Discord-Musikbot, der Songs und Playlists von YouTube und Spotify abspielt, mit Unterstützung für mehrere Sprachen und interaktiven Steuerelementen direkt in Discord.

## Features

- **Musik abspielen**: Streame hochwertige Audiodateien von YouTube und Spotify.
- **Playlist-Unterstützung**: Lade ganze Playlists oder einzelne Songs von YouTube und Spotify.
- **Lokalisierung**: Mehrsprachige Unterstützung mit leicht editierbaren Sprachdateien.
- **Lautstärkeregelung**: Passe die Wiedergabelautstärke an, Einstellungen werden zwischen den Sitzungen gespeichert.
- **Interaktive Steuerung**: Verwende Reaktions-Emojis, um die Wiedergabe direkt aus der "Jetzt spielt"-Nachricht zu steuern.
- **Warteschlangen-System**: Zeige und verwalte die aktuelle Song-Warteschlange.
- **Automatische Wiederverbindung**: Der Bot stellt die Verbindung zum Sprachkanal bei unerwarteter Trennung wieder her.
- **Persistente Einstellungen**: Lautstärkeeinstellungen werden gespeichert und bleiben nach einem Neustart erhalten.

## Inhaltsverzeichnis

- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Verwendung](#verwendung)
- [Befehle](#befehle)
- [Lokalisierung](#lokalisierung)
- [Abhängigkeiten](#abhängigkeiten)
- [Mitwirken](#mitwirken)
- [Lizenz](#lizenz)

## Installation

1. **Repository klonen:**

   ```bash
   git clone https://github.com/deinbenutzername/dein-repo-name.git
   cd dein-repo-name
   ```

2. **Erforderliche Python-Pakete installieren:**

   Stelle sicher, dass du Python 3.8 oder höher installiert hast.

   ```bash
   pip install -r requirements.txt
   ```

3. **FFmpeg installieren:**

   - **Windows:** Lade FFmpeg von [hier](https://ffmpeg.org/download.html) herunter und füge es deinem System-PATH hinzu.
   - **Linux:** Installiere es über den Paketmanager, z.B. `sudo apt-get install ffmpeg`.
   - **macOS:** Installiere es über Homebrew, z.B. `brew install ffmpeg`.

## Konfiguration

1. **Erstelle einen Discord-Bot-Account:**

   - Gehe zum [Discord Developer Portal](https://discord.com/developers/applications) und erstelle eine neue Anwendung.
   - Erstelle einen Bot-Benutzer und kopiere den Bot-Token.

2. **Spotify-API-Anmeldedaten einrichten (optional):**

   - Erstelle eine neue App im [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Kopiere die Client-ID und das Client Secret.

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
     }
   }
   ```

   - Ersetze die Platzhalter durch deine tatsächlichen Tokens und IDs.
   - Setze `ffmpeg_path` auf den Pfad, wo FFmpeg installiert ist, falls es nicht in deinem System-PATH ist.

4. **`lang.json` bearbeiten:**

   Stelle sicher, dass du eine `lang.json`-Datei in deinem Projektverzeichnis hast, die die notwendigen Lokalisierungsstrings enthält.

## Verwendung

Starte den Bot mit:

```bash
python music_bot.py
```

Lade den Bot mit der OAuth2-URL aus dem Developer Portal auf deinen Discord-Server ein und stelle sicher, dass er die notwendigen Berechtigungen hat:

- Nachrichten senden
- Links einbetten
- Nachrichtenverlauf lesen
- Reaktionen hinzufügen
- In Sprachkanälen verbinden und sprechen

## Befehle

- **`!play <URL oder Suchbegriff>`**: Spielt einen Song oder eine Playlist von YouTube oder Spotify ab.
- **`!pause`**: Pausiert die aktuelle Wiedergabe.
- **`!resume`**: Setzt die Wiedergabe fort, falls pausiert.
- **`!skip`**: Überspringt den aktuellen Song.
- **`!stop`**: Stoppt die Wiedergabe und leert die Warteschlange.
- **`!volume <1-100>`**: Stellt die Wiedergabelautstärke ein.
- **`!queue`**: Zeigt die aktuelle Song-Warteschlange an.
- **`!help`**: Zeigt die Hilfenachricht mit allen verfügbaren Befehlen an.

## Lokalisierung

Der Bot unterstützt mehrere Sprachen. Die `lang.json`-Datei enthält alle vom Bot verwendeten Texte, organisiert nach Sprachcodes.

So fügst du Übersetzungen hinzu oder bearbeitest sie:

1. Öffne `lang.json`.
2. Füge einen neuen Sprachabschnitt hinzu oder bearbeite die vorhandenen.
3. Aktualisiere das Feld `"language"` in `config.json`, um den gewünschten Sprachcode zu verwenden (z.B. `"de"` für Deutsch).

Beispielstruktur der `lang.json`:

```json
{
  "en": {
    "no_voice_channel": "You need to be in a voice channel to use this command!",
    // ... weitere Schlüssel
  },
  "de": {
    "no_voice_channel": "Du musst in einem Sprachkanal sein, um diesen Befehl zu verwenden!",
    // ... weitere Schlüssel
  }
}
```

## Abhängigkeiten

Der Bot benötigt folgende Python-Pakete:

- [discord.py](https://github.com/Rapptz/discord.py)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [spotipy](https://github.com/plamere/spotipy)

Diese sind in der `requirements.txt` aufgeführt.

**Inhalt der `requirements.txt`:**

```
discord.py
yt-dlp
spotipy
```

Installiere alle Python-Abhängigkeiten mit:

```bash
pip install -r requirements.txt
```

## Mitwirken

Beiträge sind willkommen! Bitte folge diesen Schritten:

1. Forke das Repository.
2. Erstelle einen neuen Branch:

   ```bash
   git checkout -b feature/dein-feature-name
   ```

3. Nimm deine Änderungen vor und committe sie:

   ```bash
   git commit -m "Füge deine Nachricht hier ein"
   ```

4. Pushe den Branch:

   ```bash
   git push origin feature/dein-feature-name
   ```

5. Öffne einen Pull Request und beschreibe deine Änderungen.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die [LICENSE](LICENSE)-Datei für Details.

---

Viel Spaß mit der Musik! Wenn du Probleme hast oder Vorschläge für neue Features, öffne gerne ein Issue oder einen Pull Request.