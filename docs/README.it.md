# Discord Music Bot 🎶

Un bot musicale Discord ricco di funzionalità capace di riprodurre canzoni e playlist da YouTube e Spotify. Supporta più lingue, controlli interattivi direttamente all'interno di Discord e offre un design moderno e user-friendly.

## Funzionalità

- **Riproduci Musica**: Trasmetti file audio di alta qualità da YouTube e Spotify direttamente nel tuo canale vocale.
- **Supporto Playlist**: Carica playlist intere o singole canzoni da YouTube e Spotify.
- **Multilingue**: Supporto per più lingue (tedesco, inglese, italiano, francese) con file linguistici facilmente modificabili.
- **Controllo Interattivo**: Usa emoji di reazione per controllare la riproduzione direttamente dal messaggio "In riproduzione" (Play/Pausa, Canzone Successiva, Canzone Precedente, Stop).
- **Sistema di Coda**: Aggiungi canzoni alla coda e visualizza la coda corrente.
- **Controllo del Volume**: Regola il volume di riproduzione; le impostazioni vengono salvate tra le sessioni.
- **Cronologia Canzoni**: Torna alle canzoni precedenti e risentile.
- **Barra di Progressione**: Mostra una barra di progressione moderna per la canzone corrente.
- **Impostazioni Persistenti**: Le impostazioni del volume vengono salvate e mantenute dopo un riavvio.
- **Logging degli Errori**: Tutti gli errori vengono registrati in un file `error.log`.

## Sommario

- [Installazione](#installazione)
- [Configurazione](#configurazione)
- [Utilizzo](#utilizzo)
- [Comandi](#comandi)
- [Supporto Linguistico](#supporto-linguistico)
- [Dipendenze](#dipendenze)
- [Contribuire](#contribuire)
- [Licenza](#licenza)

## Installazione

Per una guida dettagliata sull'installazione su un server Ubuntu, consulta [Ubuntu-Server_Install.md](Ubuntu-Server_Install.md).

### Prerequisiti

- **Python 3.8** o superiore
- **FFmpeg**: Deve essere installato sul sistema e il percorso deve essere noto.

### Passaggi

1. **Clonare il Repository:**

   ```bash
   git clone https://github.com/Tabsi1998/T_MusicBot.git
   cd T_MusicBot
   ```

2. **Installare i Pacchetti Python Necessari:**

   Assicurati di aver installato tutti i pacchetti necessari.

   ```bash
   pip install -r requirements.txt
   ```

3. **Installare FFmpeg:**

   - **Windows:** Scarica FFmpeg da [ffmpeg.org](https://ffmpeg.org/download.html) e aggiungilo al PATH di sistema oppure specifica il percorso in `config.json`.
   - **Linux:** Installalo tramite il gestore di pacchetti, ad esempio `sudo apt-get install ffmpeg`.
   - **macOS:** Installalo tramite Homebrew, ad esempio `brew install ffmpeg`.

## Configurazione

1. **Creare un Account Bot Discord:**

   - Vai al [Discord Developer Portal](https://discord.com/developers/applications) e crea una nuova applicazione.
   - Naviga su **"Bot"** e crea un utente bot.
   - Copia il **Token del Bot**.

2. **Configurare le Credenziali API Spotify (opzionale, per il supporto Spotify):**

   - Crea una nuova app nel [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Copia il **Client ID** e il **Client Secret**.

3. **Modificare `config.json`:**

   Rinomina `config.example.json` in `config.json` e compila i dettagli richiesti:

   ```json
   {
     "bot_token": "TUO_TOKEN_BOT_DISCORD",
     "spotify_client_id": "TUO_CLIENT_ID_SPOTIFY",
     "spotify_client_secret": "TUO_CLIENT_SECRET_SPOTIFY",
     "language": "it",
     "command_prefix": "!",
     "default_volume": 50,
     "ffmpeg_path": "ffmpeg",
     "embed_settings": {
       "footer": "Buon divertimento con la musica!"
     },
     "commands": {
       "play": {
         "name": "play",
         "aliases": ["p", "riproduremusi", "avviare"]
       },
       "pause": {
         "name": "pause",
         "aliases": ["mettereinpausa"]
       },
       "resume": {
         "name": "resume",
         "aliases": ["continua"]
       },
       "stop": {
         "name": "stop",
         "aliases": ["s", "fermare", "stopper"]
       },
       "skip": {
         "name": "skip",
         "aliases": ["next", "saltare", "successivo"]
       },
       "volume": {
         "name": "volume",
         "aliases": ["vol", "livello"]
       },
       "queue": {
         "name": "queue",
         "aliases": ["q", "coda"]
       },
       "help": {
         "name": "help",
         "aliases": ["h", "aiuto"]
       },
       "loop": {
         "name": "loop",
         "aliases": ["ripetere", "loop"]
       },
       "setlang": {
         "name": "setlang",
         "aliases": ["lingua"]
       }
     }
   }
   ```

   **Note:**

   - **`bot_token`**: Il tuo token bot Discord.
   - **`spotify_client_id` & `spotify_client_secret`**: Le tue credenziali API Spotify.
   - **`language`**: Il codice lingua per la lingua desiderata (`de`, `en`, `it`, `fr`).
   - **`command_prefix`**: Il prefisso per i comandi del bot (es. `?`).
   - **`default_volume`**: Livello di volume predefinito (1-100).
   - **`ffmpeg_path`**: Percorso all'installazione di FFmpeg (`"ffmpeg"`, se è nel PATH di sistema).
   - **`embed_settings`**: Impostazioni per gli embed, es. testo del footer.

4. **Assicurarsi che `lang.json` Esista:**

   Assicurati che il file `lang.json` sia presente nella directory del progetto e contenga le traduzioni necessarie.

## Utilizzo

Avvia il bot con:

```bash
python python/T_MusicBot.py
```

### Aggiungere il Bot al Tuo Server

1. Vai al Discord Developer Portal, seleziona la tua applicazione e naviga su **"OAuth2" > "URL Generator"**.
2. Seleziona gli scopes **"bot"** e **"applications.commands"**.
3. Sotto **Bot Permissions**, seleziona le autorizzazioni richieste:
   - **Autorizzazioni Generali**:
     - Leggere la cronologia dei messaggi
     - Inviare messaggi
     - Gestire i messaggi
     - Aggiungere reazioni
   - **Autorizzazioni Vocali**:
     - Collegarsi ai canali vocali
     - Parlare nei canali vocali
4. Copia l'URL generato e aprilo nel tuo browser per aggiungere il bot al tuo server.

## Comandi

- **`!play <URL o termine di ricerca>`** : Riproduce una canzone o una playlist da YouTube o Spotify.
  - Supporta link YouTube e Spotify così come termini di ricerca diretti.
- **`!pause`** : Mette in pausa la riproduzione attuale.
- **`!resume`** : Riprende la riproduzione se in pausa.
- **`!skip`** : Salta la canzone attuale.
- **`!stop`** : Ferma la riproduzione, svuota la coda e disconnette.
- **`!volume <1-100>`** : Imposta il volume di riproduzione.
- **`!queue`** : Mostra la coda attuale delle canzoni.
- **`!help`** : Mostra il messaggio di aiuto con tutti i comandi disponibili.
- **`!loop`** : Attiva o disattiva il loop per la canzone attuale.
- **`!setlang <codice_lingua>`** : Imposta la lingua del bot (es. `en`, `de`, `it`, `fr`).

### Controllo Interattivo tramite Reazioni

- **⏮️** : Canzone precedente
- **⏯️** : Pausa/Riprendi
- **⏭️** : Canzone successiva
- **⏹️** : Ferma la riproduzione e disconnette

## Supporto Linguistico

Il bot supporta più lingue. I codici lingua disponibili sono:

- **Tedesco** : `de`
- **Inglese** : `en`
- **Italiano** : `it`
- **Francese** : `fr`

### Impostare la Lingua

Cambia il campo `"language"` nel tuo `config.json` per utilizzare la lingua desiderata:

```json
{
  "language": "it"
}
```

### Aggiungere le Tue Traduzioni

1. Apri il file `lang.json`.
2. Aggiungi una nuova sezione linguistica con il corrispondente codice lingua.
3. Traduce i testi o adattali alle tue esigenze.

Esempio:

```json
{
  "es": {
    "no_voice_channel": "¡Debes estar en un canal de voz para que el bot se una!",
    // ... altre chiavi
  }
}
```

## Dipendenze

Il bot richiede i seguenti pacchetti Python:

- **discord.py**
- **yt-dlp**
- **spotipy**
- **PyNaCl**

Installa tutte le dipendenze con:

```bash
pip install -r requirements.txt
```

**Contenuto di `requirements.txt`:**

```
discord.py
yt-dlp
spotipy
PyNaCl
```

## Contribuire

I contributi sono benvenuti! Segui questi passaggi:

1. **Forkare il Repository:**

   Clicca su **"Fork"** per creare una copia del repository nel tuo account GitHub.

2. **Creare un Nuovo Branch:**

   ```bash
   git checkout -b feature/mio-nuovo-feature
   ```

3. **Apportare Modifiche e Commitare:**

   ```bash
   git commit -m "Aggiungi funzionalità: Mio Nuovo Feature"
   ```

4. **Pushare il Branch:**

   ```bash
   git push origin feature/mio-nuovo-feature
   ```

5. **Aprire una Pull Request:**

   Vai al tuo repository su GitHub e apri una nuova Pull Request.

## Licenza

Questo progetto è sotto licenza [MIT](LICENSE). Vedi il file `LICENSE` per maggiori dettagli.

---

**Divertiti con la musica!** Se riscontri problemi o hai suggerimenti per nuove funzionalità, sentiti libero di aprire un issue o una pull request.

---

**Nota**

Questo bot è stato sviluppato con un focus sulla facilità d'uso e l'estensibilità. Sono state seguite le migliori pratiche durante l'implementazione per fornire un bot musicale stabile e affidabile per la tua comunità Discord.

**Grazie per aver utilizzato questo bot!**