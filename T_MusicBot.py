import discord
from discord.ext import commands
import yt_dlp
import asyncio
import time
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import deque
import logging
import os

# Fehler-Logging einrichten
if not os.path.exists('error.log'):
    with open('error.log', 'w'):  # Datei erstellen, falls sie nicht existiert
        pass

logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

# Konfigurationsdatei laden
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading config.json: {e}")
        raise

config = load_config()

# Sprachdatei laden
def load_language(lang):
    try:
        with open('lang.json', 'r', encoding='utf-8') as f:
            languages = json.load(f)
            return languages.get(lang, languages['en'])  # Fallback auf Englisch, falls Sprache nicht gefunden wird
    except Exception as e:
        logging.error(f"Error loading lang.json: {e}")
        raise

# Aktuelle Sprache aus der Config laden
lang = load_language(config['language'])

# Spotify-Authentifizierung
try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config['spotify_client_id'], client_secret=config['spotify_client_secret']))
except Exception as e:
    logging.error(f"Error during Spotify authentication: {e}")
    raise

# Intents aktivieren
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True
intents.reactions = True  # Erforderlich für Reaktionen

bot = commands.Bot(command_prefix=config['command_prefix'], intents=intents, help_command=None)

# Funktionen zum Speichern und Laden der Lautstärke
def save_volume(volume):
    try:
        with open('volume.json', 'w', encoding='utf-8') as f:
            json.dump({'volume': volume}, f)
    except Exception as e:
        logging.error(f"Error saving volume.json: {e}")

def load_volume():
    try:
        with open('volume.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('volume', config['default_volume'])
    except Exception as e:
        logging.error(f"Error loading volume.json: {e}")
        return config['default_volume']

# Globale Variablen
volume = load_volume()  # Lautstärke laden
song_queue = deque()  # Warteschlange für Songs
current_song = None  # Aktueller Song
current_title = None  # Aktueller Songtitel
current_thumbnail = None  # Aktuelles Thumbnail
now_playing_message = None  # Nachricht mit dem "Jetzt spielt"-Embed

# Spotify-Songinformationen abrufen
def get_spotify_track_info(url):
    try:
        track_info = sp.track(url)
        track_name = track_info['name']
        artist_name = track_info['artists'][0]['name']
        query = f"{artist_name} {track_name}"
        return query
    except Exception as e:
        logging.error(f"Error retrieving Spotify track info: {e}")
        return None

# Spotify-Playlist-Tracks abrufen
def get_spotify_playlist_tracks(url):
    try:
        playlist_id = url.split("playlist/")[1].split("?")[0]
        results = sp.playlist_items(playlist_id)
        tracks = []
        while results:
            for item in results['items']:
                track = item['track']
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                query = f"{artist_name} {track_name}"
                youtube_url = get_youtube_url(query)
                if youtube_url:
                    tracks.append(youtube_url)
            if results['next']:
                results = sp.next(results)
            else:
                results = None
        return tracks
    except Exception as e:
        logging.error(f"Error retrieving Spotify playlist tracks: {e}")
        return None

# Ersten Track einer Spotify-Playlist abrufen
def get_first_spotify_track(url):
    try:
        playlist_id = url.split("playlist/")[1].split("?")[0]
        results = sp.playlist_items(playlist_id, limit=1)
        item = results['items'][0]
        track = item['track']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        query = f"{artist_name} {track_name}"
        youtube_url = get_youtube_url(query)
        return youtube_url
    except Exception as e:
        logging.error(f"Error retrieving first track of Spotify playlist: {e}")
        return None

# YouTube-Playlist-URLs abrufen
def get_youtube_playlist_urls(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            entries = info.get('entries', [])
            urls = [f"https://www.youtube.com/watch?v={entry['id']}" for entry in entries if 'id' in entry]
            return urls
    except Exception as e:
        logging.error(f"Error retrieving YouTube playlist URLs: {e}")
        return None

# Einzelnen YouTube-Link aus Playlist-URL extrahieren
def extract_individual_youtube_url(url):
    try:
        video_id = None
        if "watch?v=" in url:
            video_id = url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            return None
    except Exception as e:
        logging.error(f"Error extracting individual YouTube URL: {e}")
        return None

# YouTube-Link über den Songnamen und den Künstler abrufen
def get_youtube_url(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,  # Playlists sind nicht erlaubt
        'quiet': True
    }
    search_terms = [f"{query} lyrics", f"{query} audio", f"{query}"]
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for term in search_terms:
            try:
                info = ydl.extract_info(f"ytsearch:{term}", download=False)
                for entry in info['entries']:
                    video_url = entry['webpage_url']
                    try:
                        ydl.extract_info(video_url, download=False)
                        return video_url
                    except yt_dlp.utils.DownloadError as e:
                        if "DRM" in str(e):
                            continue
            except Exception as e:
                logging.error(f"Error retrieving YouTube link: {e}")
                continue
    return None

@bot.event
async def on_ready():
    print(f'Bot ist eingeloggt als {bot.user}')

# Play Command, der den Bot auch joinen lässt
@bot.command(name='play', help='Spielt einen Song oder eine Playlist von YouTube oder Spotify ab.')
async def play(ctx, *, url: str):
    if not ctx.author.voice:
        await ctx.send(lang['no_voice_channel'])
        return

    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await channel.connect()

    # Spotify Playlist
    if 'open.spotify.com/playlist' in url:
        # Sende Nachricht mit Emoji-Reaktionen
        message = await ctx.send(lang['playlist_load_prompt_spotify'])
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == message.id

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            if str(reaction.emoji) == "✅":
                tracks = get_spotify_playlist_tracks(url)
                if tracks:
                    await ctx.send(lang['playlist_added_spotify'].format(username=ctx.author.name))
                    for track in tracks:
                        song_queue.append((ctx, track))
                else:
                    await ctx.send(lang['playback_error'])
                    return
            else:
                # Lade den ersten Track der Playlist
                first_track = get_first_spotify_track(url)
                if first_track:
                    song_queue.append((ctx, first_track))
                    await ctx.send(lang['song_added_to_queue'].format(username=ctx.author.name))
                else:
                    await ctx.send(lang['playback_error'])
                    return
        except asyncio.TimeoutError:
            await ctx.send(lang['playlist_timeout'])
            return

    # Spotify Track
    elif 'open.spotify.com/track' in url:
        query = get_spotify_track_info(url)
        if query:
            youtube_url = get_youtube_url(query)
            if youtube_url:
                song_queue.append((ctx, youtube_url))
                await ctx.send(lang['song_added_to_queue'].format(username=ctx.author.name))
            else:
                await ctx.send(lang['playback_error'])
                return
        else:
            await ctx.send(lang['playback_error'])
            return

    # YouTube Playlist
    elif 'youtube.com/playlist' in url or ('list=' in url and 'watch?v=' in url):
        # Sende Nachricht mit Emoji-Reaktionen
        message = await ctx.send(lang['playlist_load_prompt_youtube'])
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == message.id

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            if str(reaction.emoji) == "✅":
                urls = get_youtube_playlist_urls(url)
                if urls:
                    await ctx.send(lang['playlist_added_youtube'].format(username=ctx.author.name))
                    for video_url in urls:
                        song_queue.append((ctx, video_url))
                else:
                    await ctx.send(lang['playback_error'])
                    return
            else:
                # Lade den individuellen Song
                individual_url = extract_individual_youtube_url(url)
                if individual_url:
                    song_queue.append((ctx, individual_url))
                    await ctx.send(lang['song_added_to_queue'].format(username=ctx.author.name))
                else:
                    await ctx.send(lang['playback_error'])
                    return
        except asyncio.TimeoutError:
            await ctx.send(lang['playlist_timeout'])
            return

    # Einzelner YouTube-Link oder Suchbegriff
    else:
        song_queue.append((ctx, url))
        await ctx.send(lang['song_added_to_queue'].format(username=ctx.author.name))

    if not ctx.voice_client.is_playing():
        await play_next_song(ctx.voice_client)

async def play_next_song(voice_client):
    if song_queue:
        global current_song, current_title, current_thumbnail, now_playing_message
        ctx, url = song_queue.popleft()
        current_song = url
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,  # Playlists sind nicht erlaubt
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                current_thumbnail = info.get('thumbnail', '')
                url2 = info['url']
                current_title = info.get('title', 'Unbekannter Titel')
                duration = info.get('duration', 0)

            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }

            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url2, executable=config['ffmpeg_path'], **ffmpeg_options), volume=volume / 100)
            voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(on_finished(ctx), bot.loop))
            await send_now_playing_embed(ctx, current_title, duration, current_thumbnail)
        except Exception as e:
            logging.error(f"Error playing next song: {e}")
            await ctx.send(f"{lang['playback_error']} {e}")
    else:
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()

async def on_finished(ctx):
    if song_queue:
        await play_next_song(ctx.voice_client)
    else:
        if ctx.voice_client and ctx.voice_client.is_connected():
            await ctx.voice_client.disconnect()

# Fortschrittsbalken mit modernem Design
async def send_now_playing_embed(ctx, title, duration, thumbnail_url):
    global now_playing_message
    embed = discord.Embed(
        title="Jetzt spielt 🎶",
        description=f"[**{title}**]({current_song})",
        color=discord.Color.from_rgb(30, 215, 96)  # Spotify-Grün
    )
    embed.set_thumbnail(url=thumbnail_url)
    total_minutes, total_seconds = divmod(int(duration), 60)
    embed.add_field(name="Dauer", value=f"{total_minutes}:{total_seconds:02d}", inline=True)
    embed.set_footer(text=config['embed_settings']['footer'])

    if now_playing_message is not None:
        try:
            await now_playing_message.delete()
        except discord.errors.NotFound:
            pass  # Nachricht bereits gelöscht

    now_playing_message = await ctx.send(embed=embed)
    await now_playing_message.add_reaction("⏭️")  # Nächster Song
    await now_playing_message.add_reaction("⏯️")  # Pause/Fortsetzen
    await now_playing_message.add_reaction("⏹️")  # Stop

    # Fortschrittsanzeige aktualisieren
    start_time = time.time()
    while True:
        if ctx.voice_client is None or not ctx.voice_client.is_connected():
            break
        if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
            break

        elapsed = time.time() - start_time
        progress = min(elapsed / duration, 1) if duration > 0 else 0
        minutes, seconds = divmod(int(elapsed), 60)
        total_minutes, total_seconds = divmod(int(duration), 60)
        progress_bar = create_progress_bar(progress)

        # Aktualisiere das Embed
        embed.clear_fields()
        embed.add_field(name="Dauer", value=f"{minutes}:{seconds:02d} / {total_minutes}:{total_seconds:02d}", inline=True)
        embed.add_field(name="Fortschritt", value=progress_bar, inline=False)
        if ctx.voice_client.is_paused():
            embed.title = "⏸️ " + "Jetzt spielt 🎶"
        else:
            embed.title = "Jetzt spielt 🎶"

        await now_playing_message.edit(embed=embed)

        await asyncio.sleep(5)  # Aktualisiere alle 5 Sekunden

def create_progress_bar(progress):
    progress_bar_length = 20
    filled_length = int(progress * progress_bar_length)
    bar = '▰' * filled_length + '▱' * (progress_bar_length - filled_length)
    return f"`{bar}`"

# Reaktionen auf Steuerungen
@bot.event
async def on_raw_reaction_add(payload):
    global now_playing_message
    if payload.user_id == bot.user.id:
        return

    if now_playing_message is None or payload.message_id != now_playing_message.id:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        return

    emoji = str(payload.emoji)
    voice_client = guild.voice_client

    if emoji == "⏭️":  # Nächster Song
        if voice_client and voice_client.is_playing():
            voice_client.stop()
    elif emoji == "⏯️":  # Pause oder Fortsetzen
        if voice_client and voice_client.is_playing():
            voice_client.pause()
        elif voice_client and voice_client.is_paused():
            voice_client.resume()
    elif emoji == "⏹️":  # Stop
        if voice_client:
            song_queue.clear()
            voice_client.stop()
            await voice_client.disconnect()
            if now_playing_message:
                try:
                    await now_playing_message.delete()
                except discord.errors.NotFound:
                    pass  # Nachricht bereits gelöscht
                now_playing_message = None
            await guild.text_channels[0].send(lang['playback_stopped_emoji'])

    # Entferne die Reaktion des Benutzers
    channel = bot.get_channel(payload.channel_id)
    try:
        message = await channel.fetch_message(payload.message_id)
    except discord.errors.NotFound:
        return  # Nachricht nicht gefunden, nichts tun
    user = guild.get_member(payload.user_id)
    await message.remove_reaction(payload.emoji, user)

# Volume Command
@bot.command(name='volume', aliases=['vol'], help='Stellt die Lautstärke ein (1-100).')
async def volume_cmd(ctx, value: int = None):
    global volume
    if value is None:
        await ctx.send(lang['volume_prompt'].format(prefix=config['command_prefix']))
        return
    if ctx.voice_client and 1 <= value <= 100:
        volume = value
        save_volume(volume)  # Lautstärke speichern
        if ctx.voice_client.source:
            ctx.voice_client.source.volume = volume / 100
        await ctx.send(lang['volume_set'].format(volume=volume))
    else:
        await ctx.send(lang['invalid_volume'])

# Pause Command
@bot.command(name='pause', help='Pausiert die Wiedergabe.')
async def pause_cmd(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send(lang['song_paused'])

# Resume Command
@bot.command(name='resume', help='Setzt die Wiedergabe fort.')
async def resume_cmd(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send(lang['song_resumed'])

# Skip Command
@bot.command(name='skip', help='Überspringt den aktuellen Song.')
async def skip_cmd(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send(lang['song_skipped'])

# Stop Command
@bot.command(name='stop', help='Stoppt die Wiedergabe und leert die Warteschlange.')
async def stop_cmd(ctx):
    global now_playing_message
    if ctx.voice_client:
        song_queue.clear()
        ctx.voice_client.stop()
        if ctx.voice_client.is_connected():
            await ctx.voice_client.disconnect()
        await ctx.send(lang['song_finished'])
        if now_playing_message:
            try:
                await now_playing_message.delete()
            except discord.errors.NotFound:
                pass  # Nachricht bereits gelöscht
            now_playing_message = None

# Queue Command
@bot.command(name='queue', aliases=['q'], help='Zeigt die aktuelle Warteschlange an.')
async def queue_cmd(ctx):
    if song_queue:
        embed = discord.Embed(title="🎶 Warteschlange", color=discord.Color.purple())
        for idx, (ctx_item, url) in enumerate(song_queue):
            embed.add_field(name=f"{idx + 1}.", value=f"[Link]({url})", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(lang['queue_empty'])

# Hilfe Command
@bot.command(name='help', help='Zeigt diese Hilfe-Nachricht an.')
async def help_cmd(ctx):
    embed = discord.Embed(title="Hilfe - Verfügbare Befehle", color=discord.Color.green())
    for command in bot.commands:
        embed.add_field(name=f"{config['command_prefix']}{command.name}", value=command.help, inline=False)
    await ctx.send(embed=embed)

bot.run(config['bot_token'])