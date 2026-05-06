# YouTube Channel Manager

A Python CLI tool for managing YouTube channels using the YouTube Data API v3.

## Features

- **Authentication**: OAuth2 flow with token management
- **Channel Management**: View channel info and statistics
- **Video Operations**: List, get, update, delete, and upload videos
- **Playlist Management**: Create playlists, add/remove videos
- **Comment Management**: List, add, reply to, and delete comments

## Prerequisites

- Python 3.10+
- Google Cloud Project with YouTube Data API v3 enabled
- OAuth 2.0 credentials (client_secrets.json)

## Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3:
   - Go to APIs & Services > Library
   - Search for "YouTube Data API v3"
   - Click Enable

### 2. Create OAuth Credentials

1. Go to APIs & Services > Credentials
2. Click Create Credentials > OAuth client ID
3. Select "Desktop app" as application type
4. Download the JSON file
5. Rename it to `client_secrets.json`
6. Place it in the project root directory

### 3. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 4. Authenticate

```bash
# First time - will open browser for OAuth flow
python main.py auth login

# Token will be saved to token.json for future use
```

## Usage

### Authentication

```bash
# Login (opens browser for OAuth)
python main.py auth login

# Logout (revoke credentials)
python main.py auth logout
```

### Channel Operations

```bash
# Get channel information
python main.py channel info

# Get channel statistics
python main.py channel stats
```

### Video Operations

```bash
# List videos (default: 50)
python main.py video list
python main.py video list --max 100

# Get video details
python main.py video get VIDEO_ID

# Update video metadata
python main.py video update VIDEO_ID --title "New Title" --description "New desc" --tags tag1 tag2 --privacy public

# Delete video
python main.py video delete VIDEO_ID

# Upload video
python main.py video upload /path/to/video.mp4 --title "My Video" --description "Description" --tags tag1 tag2 --privacy private
```

### Playlist Operations

```bash
# List playlists
python main.py playlist list
python main.py playlist list --max 100

# Create playlist
python main.py playlist create --title "My Playlist" --description "Description" --privacy public

# Add video to playlist
python main.py playlist add PLAYLIST_ID VIDEO_ID

# Remove video from playlist
python main.py playlist remove PLAYLIST_ITEM_ID
```

### Comment Operations

```bash
# List comments on a video
python main.py comment list --video-id VIDEO_ID

# List comments on a channel
python main.py comment list --channel-id CHANNEL_ID

# Add comment to video
python main.py comment add VIDEO_ID "Great video!"

# Reply to comment
python main.py comment reply COMMENT_ID "Thanks!"

# Delete comment
python main.py comment delete COMMENT_ID
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `YOUTUBE_TOKEN_PATH` | Path to store OAuth token | `token.json` |
| `YOUTUBE_CLIENT_SECRETS` | Path to client secrets file | `client_secrets.json` |

## Using as a Python Library

```python
from youtube_manager import YouTubeClient

# Initialize client (will authenticate if needed)
client = YouTubeClient()

# Get channel info
channel = client.get_channel_info()
print(channel["snippet"]["title"])

# List videos
videos = client.list_videos(max_results=10)
for video in videos:
    print(video["snippet"]["title"])

# Upload video
result = client.upload_video(
    "video.mp4",
    title="My Video",
    description="Description",
    tags=["tag1", "tag2"],
    privacy_status="private"
)
print(f"Uploaded: {result['id']}")
```

## Security Notes

- Never commit `client_secrets.json` or `token.json` to version control
- These files are already in `.gitignore`
- Token files are stored locally and can be revoked with `python main.py auth logout`

## Troubleshooting

### "Client secrets file not found"
Ensure `client_secrets.json` is in the project root directory.

### "Access denied" or "Quota exceeded"
Check your Google Cloud Console for API quotas and ensure the YouTube Data API v3 is enabled.

### Token expired
Run `python main.py auth login` to refresh authentication.

## License

MIT
