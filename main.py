"""CLI entry point for YouTube Channel Manager."""

import argparse
import json
import sys

from youtube_manager import YouTubeClient


def format_output(data: dict | list, format_type: str = "json") -> str:
    """Format output for display."""
    if format_type == "json":
        return json.dumps(data, indent=2, default=str)
    return str(data)


def main():
    parser = argparse.ArgumentParser(
        description="YouTube Channel Manager - Manage your YouTube channel via CLI",
        prog="youtube-manager"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    auth_parser = subparsers.add_parser("auth", help="Authentication commands")
    auth_subparsers = auth_parser.add_subparsers(dest="auth_command")
    auth_subparsers.add_parser("login", help="Authenticate with YouTube")
    auth_subparsers.add_parser("logout", help="Revoke credentials")
    
    subparsers.add_parser("quota", help="Check YouTube API quota status")
    
    channel_parser = subparsers.add_parser("channel", help="Channel operations")
    channel_subparsers = channel_parser.add_subparsers(dest="channel_command")
    channel_subparsers.add_parser("info", help="Get channel information")
    channel_subparsers.add_parser("stats", help="Get channel statistics")
    update_channel_parser = channel_subparsers.add_parser("update", help="Update channel metadata")
    update_channel_parser.add_argument("--title", help="New channel title")
    update_channel_parser.add_argument("--description", help="New channel description")
    update_channel_parser.add_argument("--keywords", help="Channel keywords (comma-separated)")
    update_channel_parser.add_argument("--country", help="Country code (e.g. IN, US)")
    
    video_parser = subparsers.add_parser("video", help="Video operations")
    video_subparsers = video_parser.add_subparsers(dest="video_command")
    
    list_videos_parser = video_subparsers.add_parser("list", help="List videos")
    list_videos_parser.add_argument("--max", type=int, default=50, help="Max results")
    list_videos_parser.add_argument("--include-private", action="store_true", help="Include private/unlisted videos")
    
    get_video_parser = video_subparsers.add_parser("get", help="Get video details")
    get_video_parser.add_argument("video_id", help="Video ID")
    
    update_video_parser = video_subparsers.add_parser("update", help="Update video")
    update_video_parser.add_argument("video_id", help="Video ID")
    update_video_parser.add_argument("--title", help="New title")
    update_video_parser.add_argument("--description", help="New description")
    update_video_parser.add_argument("--tags", nargs="+", help="New tags")
    update_video_parser.add_argument("--privacy", choices=["private", "public", "unlisted"], help="Privacy status")
    
    delete_video_parser = video_subparsers.add_parser("delete", help="Delete video")
    delete_video_parser.add_argument("video_id", help="Video ID")
    
    upload_parser = video_subparsers.add_parser("upload", help="Upload video")
    upload_parser.add_argument("file", help="Video file path")
    upload_parser.add_argument("--title", required=True, help="Video title")
    upload_parser.add_argument("--description", default="", help="Video description")
    upload_parser.add_argument("--tags", nargs="+", help="Video tags")
    upload_parser.add_argument("--privacy", default="private", choices=["private", "public", "unlisted"], help="Privacy status")
    
    thumbnail_parser = video_subparsers.add_parser("thumbnail", help="Set custom thumbnail for a video")
    thumbnail_parser.add_argument("video_id", help="Video ID (e.g. sKY8e4-SDQg)")
    thumbnail_parser.add_argument("--file", required=True, help="Path to thumbnail image (JPG/PNG, 1280x720 recommended, <2MB)")
    
    playlist_parser = subparsers.add_parser("playlist", help="Playlist operations")
    playlist_subparsers = playlist_parser.add_subparsers(dest="playlist_command")
    
    list_playlists_parser = playlist_subparsers.add_parser("list", help="List playlists")
    list_playlists_parser.add_argument("--max", type=int, default=50, help="Max results")
    
    create_playlist_parser = playlist_subparsers.add_parser("create", help="Create playlist")
    create_playlist_parser.add_argument("--title", required=True, help="Playlist title")
    create_playlist_parser.add_argument("--description", default="", help="Playlist description")
    create_playlist_parser.add_argument("--privacy", default="private", choices=["private", "public", "unlisted"], help="Privacy status")
    
    add_to_playlist_parser = playlist_subparsers.add_parser("add", help="Add video to playlist")
    add_to_playlist_parser.add_argument("playlist_id", help="Playlist ID")
    add_to_playlist_parser.add_argument("video_id", help="Video ID")
    
    remove_from_playlist_parser = playlist_subparsers.add_parser("remove", help="Remove from playlist")
    remove_from_playlist_parser.add_argument("playlist_item_id", help="Playlist item ID")
    
    comment_parser = subparsers.add_parser("comment", help="Comment operations")
    comment_subparsers = comment_parser.add_subparsers(dest="comment_command")
    
    list_comments_parser = comment_subparsers.add_parser("list", help="List comments")
    list_comments_parser.add_argument("--video-id", help="Video ID")
    list_comments_parser.add_argument("--channel-id", help="Channel ID")
    list_comments_parser.add_argument("--max", type=int, default=100, help="Max results")
    
    add_comment_parser = comment_subparsers.add_parser("add", help="Add comment")
    add_comment_parser.add_argument("video_id", help="Video ID")
    add_comment_parser.add_argument("text", help="Comment text")
    
    reply_parser = comment_subparsers.add_parser("reply", help="Reply to comment")
    reply_parser.add_argument("comment_id", help="Comment ID")
    reply_parser.add_argument("text", help="Reply text")
    
    delete_comment_parser = comment_subparsers.add_parser("delete", help="Delete comment")
    delete_comment_parser.add_argument("comment_id", help="Comment ID")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "auth":
            handle_auth(args)
        elif args.command == "quota":
            handle_quota()
        elif args.command == "channel":
            handle_channel(args)
        elif args.command == "video":
            handle_video(args)
        elif args.command == "playlist":
            handle_playlist(args)
        elif args.command == "comment":
            handle_comment(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_auth(args):
    from youtube_manager.auth import authenticate, revoke_credentials
    
    if args.auth_command == "login":
        creds = authenticate()
        print("Successfully authenticated!")
        print(f"Token saved to: {creds.token}")
    elif args.auth_command == "logout":
        if revoke_credentials():
            print("Credentials revoked successfully.")
        else:
            print("No credentials found to revoke.")
    else:
        print("Usage: youtube-manager auth {login|logout}")


def handle_quota():
    """Handle quota check command."""
    client = YouTubeClient()
    status = client.check_quota()
    if status["available"]:
        print("Quota available")
    else:
        print(f"Quota exhausted — {status['message']}")


def handle_channel(args):
    client = YouTubeClient()
    
    if args.channel_command == "info":
        info = client.get_channel_info()
        print(format_output(info))
    elif args.channel_command == "stats":
        stats = client.channels.get_channel_statistics()
        print(format_output(stats))
    elif args.channel_command == "update":
        result = client.update_channel(
            title=args.title,
            description=args.description,
            keywords=args.keywords,
            country=args.country
        )
        print(format_output(result))
    else:
        print("Usage: youtube-manager channel {info|stats}")


def handle_video(args):
    client = YouTubeClient()
    
    if args.video_command == "list":
        videos = client.list_videos(max_results=args.max, include_private=args.include_private)
        print(format_output(videos))
    elif args.video_command == "get":
        video = client.get_video(args.video_id)
        print(format_output(video))
    elif args.video_command == "update":
        result = client.update_video(
            args.video_id,
            title=args.title,
            description=args.description,
            tags=args.tags,
            privacy_status=args.privacy
        )
        print(format_output(result))
    elif args.video_command == "delete":
        client.delete_video(args.video_id)
        print(f"Video {args.video_id} deleted successfully.")
    elif args.video_command == "upload":
        result = client.upload_video(
            args.file,
            title=args.title,
            description=args.description,
            tags=args.tags,
            privacy_status=args.privacy
        )
        print(format_output(result))
    elif args.video_command == "thumbnail":
        result = client.set_thumbnail(args.video_id, args.file)
        print(format_output(result))
    else:
        print("Usage: youtube-manager video {list|get|update|delete|upload}")


def handle_playlist(args):
    client = YouTubeClient()
    
    if args.playlist_command == "list":
        playlists = client.list_playlists(max_results=args.max)
        print(format_output(playlists))
    elif args.playlist_command == "create":
        result = client.create_playlist(
            title=args.title,
            description=args.description,
            privacy_status=args.privacy
        )
        print(format_output(result))
    elif args.playlist_command == "add":
        result = client.add_to_playlist(args.playlist_id, args.video_id)
        print(format_output(result))
    elif args.playlist_command == "remove":
        client.remove_from_playlist(args.playlist_item_id)
        print("Video removed from playlist successfully.")
    else:
        print("Usage: youtube-manager playlist {list|create|add|remove}")


def handle_comment(args):
    client = YouTubeClient()
    
    if args.comment_command == "list":
        comments = client.list_comments(
            video_id=args.video_id,
            channel_id=args.channel_id,
            max_results=args.max
        )
        print(format_output(comments))
    elif args.comment_command == "add":
        result = client.comments.add_comment(args.video_id, args.text)
        print(format_output(result))
    elif args.comment_command == "reply":
        result = client.reply_to_comment(args.comment_id, args.text)
        print(format_output(result))
    elif args.comment_command == "delete":
        client.delete_comment(args.comment_id)
        print("Comment deleted successfully.")
    else:
        print("Usage: youtube-manager comment {list|add|reply|delete}")


if __name__ == "__main__":
    main()
