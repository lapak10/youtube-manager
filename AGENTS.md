# AGENTS.md — Instructions for AI Agents

## Project: YouTube Manager

A Python CLI tool to manage a YouTube channel via the YouTube Data API v3.

## How to Run

Always activate the virtual environment first:

```bash
source venv/bin/activate
```

All commands are run via the CLI entry point:

```bash
python main.py <command>
```

## Project Structure

```
main.py                          # CLI entry point (argparse)
youtube_manager/
  __init__.py                    # Exports YouTubeClient, authenticate
  auth.py                        # OAuth2 auth, token management
  client.py                      # YouTubeClient — top-level API facade
  channels.py                    # ChannelOperations — channel CRUD
  videos.py                      # VideoOperations — video CRUD, thumbnails
  playlists.py                   # PlaylistOperations — playlist CRUD
  comments.py                    # CommentOperations — comment CRUD
```

## Authentication

- Token stored at `token.json` (auto-refreshes)
- Client secrets at `client_secrets.json`
- Both are gitignored. NEVER commit them.
- To (re)authenticate: `python main.py auth login`

## Available Commands

| Command | Description |
|---------|-------------|
| `auth login` | Authenticate with YouTube (OAuth2) |
| `auth logout` | Revoke credentials |
| `channel info` | Get channel metadata |
| `channel stats` | Get subscriber/view/video counts |
| `channel update --description "..." --keywords "..." --country IN` | Update channel branding |
| `video list` | List public videos (--max N, --include-private for all) |
| `video get <id>` | Get video details |
| `video update <id> --title "..." --description "..."` | Update video metadata |
| `video thumbnail <id> --file thumb.jpg` | Set custom thumbnail (1280x720, <2MB, JPG/PNG) |
| `video delete <id>` | Delete a video |
| `video upload <file> --title "..."` | Upload a new video |
| `playlist list/create/add/remove` | Manage playlists |
| `comment list/add/reply/delete` | Manage comments |

## Common AI Agent Tasks

### List all videos with stats in readable format
```python
from youtube_manager import YouTubeClient
client = YouTubeClient()

videos = client.list_videos(max_results=50)
for v in videos:
    s = v['snippet']
    stats = v['statistics']
    print(f"{v['id']} | {stats.get('viewCount',0)} views | {s['localized']['title'][:50]}")
```

### Check if a video has auto captions (ASR)
```python
caps = client.youtube.captions().list(part='snippet', videoId=vid).execute()
asr = [i for i in caps.get('items', []) if i['snippet']['trackKind'] == 'asr']
if asr:
    text = client.youtube.captions().download(id=asr[0]['id'], tfmt='srt').execute()
```

### Update multiple videos at once (watch for rate limits)
```python
for vid_id, title, desc in updates:
    client.update_video(video_id=vid_id, title=title, description=desc)
```

### Get only public videos
```python
videos = client.list_videos(include_private=False)
# Filters out private/unlisted in videos.py
```

## Channel Context

- Channel: **Anand Kumar** (`@iamanandkmk`)
- Content: Standup comedy, open mic performances, Hinglish humor
- Topics: UP culture, Bollywood roasts, desi daily life, men-vs-women, India-Pakistan jokes
- Audience: Hindi/Hinglish speakers, Indian viewers
- Issues to watch for: duplicate titles, empty descriptions, missing thumbnails, auto-generated titles
