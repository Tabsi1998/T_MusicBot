# Discord Music Bot 🎶

Un bot de musique Discord riche en fonctionnalités capable de jouer des chansons et des playlists depuis YouTube et Spotify. Il prend en charge plusieurs langues, des contrôles interactifs directement dans Discord et offre un design moderne et convivial.

## Fonctionnalités

- **Jouer de la Musique** : Diffusez des fichiers audio de haute qualité depuis YouTube et Spotify directement dans votre canal vocal.
- **Support de Playlist** : Chargez des playlists entières ou des chansons individuelles depuis YouTube et Spotify.
- **Multilingue** : Support de plusieurs langues (allemand, anglais, italien, français) avec des fichiers de langue facilement modifiables.
- **Contrôle Interactif** : Utilisez des émojis de réaction pour contrôler la lecture directement depuis le message "En cours de lecture" (Lecture/Pause, Chanson suivante, Chanson précédente, Stop).
- **Système de File d'Attente** : Ajoutez des chansons à la file d'attente et affichez la file d'attente actuelle.
- **Contrôle du Volume** : Ajustez le volume de lecture ; les paramètres sont enregistrés entre les sessions.
- **Historique des Chansons** : Revenez aux chansons précédentes et réécoutez-les.
- **Barre de Progression** : Affiche une barre de progression moderne pour la chanson actuelle.
- **Paramètres Persistants** : Les paramètres de volume sont enregistrés et conservés après un redémarrage.
- **Journalisation des Erreurs** : Toutes les erreurs sont enregistrées dans un fichier `error.log`.

## Table des Matières

- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Commandes](#commandes)
- [Support Linguistique](#support-linguistique)
- [Dépendances](#d%C3%A9pendances)
- [Contribuer](#contribuer)
- [Licence](#licence)

## Installation

Pour un guide d'installation détaillé sur un serveur Ubuntu, consultez [Ubuntu-Server_Install.md](Ubuntu-Server_Install.md).

### Prérequis

- **Python 3.8** ou supérieur
- **FFmpeg** : Doit être installé sur le système et le chemin doit être connu.

### Étapes

1. **Cloner le Répertoire :**

   ```bash
   git clone https://github.com/votreutilisateur/votre-nom-de-repo.git
   cd votre-nom-de-repo
   ```

2. **Installer les Paquets Python Nécessaires :**

   Assurez-vous d'avoir installé tous les paquets nécessaires.

   ```bash
   pip install -r requirements.txt
   ```

3. **Installer FFmpeg :**

   - **Windows:** Téléchargez FFmpeg depuis [ffmpeg.org](https://ffmpeg.org/download.html) et ajoutez-le à votre PATH système ou spécifiez le chemin dans `config.json`.
   - **Linux:** Installez-le via le gestionnaire de paquets, par exemple `sudo apt-get install ffmpeg`.
   - **macOS:** Installez-le via Homebrew, par exemple `brew install ffmpeg`.

## Configuration

1. **Créer un Compte Bot Discord :**

   - Allez sur le [Portail des Développeurs Discord](https://discord.com/developers/applications) et créez une nouvelle application.
   - Naviguez vers **"Bot"** et créez un utilisateur bot.
   - Copiez le **Token du Bot**.

2. **Configurer les Identifiants API Spotify (optionnel, pour le support Spotify) :**

   - Créez une nouvelle application dans le [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Copiez le **Client ID** et le **Client Secret**.

3. **Modifier `config.json` :**

   Renommez `config.example.json` en `config.json` et remplissez les détails requis :

   ```json
   {
     "bot_token": "VOTRE_TOKEN_BOT_DISCORD",
     "spotify_client_id": "VOTRE_CLIENT_ID_SPOTIFY",
     "spotify_client_secret": "VOTRE_CLIENT_SECRET_SPOTIFY",
     "language": "fr",
     "command_prefix": "!",
     "default_volume": 50,
     "ffmpeg_path": "ffmpeg",
     "embed_settings": {
       "footer": "Profitez de la musique !"
     },
     "commands": {
       "play": {
         "name": "play",
         "aliases": ["p", "jouermusique", "lancer"]
       },
       "pause": {
         "name": "pause",
         "aliases": ["mettreenpause"]
       },
       "resume": {
         "name": "resume",
         "aliases": ["continuer"]
       },
       "stop": {
         "name": "stop",
         "aliases": ["s", "arrêter", "stopper"]
       },
       "skip": {
         "name": "skip",
         "aliases": ["next", "passer", "suivant"]
       },
       "volume": {
         "name": "volume",
         "aliases": ["vol", "niveau"]
       },
       "queue": {
         "name": "queue",
         "aliases": ["q", "filedattente"]
       },
       "help": {
         "name": "help",
         "aliases": ["h", "aide"]
       },
       "loop": {
         "name": "loop",
         "aliases": ["répéter", "boucle"]
       },
       "setlang": {
         "name": "setlang",
         "aliases": ["langue"]
       }
     }
   }
   ```

   **Remarques :**

   - **`bot_token`**: Votre token bot Discord.
   - **`spotify_client_id` & `spotify_client_secret`**: Vos identifiants API Spotify.
   - **`language`**: Le code de langue pour la langue désirée (`de`, `en`, `it`, `fr`).
   - **`command_prefix`**: Le préfixe pour les commandes du bot (par exemple, `?`).
   - **`default_volume`**: Niveau de volume par défaut (1-100).
   - **`ffmpeg_path`**: Chemin vers l'installation de FFmpeg (`"ffmpeg"`, si c'est dans le PATH système).
   - **`embed_settings`**: Paramètres pour les embeds, par exemple le texte de pied de page.

4. **Vérifier que `lang.json` Existe :**

   Assurez-vous que le fichier `lang.json` est présent dans le répertoire du projet et contient les traductions nécessaires.

## Utilisation

Démarrez le bot avec :

```bash
python python/T_MusicBot.py
```

### Ajouter le Bot à Votre Serveur

1. Allez sur le Portail des Développeurs Discord, sélectionnez votre application et naviguez vers **"OAuth2" > "URL Generator"**.
2. Sélectionnez les scopes **"bot"** et **"applications.commands"**.
3. Sous **Bot Permissions**, sélectionnez les permissions requises :
   - **Permissions Générales** :
     - Lire l'historique des messages
     - Envoyer des messages
     - Gérer les messages
     - Ajouter des réactions
   - **Permissions Vocales** :
     - Rejoindre les canaux vocaux
     - Parler dans les canaux vocaux
4. Copiez l'URL générée et ouvrez-la dans votre navigateur pour ajouter le bot à votre serveur.

## Commandes

- **`!play <URL ou terme de recherche>`** : Joue une chanson ou une playlist depuis YouTube ou Spotify.
  - Prend en charge les liens YouTube et Spotify ainsi que les termes de recherche directs.
- **`!pause`** : Met en pause la lecture actuelle.
- **`!resume`** : Reprend la lecture si elle est en pause.
- **`!skip`** : Passe la chanson actuelle.
- **`!stop`** : Arrête la lecture, vide la file d'attente et se déconnecte.
- **`!volume <1-100>`** : Définit le volume de lecture.
- **`!queue`** : Affiche la file d'attente actuelle des chansons.
- **`!help`** : Affiche le message d'aide avec toutes les commandes disponibles.
- **`!loop`** : Active ou désactive la boucle pour la chanson actuelle.
- **`!setlang <code_langue>`** : Définit la langue du bot (par exemple, `en`, `de`, `it`, `fr`).

### Contrôle Interactif via Réactions

- **⏮️** : Chanson précédente
- **⏯️** : Pause/Reprendre
- **⏭️** : Chanson suivante
- **⏹️** : Arrête la lecture et se déconnecte

## Support Linguistique

Le bot prend en charge plusieurs langues. Les codes de langue disponibles sont :

- **Allemand** : `de`
- **Anglais** : `en`
- **Italien** : `it`
- **Français** : `fr`

### Définir la Langue

Modifiez le champ `"language"` dans votre `config.json` pour utiliser la langue désirée :

```json
{
  "language": "fr"
}
```

### Ajouter Vos Propres Traductions

1. Ouvrez le fichier `lang.json`.
2. Ajoutez une nouvelle section linguistique avec le code de langue correspondant.
3. Traduisez les textes ou ajustez-les selon vos besoins.

Exemple :

```json
{
  "es": {
    "no_voice_channel": "¡Debes estar en un canal de voz para que el bot se una!",
    // ... autres clés
  }
}
```

## Dépendances

Le bot nécessite les paquets Python suivants :

- **discord.py**
- **yt-dlp**
- **spotipy**
- **PyNaCl**

Installez toutes les dépendances avec :

```bash
pip install -r requirements.txt
```

**Contenu de `requirements.txt`:**

```
discord.py
yt-dlp
spotipy
PyNaCl
```

## Contribuer

Les contributions sont les bienvenues ! Veuillez suivre ces étapes :

1. **Forker le Répertoire :**

   Cliquez sur **"Fork"** pour créer une copie du répertoire dans votre compte GitHub.

2. **Créer une Nouvelle Branche :**

   ```bash
   git checkout -b feature/mon-nouveau-feature
   ```

3. **Apporter des Modifications et Committer :**

   ```bash
   git commit -m "Ajoute la fonctionnalité : Mon Nouveau Feature"
   ```

4. **Pusher la Branche :**

   ```bash
   git push origin feature/mon-nouveau-feature
   ```

5. **Ouvrir une Pull Request :**

   Allez dans votre répertoire sur GitHub et ouvrez une nouvelle Pull Request.

## Licence

Ce projet est sous licence [MIT](LICENSE). Voir le fichier `LICENSE` pour plus de détails.

---

**Profitez de la musique !** Si vous rencontrez des problèmes ou avez des suggestions pour de nouvelles fonctionnalités, n'hésitez pas à ouvrir un issue ou une pull request.

---

**Remarque**

Ce bot a été développé avec un focus sur la convivialité et l'extensibilité. Les meilleures pratiques ont été suivies lors de l'implémentation pour fournir un bot de musique stable et fiable pour votre communauté Discord.

**Merci d'utiliser ce bot !**