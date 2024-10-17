# Discord Music Bot 🎶

A feature-rich Discord music bot capable of playing songs and playlists from YouTube and Spotify. It supports multiple languages, interactive controls directly within Discord, and offers a modern, user-friendly design.

## Features

- **Play Music**: Stream high-quality audio files from YouTube and Spotify directly into your voice channel.
- **Playlist Support**: Load entire playlists or individual songs from YouTube and Spotify.
- **Multilingual**: Support for multiple languages (German, English, Italian, French) with easily editable language files.
- **Interactive Control**: Use reaction emojis to control playback directly from the "Now Playing" message (Play/Pause, Next Song, Previous Song, Stop).
- **Queue System**: Add songs to the queue and display the current queue.
- **Volume Control**: Adjust playback volume; settings are saved between sessions.
- **Song History**: Go back to previous songs and listen to them again.
- **Progress Bar**: Displays a modern progress bar for the current song.
- **Persistent Settings**: Volume settings are saved and retained after a restart.
- **Error Logging**: All errors are logged in an `error.log` file.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands](#commands)
- [Language Support](#language-support)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Installation

For a detailed installation guide on an Ubuntu server, see [Ubuntu-Server_Install.md](Ubuntu-Server_Install.md).

### Prerequisites

- **Python 3.8** or higher
- **FFmpeg**: Must be installed on the system and the path should be known.

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Install Required Python Packages:**

   Ensure that you have all necessary packages installed.

   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg:**

   - **Windows:** Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your system PATH or specify the path in `config.json`.
   - **Linux:** Install it via the package manager, e.g., `sudo apt-get install ffmpeg`.
   - **macOS:** Install it via Homebrew, e.g., `brew install ffmpeg`.

## Configuration

1. **Create a Discord Bot Account:**

   - Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
   - Navigate to **"Bot"** and create a bot user.
   - Copy the **Bot Token**.

2. **Set Up Spotify API Credentials (optional, for Spotify support):**

   - Create a new app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Copy the **Client ID** and **Client Secret**.

3. **Edit `config.json`:**

   Rename `config.example.json` to `config.json` and fill in the required details:

   ```json
   {
     "bot_token": "YOUR_DISCORD_BOT_TOKEN",
     "spotify_client_id": "YOUR_SPOTIFY_CLIENT_ID",
     "spotify_client_secret": "YOUR_SPOTIFY_CLIENT_SECRET",
     "language": "en",
     "command_prefix": "!",
     "default_volume": 50,
     "ffmpeg_path": "ffmpeg",
     "embed_settings": {
       "footer": "Enjoy the music!"
     },
     "commands": {
       "play": {
         "name": "play",
         "aliases": ["p", "playmusic"]
       },
       "pause": {
         "name": "pause",
         "aliases": ["paus"]
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

   **Notes:**

   - **`bot_token`**: Your Discord bot token.
   - **`spotify_client_id` & `spotify_client_secret`**: Your Spotify API credentials.
   - **`language`**: The language code for the desired language (`de`, `en`, `it`, `fr`).
   - **`command_prefix`**: The prefix for bot commands (e.g., `?`).
   - **`default_volume`**: Default volume level (1-100).
   - **`ffmpeg_path`**: Path to the FFmpeg installation (`"ffmpeg"`, if it's in the system PATH).
   - **`embed_settings`**: Settings for embeds, e.g., footer text.

4. **Ensure `lang.json` Exists:**

   Make sure the `lang.json` file is present in the project directory and contains the necessary translations.

## Usage

Start the bot with:

```bash
python python/T_MusicBot.py
```

### Adding the Bot to Your Server

1. Go to the Discord Developer Portal, select your application, and navigate to **"OAuth2" > "URL Generator"**.
2. Select the scopes **"bot"** and **"applications.commands"**.
3. Under **Bot Permissions**, select the required permissions:
   - **General Permissions**:
     - Read Message History
     - Send Messages
     - Manage Messages
     - Add Reactions
   - **Voice Permissions**:
     - Connect to Voice Channels
     - Speak in Voice Channels
4. Copy the generated URL and open it in your browser to add the bot to your server.

## Commands

- **`!play <URL or search term>`**: Plays a song or playlist from YouTube or Spotify.
  - Supports YouTube and Spotify links as well as direct search terms.
- **`!pause`**: Pauses the current playback.
- **`!resume`**: Resumes playback if paused.
- **`!skip`**: Skips the current song.
- **`!stop`**: Stops playback, clears the queue, and disconnects.
- **`!volume <1-100>`**: Sets the playback volume.
- **`!queue`**: Displays the current song queue.
- **`!help`**: Shows the help message with all available commands.
- **`!loop`**: Enables or disables looping of the current song.
- **`!setlang <language_code>`**: Sets the bot's language (e.g., `en`, `de`, `it`, `fr`).

### Interactive Control via Reactions

- **⏮️**: Previous Song
- **⏯️**: Pause/Resume
- **⏭️**: Next Song
- **⏹️**: Stop Playback and Disconnect

## Language Support

The bot supports multiple languages. The available language codes are:

- **German**: `de`
- **English**: `en`
- **Italian**: `it`
- **French**: `fr`

### Setting the Language

Change the `"language"` field in your `config.json` to use the desired language:

```json
{
  "language": "en"
}
```

### Adding Your Own Translations

1. Open the `lang.json` file.
2. Add a new language section with the corresponding language code.
3. Translate the texts or adjust them to your needs.

Example:

```json
{
  "es": {
    "no_voice_channel": "¡Debes estar en un canal de voz para que el bot se una!",
    // ... more keys
  }
}
```

## Dependencies

The bot requires the following Python packages:

- **discord.py**
- **yt-dlp**
- **spotipy**
- **PyNaCl**

Install all dependencies with:

```bash
pip install -r requirements.txt
```

**Contents of `requirements.txt`:**

```
discord.py
yt-dlp
spotipy
PyNaCl
```

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository:**

   Click on **"Fork"** to create a copy of the repository in your GitHub account.

2. **Create a New Branch:**

   ```bash
   git checkout -b feature/my-new-feature
   ```

3. **Make Your Changes and Commit:**

   ```bash
   git commit -m "Add feature: My New Feature"
   ```

4. **Push to Your Fork:**

   ```bash
   git push origin feature/my-new-feature
   ```

5. **Open a Pull Request:**

   Go to your repository on GitHub and open a new Pull Request.

---

**Enjoy the Music!** If you encounter any issues or have suggestions for new features, feel free to open an issue or a pull request.

---

**Note**

This bot was developed with a focus on user-friendliness and extensibility. Best practices were followed during implementation to provide a stable and reliable music bot for your Discord community.

**Thank you for using this bot!**