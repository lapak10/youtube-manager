"""Channel-related operations for YouTube API."""


class ChannelOperations:
    """Operations for YouTube channels."""
    
    def __init__(self, youtube):
        """Initialize with YouTube API service."""
        self.youtube = youtube
    
    def get_channel(self, channel_id: str | None = None) -> dict:
        """Get channel information.
        
        Args:
            channel_id: Channel ID. If None, returns authenticated user's channel.
        
        Returns:
            Channel information dictionary.
        """
        if channel_id:
            request = self.youtube.channels().list(
                part="snippet,contentDetails,statistics",
                id=channel_id
            )
        else:
            request = self.youtube.channels().list(
                part="snippet,contentDetails,statistics",
                mine=True
            )
        
        response = request.execute()
        
        if not response.get("items"):
            raise ValueError(f"Channel not found: {channel_id or 'authenticated user'}")
        
        return response["items"][0]
    
    def get_channel_id(self) -> str:
        """Get the authenticated user's channel ID.
        
        Returns:
            Channel ID string.
        """
        channel = self.get_channel()
        return channel["id"]
    
    def get_uploads_playlist_id(self, channel_id: str | None = None) -> str:
        """Get the uploads playlist ID for a channel.
        
        Args:
            channel_id: Channel ID. If None, uses authenticated user's channel.
        
        Returns:
            Uploads playlist ID.
        """
        channel = self.get_channel(channel_id)
        return channel["contentDetails"]["relatedPlaylists"]["uploads"]
    
    def get_channel_statistics(self, channel_id: str | None = None) -> dict:
        """Get channel statistics.
        
        Args:
            channel_id: Channel ID. If None, uses authenticated user's channel.
        
        Returns:
            Dictionary with subscriber count, view count, video count.
        """
        channel = self.get_channel(channel_id)
        stats = channel["statistics"]
        return {
            "subscriber_count": stats.get("subscriberCount", 0),
            "view_count": stats.get("viewCount", 0),
            "video_count": stats.get("videoCount", 0),
            "hidden_subscriber_count": stats.get("hiddenSubscriberCount", False),
        }
    
    def update_channel(self, title: str | None = None, description: str | None = None,
                       keywords: str | None = None, country: str | None = None) -> dict:
        """Update channel metadata.
        
        Args:
            title: New channel title.
            description: New channel description.
            keywords: New channel keywords.
            country: New country code.
        
        Returns:
            Updated channel information.
        """
        channel = self.get_channel()
        
        body = {
            "id": channel["id"],
            "brandingSettings": {
                "channel": {}
            }
        }
        
        if title is not None:
            body["brandingSettings"]["channel"]["title"] = title
        if description is not None:
            body["brandingSettings"]["channel"]["description"] = description
        if keywords is not None:
            body["brandingSettings"]["channel"]["keywords"] = keywords
        if country is not None:
            body["brandingSettings"]["channel"]["country"] = country
        
        request = self.youtube.channels().update(
            part="brandingSettings",
            body=body
        )
        
        return request.execute()
    
    def check_quota(self) -> dict:
        """Check if YouTube API quota is available.
        
        Makes a minimal-cost API call (1 unit) and returns status.
        
        Returns:
            Dictionary with 'available' (bool) and 'message' (str).
        """
        try:
            self.youtube.channels().list(
                part="id",
                mine=True,
                maxResults=1
            ).execute()
            return {"available": True, "message": "Quota available"}
        except Exception as e:
            if "quota" in str(e).lower():
                return {"available": False, "message": "Quota exceeded"}
            raise e
