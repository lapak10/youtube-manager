"""Main YouTube API client."""

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from .auth import authenticate
from .channels import ChannelOperations
from .videos import VideoOperations
from .playlists import PlaylistOperations
from .comments import CommentOperations


class YouTubeClient:
    """Client for interacting with YouTube Data API v3."""
    
    def __init__(self, credentials: Credentials | None = None, headless: bool = False):
        """Initialize YouTube client.
        
        Args:
            credentials: Pre-existing credentials. If None, will authenticate.
            headless: If True, use console-based auth flow.
        """
        if credentials is None:
            credentials = authenticate(headless=headless)
        
        self.credentials = credentials
        self.youtube = build("youtube", "v3", credentials=credentials)
        
        self.channels = ChannelOperations(self.youtube)
        self.videos = VideoOperations(self.youtube)
        self.playlists = PlaylistOperations(self.youtube)
        self.comments = CommentOperations(self.youtube)
    
    def get_channel_info(self, channel_id: str | None = None) -> dict:
        """Get channel information.
        
        Args:
            channel_id: Channel ID. If None, returns authenticated user's channel.
        
        Returns:
            Channel information dictionary.
        """
        return self.channels.get_channel(channel_id)
    
    def update_channel(self, title: str | None = None, description: str | None = None,
                       keywords: str | None = None, country: str | None = None) -> dict:
        """Update channel metadata (title, description, keywords, country).
        
        Args:
            title: New channel title.
            description: New channel description.
            keywords: New channel keywords (comma-separated).
            country: New country code (e.g. 'IN', 'US').
        
        Returns:
            Updated channel information.
        """
        return self.channels.update_channel(title, description, keywords, country)
    
    def list_videos(self, channel_id: str | None = None, max_results: int = 50, 
                    include_private: bool = False) -> list[dict]:
        """List videos from a channel.
        
        Args:
            channel_id: Channel ID. If None, uses authenticated user's channel.
            max_results: Maximum number of results to return.
            include_private: If True, include private/unlisted videos.
        
        Returns:
            List of video dictionaries (public only by default).
        """
        return self.videos.list_videos(channel_id, max_results, include_private)
    
    def get_video(self, video_id: str) -> dict:
        """Get video details.
        
        Args:
            video_id: YouTube video ID.
        
        Returns:
            Video information dictionary.
        """
        return self.videos.get_video(video_id)
    
    def update_video(self, video_id: str, title: str | None = None, 
                     description: str | None = None, tags: list[str] | None = None,
                     category_id: str | None = None, privacy_status: str | None = None) -> dict:
        """Update video metadata.
        
        Args:
            video_id: YouTube video ID.
            title: New title (optional).
            description: New description (optional).
            tags: New tags (optional).
            category_id: New category ID (optional).
            privacy_status: New privacy status (optional).
        
        Returns:
            Updated video information.
        """
        return self.videos.update_video(video_id, title, description, tags, category_id, privacy_status)
    
    def delete_video(self, video_id: str) -> bool:
        """Delete a video.
        
        Args:
            video_id: YouTube video ID.
        
        Returns:
            True if successful.
        """
        return self.videos.delete_video(video_id)
    
    def set_thumbnail(self, video_id: str, thumbnail_path: str) -> dict:
        """Set a custom thumbnail for a video.
        
        Args:
            video_id: YouTube video ID.
            thumbnail_path: Path to thumbnail image (JPG/PNG, 1280x720, <2MB).
        
        Returns:
            Thumbnail upload response.
        """
        return self.videos.set_thumbnail(video_id, thumbnail_path)
    
    def upload_video(self, file_path: str, title: str, description: str = "",
                     tags: list[str] | None = None, category_id: str = "22",
                     privacy_status: str = "private") -> dict:
        """Upload a video to YouTube.
        
        Args:
            file_path: Path to video file.
            title: Video title.
            description: Video description.
            tags: List of tags.
            category_id: YouTube category ID (default: 22 = People & Blogs).
            privacy_status: Privacy status (private, public, unlisted).
        
        Returns:
            Uploaded video information.
        """
        return self.videos.upload_video(file_path, title, description, tags, category_id, privacy_status)
    
    def list_playlists(self, channel_id: str | None = None, max_results: int = 50) -> list[dict]:
        """List playlists from a channel.
        
        Args:
            channel_id: Channel ID. If None, uses authenticated user's channel.
            max_results: Maximum number of results to return.
        
        Returns:
            List of playlist dictionaries.
        """
        return self.playlists.list_playlists(channel_id, max_results)
    
    def create_playlist(self, title: str, description: str = "",
                        privacy_status: str = "private") -> dict:
        """Create a new playlist.
        
        Args:
            title: Playlist title.
            description: Playlist description.
            privacy_status: Privacy status.
        
        Returns:
            Created playlist information.
        """
        return self.playlists.create_playlist(title, description, privacy_status)
    
    def add_to_playlist(self, playlist_id: str, video_id: str) -> dict:
        """Add a video to a playlist.
        
        Args:
            playlist_id: Playlist ID.
            video_id: Video ID to add.
        
        Returns:
            Playlist item information.
        """
        return self.playlists.add_video(playlist_id, video_id)
    
    def remove_from_playlist(self, playlist_item_id: str) -> bool:
        """Remove a video from a playlist.
        
        Args:
            playlist_item_id: Playlist item ID.
        
        Returns:
            True if successful.
        """
        return self.playlists.remove_video(playlist_item_id)
    
    def list_comments(self, video_id: str | None = None, 
                      channel_id: str | None = None,
                      max_results: int = 100) -> list[dict]:
        """List comments on a video or channel.
        
        Args:
            video_id: Video ID to get comments from.
            channel_id: Channel ID to get comments from.
            max_results: Maximum number of results.
        
        Returns:
            List of comment dictionaries.
        """
        return self.comments.list_comments(video_id, channel_id, max_results)
    
    def reply_to_comment(self, parent_comment_id: str, text: str) -> dict:
        """Reply to a comment.
        
        Args:
            parent_comment_id: Parent comment ID.
            text: Reply text.
        
        Returns:
            Reply comment information.
        """
        return self.comments.reply_to_comment(parent_comment_id, text)
    
    def delete_comment(self, comment_id: str) -> bool:
        """Delete a comment.
        
        Args:
            comment_id: Comment ID.
        
        Returns:
            True if successful.
        """
        return self.comments.delete_comment(comment_id)
