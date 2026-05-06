"""Video-related operations for YouTube API."""

import os
from googleapiclient.http import MediaFileUpload


class VideoOperations:
    """Operations for YouTube videos."""
    
    def __init__(self, youtube):
        """Initialize with YouTube API service."""
        self.youtube = youtube
    
    def get_video(self, video_id: str) -> dict:
        """Get video details.
        
        Args:
            video_id: YouTube video ID.
        
        Returns:
            Video information dictionary.
        """
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
        
        if not response.get("items"):
            raise ValueError(f"Video not found: {video_id}")
        
        return response["items"][0]
    
    def list_videos(self, channel_id: str | None = None, max_results: int = 50) -> list[dict]:
        """List videos from a channel.
        
        Args:
            channel_id: Channel ID. If None, uses authenticated user's channel.
            max_results: Maximum number of results to return.
        
        Returns:
            List of video dictionaries.
        """
        if channel_id is None:
            channels_request = self.youtube.channels().list(
                part="contentDetails",
                mine=True
            )
            channels_response = channels_request.execute()
            channel_id = channels_response["items"][0]["id"]
        
        uploads_request = self.youtube.channels().list(
            part="contentDetails",
            id=channel_id
        )
        uploads_response = uploads_request.execute()
        uploads_playlist_id = uploads_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        
        videos = []
        next_page_token = None
        
        while True:
            playlist_request = self.youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=min(max_results - len(videos), 50),
                pageToken=next_page_token
            )
            playlist_response = playlist_request.execute()
            
            video_ids = [item["snippet"]["resourceId"]["videoId"] 
                        for item in playlist_response.get("items", [])]
            
            if video_ids:
                videos_request = self.youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=",".join(video_ids)
                )
                videos_response = videos_request.execute()
                videos.extend(videos_response.get("items", []))
            
            next_page_token = playlist_response.get("nextPageToken")
            if not next_page_token or len(videos) >= max_results:
                break
        
        return videos[:max_results]
    
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
        video = self.get_video(video_id)
        snippet = video["snippet"]
        
        if title is not None:
            snippet["title"] = title
        if description is not None:
            snippet["description"] = description
        if tags is not None:
            snippet["tags"] = tags
        if category_id is not None:
            snippet["categoryId"] = category_id
        
        body = {
            "id": video_id,
            "snippet": snippet
        }
        
        if privacy_status is not None:
            body["status"] = {"privacyStatus": privacy_status}
            request = self.youtube.videos().update(
                part="snippet,status",
                body=body
            )
        else:
            request = self.youtube.videos().update(
                part="snippet",
                body=body
            )
        
        return request.execute()
    
    def delete_video(self, video_id: str) -> bool:
        """Delete a video.
        
        Args:
            video_id: YouTube video ID.
        
        Returns:
            True if successful.
        """
        request = self.youtube.videos().delete(id=video_id)
        request.execute()
        return True
    
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
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Video file not found: {file_path}")
        
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status
            }
        }
        
        media = MediaFileUpload(
            file_path,
            mimetype="video/*",
            resumable=True
        )
        
        request = self.youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Upload progress: {int(status.progress() * 100)}%")
        
        return response
    
    def get_video_statistics(self, video_id: str) -> dict:
        """Get video statistics.
        
        Args:
            video_id: YouTube video ID.
        
        Returns:
            Dictionary with view count, like count, comment count.
        """
        video = self.get_video(video_id)
        stats = video["statistics"]
        return {
            "view_count": stats.get("viewCount", 0),
            "like_count": stats.get("likeCount", 0),
            "dislike_count": stats.get("dislikeCount", 0),
            "favorite_count": stats.get("favoriteCount", 0),
            "comment_count": stats.get("commentCount", 0),
        }
