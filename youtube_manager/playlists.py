"""Playlist-related operations for YouTube API."""


class PlaylistOperations:
    """Operations for YouTube playlists."""
    
    def __init__(self, youtube):
        """Initialize with YouTube API service."""
        self.youtube = youtube
    
    def list_playlists(self, channel_id: str | None = None, max_results: int = 50) -> list[dict]:
        """List playlists from a channel.
        
        Args:
            channel_id: Channel ID. If None, uses authenticated user's channel.
            max_results: Maximum number of results to return.
        
        Returns:
            List of playlist dictionaries.
        """
        if channel_id:
            request = self.youtube.playlists().list(
                part="snippet,contentDetails",
                channelId=channel_id,
                maxResults=max_results
            )
        else:
            request = self.youtube.playlists().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=max_results
            )
        
        response = request.execute()
        return response.get("items", [])
    
    def get_playlist(self, playlist_id: str) -> dict:
        """Get playlist details.
        
        Args:
            playlist_id: Playlist ID.
        
        Returns:
            Playlist information dictionary.
        """
        request = self.youtube.playlists().list(
            part="snippet,contentDetails",
            id=playlist_id
        )
        response = request.execute()
        
        if not response.get("items"):
            raise ValueError(f"Playlist not found: {playlist_id}")
        
        return response["items"][0]
    
    def create_playlist(self, title: str, description: str = "",
                        privacy_status: str = "private") -> dict:
        """Create a new playlist.
        
        Args:
            title: Playlist title.
            description: Playlist description.
            privacy_status: Privacy status (private, public, unlisted).
        
        Returns:
            Created playlist information.
        """
        body = {
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {
                "privacyStatus": privacy_status
            }
        }
        
        request = self.youtube.playlists().insert(
            part="snippet,status",
            body=body
        )
        
        return request.execute()
    
    def update_playlist(self, playlist_id: str, title: str | None = None,
                        description: str | None = None,
                        privacy_status: str | None = None) -> dict:
        """Update playlist metadata.
        
        Args:
            playlist_id: Playlist ID.
            title: New title (optional).
            description: New description (optional).
            privacy_status: New privacy status (optional).
        
        Returns:
            Updated playlist information.
        """
        playlist = self.get_playlist(playlist_id)
        snippet = playlist["snippet"]
        
        if title is not None:
            snippet["title"] = title
        if description is not None:
            snippet["description"] = description
        
        body = {
            "id": playlist_id,
            "snippet": snippet
        }
        
        if privacy_status is not None:
            body["status"] = {"privacyStatus": privacy_status}
            request = self.youtube.playlists().update(
                part="snippet,status",
                body=body
            )
        else:
            request = self.youtube.playlists().update(
                part="snippet",
                body=body
            )
        
        return request.execute()
    
    def delete_playlist(self, playlist_id: str) -> bool:
        """Delete a playlist.
        
        Args:
            playlist_id: Playlist ID.
        
        Returns:
            True if successful.
        """
        request = self.youtube.playlists().delete(id=playlist_id)
        request.execute()
        return True
    
    def list_playlist_items(self, playlist_id: str, max_results: int = 50) -> list[dict]:
        """List items in a playlist.
        
        Args:
            playlist_id: Playlist ID.
            max_results: Maximum number of results.
        
        Returns:
            List of playlist item dictionaries.
        """
        request = self.youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=max_results
        )
        response = request.execute()
        return response.get("items", [])
    
    def add_video(self, playlist_id: str, video_id: str,
                  position: int | None = None) -> dict:
        """Add a video to a playlist.
        
        Args:
            playlist_id: Playlist ID.
            video_id: Video ID to add.
            position: Position in playlist (optional).
        
        Returns:
            Playlist item information.
        """
        body = {
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
        
        if position is not None:
            body["snippet"]["position"] = position
        
        request = self.youtube.playlistItems().insert(
            part="snippet",
            body=body
        )
        
        return request.execute()
    
    def remove_video(self, playlist_item_id: str) -> bool:
        """Remove a video from a playlist.
        
        Args:
            playlist_item_id: Playlist item ID.
        
        Returns:
            True if successful.
        """
        request = self.youtube.playlistItems().delete(id=playlist_item_id)
        request.execute()
        return True
    
    def update_playlist_item(self, playlist_item_id: str, video_id: str,
                             title: str | None = None, description: str | None = None,
                             position: int | None = None) -> dict:
        """Update a playlist item.
        
        Args:
            playlist_item_id: Playlist item ID.
            video_id: Video ID.
            title: New title (optional).
            description: New description (optional).
            position: New position (optional).
        
        Returns:
            Updated playlist item information.
        """
        body = {
            "id": playlist_item_id,
            "snippet": {
                "playlistId": playlist_item_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
        
        if title is not None:
            body["snippet"]["title"] = title
        if description is not None:
            body["snippet"]["description"] = description
        if position is not None:
            body["snippet"]["position"] = position
        
        request = self.youtube.playlistItems().update(
            part="snippet",
            body=body
        )
        
        return request.execute()
