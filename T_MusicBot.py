import discord
from discord.ext import commands, tasks
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
    with open('error.log', 'w'):
        pass
logging.basicConfig(filename='error.log', level=logging.ERROR, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Konfigurationsdatei laden
def load_config():
    try:
        with open('config/config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading config.json: {e}")
        raise
config = load_config()

# Sprachdatei laden
def load_language(language_code):
    try:
        with open('config/lang.json', 'r', encoding='utf-8') as f:
            languages = json.load(f)
            default_language = languages.get('en') or next(iter(languages.values()))
            return languages.get(language_code, default_language)
    except Exception as e:
        logging.error(f"Error loading lang.json: {e}")
        raise
lang = load_language(config['language'])

# Spotify-Authentifizierung
try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=config['spotify_client_id'],
        client_secret=config['spotify_client_secret']
    ))
except Exception as e:
    logging.error(f"Error during Spotify authentication: {e}")
    raise

# Intents aktivieren
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True
intents.reactions = True

# Befehle aus der Config laden
commands_config = config.get('commands', {})
def get_command_info(command_key):
    command_info = commands_config.get(command_key, {})
    name = command_info.get('name', command_key)
    aliases = command_info.get('aliases', [])
    return name, aliases

bot = commands.Bot(command_prefix=config['command_prefix'], intents=intents, help_command=None)

# Globaler Check: Befehle nur im Textkanal des Voice-Channels erlauben
def voice_text_channel_only():
    async def predicate(ctx):
        if not ctx.author.voice or not ctx.author.voice.channel:
            return True
        associated_text = discord.utils.get(ctx.guild.text_channels, name=ctx.author.voice.channel.name)
        if associated_text and ctx.channel.id != associated_text.id:
            await ctx.send(f"Bitte benutze den Textkanal {associated_text.mention}, der zum Voice-Channel gehört!")
            return False
        return True
    return commands.check(predicate)
bot.add_check(voice_text_channel_only())

# Funktionen zum Speichern der Lautstärke
def save_volume(volume):
    global config
    try:
        config['default_volume'] = volume
        with open('config/config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error saving config.json: {e}")

# Globale Variablen
volume = config.get('default_volume', 50)
song_queue = deque()
played_songs = deque()
current_song = None
current_title = None
current_thumbnail = None
now_playing_message = None
is_looping = False
progress_start_time = 0
progress_duration = 0
progress_last_progress = -1
url_cache = {}

### ASYNCHRONE HILFSFUNKTIONEN ###

async def get_spotify_track_info(url):
    def fetch_track_info():
        try:
            info = sp.track(url)
            track_name = info['name']
            artist_name = info['artists'][0]['name']
            album_art = info['album']['images'][0]['url']
            duration_sec = info['duration_ms'] // 1000
            # Wir ignorieren den von Spotify gelieferten Preview-Link (DRM-Problematik)
            preview_url = info.get('preview_url')
            return None, track_name, artist_name, album_art, duration_sec, preview_url
        except Exception as e:
            logging.error(f"Error retrieving Spotify track info: {e}")
            return None, None, None, None, None, None
    return await asyncio.to_thread(fetch_track_info)

async def get_spotify_playlist_tracks(url):
    def fetch_tracks():
        try:
            playlist_id = url.split("playlist/")[1].split("?")[0]
            results = sp.playlist_items(playlist_id)
            tracks = []
            while results:
                for item in results['items']:
                    track = item['track']
                    preview_url = track.get('preview_url')
                    if preview_url:
                        tracks.append(preview_url)
                if results.get('next'):
                    results = sp.next(results)
                else:
                    results = None
            return tracks
        except Exception as e:
            logging.error(f"Error retrieving Spotify playlist tracks: {e}")
            return None
    return await asyncio.to_thread(fetch_tracks)

async def get_first_spotify_track(url):
    def fetch_first_track():
        try:
            playlist_id = url.split("playlist/")[1].split("?")[0]
            results = sp.playlist_items(playlist_id, limit=1)
            item = results['items'][0]
            track = item['track']
            preview_url = track.get('preview_url')
            return preview_url
        except Exception as e:
            logging.error(f"Error retrieving first track of Spotify playlist: {e}")
            return None
    return await asyncio.to_thread(fetch_first_track)

async def get_youtube_url(query):
    return await asyncio.to_thread(get_youtube_url_sync, query)

def get_youtube_url_sync(query):
    if query in url_cache:
        return url_cache[query]
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
    }
    # Mehrere Suchbegriffe ausprobieren, um DRM-geschützte Ergebnisse zu vermeiden
    search_queries = [f"{query} official audio", f"{query} lyrics", f"{query} audio", f"{query} cover"]
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for sq in search_queries:
            try:
                info = ydl.extract_info(f"ytsearch:{sq}", download=False)
                for entry in info.get('entries', []):
                    video_url = entry.get('webpage_url')
                    if not video_url:
                        continue
                    try:
                        candidate = ydl.extract_info(video_url, download=False)
                        if candidate and "DRM" not in str(candidate).upper():
                            url_cache[query] = video_url
                            return video_url
                    except yt_dlp.utils.DownloadError as e:
                        if "DRM" in str(e):
                            continue
            except Exception as e:
                logging.error(f"Error retrieving YouTube link for query '{sq}': {e}")
                continue
    return None

async def get_youtube_playlist_urls(url):
    def fetch_playlist_urls():
        ydl_opts = {'quiet': True, 'extract_flat': True, 'skip_download': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                entries = info.get('entries', [])
                return [f"https://www.youtube.com/watch?v={entry['id']}" for entry in entries if 'id' in entry]
        except Exception as e:
            logging.error(f"Error retrieving YouTube playlist URLs: {e}")
            return None
    return await asyncio.to_thread(fetch_playlist_urls)

def extract_individual_youtube_url(url):
    try:
        if "watch?v=" in url:
            video_id = url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        else:
            return None
        return f"https://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        logging.error(f"Error extracting individual YouTube URL: {e}")
        return None

async def get_song_info_async(url):
    def fetch_song_info():
        ydl_opts = {'format': 'bestaudio/best', 'noplaylist': True, 'quiet': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)
        except Exception as e:
            logging.error(f"Error fetching song info: {e}")
            return None
    return await asyncio.to_thread(fetch_song_info)

### Fortschrittsanzeige ###
@tasks.loop(seconds=5)
async def update_progress_loop(ctx):
    global now_playing_message, progress_start_time, progress_duration, progress_last_progress
    if ctx.voice_client is None or not ctx.voice_client.is_connected():
        update_progress_loop.cancel()
        return
    if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
        update_progress_loop.cancel()
        return
    elapsed = time.time() - progress_start_time
    progress = min(elapsed / progress_duration, 1.0)
    minutes, seconds = divmod(int(elapsed), 60)
    total_minutes, total_seconds = divmod(int(progress_duration), 60)
    progress_bar = create_progress_bar(progress)
    new_progress_level = int(progress * 100) // 5
    if new_progress_level != progress_last_progress:
        progress_last_progress = new_progress_level
        embed = now_playing_message.embeds[0]
        embed.clear_fields()
        embed.add_field(name="Dauer", value=f"{minutes}:{seconds:02d} / {total_minutes}:{total_seconds:02d}", inline=True)
        embed.add_field(name="Fortschritt", value=progress_bar, inline=False)
        embed.title = "⏸️ Jetzt spielt 🎶" if ctx.voice_client.is_paused() else "Jetzt spielt 🎶"
        try:
            await now_playing_message.edit(embed=embed)
        except discord.errors.NotFound:
            update_progress_loop.cancel()
            return
    if elapsed >= progress_duration:
        update_progress_loop.cancel()

def create_progress_bar(progress):
    length = 20
    filled = int(progress * length)
    bar = '▰' * filled + '▱' * (length - filled)
    return f"{bar} {int(progress * 100)}%"

### Events & Commands ###
@bot.event
async def on_ready():
    print(f'Bot ist eingeloggt als {bot.user}')
    for guild in bot.guilds:
        await guild.me.edit(nick='T_MusicBot')

# Play Command
play_name, play_aliases = get_command_info('play')
@bot.command(name=play_name, aliases=play_aliases, help=lang['play_help'])
async def play(ctx, *, url: str):
    if not ctx.author.voice:
        await ctx.send(lang['no_voice_channel'])
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await channel.connect()

    # Spotify Playlist
    if 'open.spotify.com/playlist' in url:
        message = await ctx.send(lang['playlist_load_prompt_spotify'])
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == message.id
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            if str(reaction.emoji) == "✅":
                tracks = await get_spotify_playlist_tracks(url)
                if tracks:
                    await ctx.send(lang['playlist_added_spotify'].format(username=ctx.author.name))
                    for track in tracks:
                        song_queue.append((ctx, track))
                else:
                    await ctx.send(lang['playback_error'])
                    return
            else:
                first_track = await get_first_spotify_track(url)
                if first_track:
                    song_queue.append((ctx, first_track))
                    await ctx.send(lang['song_added_to_queue'].format(username=ctx.author.name))
                else:
                    await ctx.send(lang['playback_error'])
                    return
        except asyncio.TimeoutError:
            await ctx.send(lang['playlist_timeout'])
            return

    # Spotify Track: Wir nutzen ausschließlich YouTube als Fallback
    elif 'open.spotify.com/track' in url:
        _, track_name, artist_name, album_art, duration, _ = await get_spotify_track_info(url)
        fallback_query = f"{artist_name} - {track_name} official audio"
        fallback_url = await get_youtube_url(fallback_query)
        if not fallback_url:
            await ctx.send("Konnte keinen abspielbaren Link für diesen Track finden.")
            return
        preview_url = fallback_url
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(preview_url, executable=config['ffmpeg_path'], **ffmpeg_options),
            volume=volume / 100
        )
        ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(on_finished(ctx), bot.loop))
        await send_now_playing_embed(ctx, f"{artist_name} - {track_name}", duration, album_art)

    # YouTube Playlist
    elif 'youtube.com/playlist' in url or ('list=' in url and 'watch?v=' in url):
        message = await ctx.send(lang['playlist_load_prompt_youtube'])
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == message.id
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            if str(reaction.emoji) == "✅":
                urls = await get_youtube_playlist_urls(url)
                if urls:
                    await ctx.send(lang['playlist_added_youtube'].format(username=ctx.author.name))
                    for video_url in urls:
                        song_queue.append((ctx, video_url))
                else:
                    await ctx.send(lang['playback_error'])
                    return
            else:
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
    global now_playing_message, played_songs, current_song, current_title, current_thumbnail
    if song_queue:
        ctx, url = song_queue.popleft()
        if current_song is not None:
            played_songs.append((ctx, current_song))
        current_song = url
        def fetch_song_info():
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'quiet': True,
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}],
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    return ydl.extract_info(url, download=False)
            except Exception as e:
                logging.error(f"Error fetching song info: {e}")
                return None
        info = await asyncio.to_thread(fetch_song_info)
        if info is None:
            await ctx.send(lang['playback_error'])
            return
        current_thumbnail = info.get('thumbnail', '')
        url2 = info['url']
        current_title = info.get('title', 'Unbekannter Titel')
        duration = info.get('duration', 0)
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(url2, executable=config['ffmpeg_path'], **ffmpeg_options),
            volume=volume / 100
        )
        voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(on_finished(ctx), bot.loop))
        await send_now_playing_embed(ctx, current_title, duration, current_thumbnail)
    else:
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()

async def play_previous_song(voice_client):
    global now_playing_message, played_songs, song_queue, current_song, current_title, current_thumbnail
    if played_songs:
        if current_song is not None:
            song_queue.appendleft((None, current_song))
        ctx, url = played_songs.pop()
        current_song = url
        def fetch_song_info():
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'quiet': True,
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}],
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    return ydl.extract_info(url, download=False)
            except Exception as e:
                logging.error(f"Error fetching song info: {e}")
                return None
        info = await asyncio.to_thread(fetch_song_info)
        if info is None:
            await voice_client.guild.text_channels[0].send(lang['playback_error'])
            return
        current_thumbnail = info.get('thumbnail', '')
        url2 = info['url']
        current_title = info.get('title', 'Unbekannter Titel')
        duration = info.get('duration', 0)
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(url2, executable=config['ffmpeg_path'], **ffmpeg_options),
            volume=volume / 100
        )
        voice_client.stop()
        voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(on_finished(ctx), bot.loop))
        await send_now_playing_embed(ctx, current_title, duration, current_thumbnail)
    else:
        await voice_client.guild.text_channels[0].send(lang['no_previous_song'])

async def on_finished(ctx):
    global is_looping, song_queue, current_song
    if is_looping:
        song_queue.appendleft((ctx, current_song))
    if song_queue:
        await play_next_song(ctx.voice_client)
    else:
        if ctx.voice_client and ctx.voice_client.is_connected():
            await ctx.voice_client.disconnect()

async def send_now_playing_embed(ctx, title, duration, thumbnail_url):
    global now_playing_message, progress_start_time, progress_duration, progress_last_progress
    embed = discord.Embed(
        title="Jetzt spielt 🎶",
        description=f"[**{title}**]({current_song})",
        color=discord.Color.from_rgb(30, 215, 96)
    )
    embed.set_thumbnail(url=thumbnail_url)
    total_minutes, total_seconds = divmod(int(duration), 60)
    embed.add_field(name="Dauer", value=f"{total_minutes}:{total_seconds:02d}", inline=True)
    embed.set_footer(text=config['embed_settings']['footer'])
    if now_playing_message is not None:
        try:
            await now_playing_message.delete()
        except discord.errors.NotFound:
            pass
    now_playing_message = await ctx.send(embed=embed)
    await now_playing_message.add_reaction("⏮️")
    await now_playing_message.add_reaction("⏭️")
    await now_playing_message.add_reaction("⏯️")
    await now_playing_message.add_reaction("⏹️")
    progress_start_time = time.time()
    progress_duration = duration
    progress_last_progress = -1
    update_progress_loop.start(ctx)

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
    if emoji == "⏮️":
        if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
            await play_previous_song(voice_client)
    elif emoji == "⏭️":
        if voice_client and voice_client.is_playing():
            voice_client.stop()
    elif emoji == "⏯️":
        if voice_client and voice_client.is_playing():
            voice_client.pause()
        elif voice_client and voice_client.is_paused():
            voice_client.resume()
    elif emoji == "⏹️":
        if voice_client:
            song_queue.clear()
            voice_client.stop()
            await voice_client.disconnect()
            if now_playing_message:
                try:
                    await now_playing_message.delete()
                except discord.errors.NotFound:
                    pass
                now_playing_message = None
            await guild.text_channels[0].send(lang['playback_stopped_emoji'])
    channel = bot.get_channel(payload.channel_id)
    try:
        message = await channel.fetch_message(payload.message_id)
    except discord.errors.NotFound:
        return
    user = guild.get_member(payload.user_id)
    await message.remove_reaction(payload.emoji, user)

volume_name, volume_aliases = get_command_info('volume')
@bot.command(name=volume_name, aliases=volume_aliases, help=lang['volume_help'])
async def volume_cmd(ctx, value: int = None):
    global volume
    if value is None:
        await ctx.send(lang['volume_prompt'].format(prefix=config['command_prefix']))
        return
    if value < 1 or value > 100:
        await ctx.send(lang['invalid_volume'])
        return
    if ctx.voice_client and ctx.voice_client.source:
        volume = value
        save_volume(volume)
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(lang['volume_set'].format(volume=volume))
    else:
        await ctx.send(lang['no_voice_client'])

pause_name, pause_aliases = get_command_info('pause')
@bot.command(name=pause_name, aliases=pause_aliases, help=lang['pause_help'])
async def pause_cmd(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send(lang['song_paused'])

resume_name, resume_aliases = get_command_info('resume')
@bot.command(name=resume_name, aliases=resume_aliases, help=lang['resume_help'])
async def resume_cmd(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send(lang['song_resumed'])

skip_name, skip_aliases = get_command_info('skip')
@bot.command(name=skip_name, aliases=skip_aliases, help=lang['skip_help'])
async def skip_cmd(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send(lang['song_skipped'])

stop_name, stop_aliases = get_command_info('stop')
@bot.command(name=stop_name, aliases=stop_aliases, help=lang['stop_help'])
async def stop_cmd(ctx):
    global now_playing_message
    if ctx.voice_client:
        song_queue.clear()
        played_songs.clear()
        ctx.voice_client.stop()
        if ctx.voice_client.is_connected():
            await ctx.voice_client.disconnect()
        await ctx.send(lang['song_finished'])
        if now_playing_message:
            try:
                await now_playing_message.delete()
            except discord.errors.NotFound:
                pass
            now_playing_message = None

queue_name, queue_aliases = get_command_info('queue')
@bot.command(name=queue_name, aliases=queue_aliases, help=lang['queue_help'])
async def queue_cmd(ctx):
    print("Queue-Befehl wurde aufgerufen!")
    if song_queue:
        embed = discord.Embed(title="🎶 Warteschlange", color=discord.Color.purple())
        queue_message = await ctx.send(embed=embed)
        for idx, (ctx_item, url) in enumerate(song_queue):
            print(f"Verarbeite Song {idx + 1}: {url}")
            info = await get_song_info_async(url)
            if info:
                title = info.get('title', 'Unbekannter Titel')
                duration = info.get('duration', 0)
                minutes, seconds = divmod(duration, 60)
                embed.add_field(name=f"{idx + 1}. {title} ({minutes}:{seconds:02d})", value=f"[Link]({url})", inline=False)
            else:
                embed.add_field(name=f"{idx + 1}.", value=f"[Link]({url})", inline=False)
            try:
                await queue_message.edit(embed=embed)
            except Exception as e:
                logging.error(f"Error updating queue message: {e}")
            await asyncio.sleep(0.5)
    else:
        print("Die Warteschlange ist leer.")
        await ctx.send(lang['queue_empty'])

help_name, help_aliases = get_command_info('help')
@bot.command(name=help_name, aliases=help_aliases, help=lang['help_help'])
async def help_cmd(ctx):
    embed = discord.Embed(title="Hilfe - Verfügbare Befehle", color=discord.Color.green())
    for command in bot.commands:
        embed.add_field(name=f"{config['command_prefix']}{command.name}", value=command.help, inline=False)
    await ctx.send(embed=embed)

loop_name, loop_aliases = get_command_info('loop')
@bot.command(name=loop_name, aliases=loop_aliases, help=lang['loop_help'])
async def loop_cmd(ctx):
    global is_looping
    is_looping = not is_looping
    if is_looping:
        await ctx.send(lang['loop_enabled'])
    else:
        await ctx.send(lang['loop_disabled'])

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(lang['command_not_found'])
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(lang['missing_argument'])
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(lang['missing_role'])
    else:
        logging.error(f"Unhandled error in command {ctx.command}: {error}")
        await ctx.send(lang['unexpected_error'])

bot.run(config['bot_token'])