import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import logging

def load_config(path='config/config.json'):
    try:
        print("Lade Konfigurationsdatei...")
        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            print("Konfigurationsdatei erfolgreich geladen.")
            return config
    except Exception as e:
        print(f"Fehler beim Laden von {path}: {e}")
        logging.error(f"Fehler beim Laden von {path}: {e}")
        return None

def authenticate_spotify(config):
    try:
        print("Authentifiziere Spotify...")
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=config['spotify_client_id'],
            client_secret=config['spotify_client_secret']
        ))
        print("Spotify-Authentifizierung erfolgreich.")
        return sp
    except Exception as e:
        print(f"Fehler bei der Spotify-Authentifizierung: {e}")
        logging.error(f"Fehler bei der Spotify-Authentifizierung: {e}")
        return None

def test_spotify_api(sp, track_url):
    try:
        print(f"Rufe Track-Info für URL: {track_url} ab...")
        track_info = sp.track(track_url)
        preview_url = track_info.get('preview_url')
        if preview_url:
            print(f"Preview URL: {preview_url}")
        else:
            print("Keine Preview-URL für diesen Track verfügbar.")
    except Exception as e:
        print(f"Fehler beim Abrufen von Track-Info: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print("Starte Testskript für Spotify-API...")
    config = load_config()
    if config:
        sp = authenticate_spotify(config)
        if sp:
            # Ersetze dies durch einen gültigen Spotify-Track-Link mit Preview
            test_track_url = "https://open.spotify.com/track/03xIKiQXopptD4Sv8ijvcG"
            test_spotify_api(sp, test_track_url)
    print("Testskript beendet.")
