"""Comment-related operations for YouTube API."""


class CommentOperations:
    """Operations for YouTube comments."""
    
    def __init__(self, youtube):
        """Initialize with YouTube API service."""
        self.youtube = youtube
    
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
        if video_id:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(max_results, 100),
                order="relevance"
            )
        elif channel_id:
            request = self.youtube.commentThreads().list(
                part="snippet",
                allThreadsRelatedToChannelId=channel_id,
                maxResults=min(max_results, 100),
                order="relevance"
            )
        else:
            raise ValueError("Either video_id or channel_id must be provided")
        
        response = request.execute()
        return response.get("items", [])
    
    def get_comment(self, comment_id: str) -> dict:
        """Get a specific comment.
        
        Args:
            comment_id: Comment ID.
        
        Returns:
            Comment information dictionary.
        """
        request = self.youtube.comments().list(
            part="snippet",
            id=comment_id
        )
        response = request.execute()
        
        if not response.get("items"):
            raise ValueError(f"Comment not found: {comment_id}")
        
        return response["items"][0]
    
    def add_comment(self, video_id: str, text: str) -> dict:
        """Add a comment to a video.
        
        Args:
            video_id: Video ID.
            text: Comment text.
        
        Returns:
            Comment thread information.
        """
        body = {
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": text
                    }
                }
            }
        }
        
        request = self.youtube.commentThreads().insert(
            part="snippet",
            body=body
        )
        
        return request.execute()
    
    def reply_to_comment(self, parent_comment_id: str, text: str) -> dict:
        """Reply to a comment.
        
        Args:
            parent_comment_id: Parent comment ID.
            text: Reply text.
        
        Returns:
            Reply comment information.
        """
        body = {
            "snippet": {
                "parentId": parent_comment_id,
                "textOriginal": text
            }
        }
        
        request = self.youtube.comments().insert(
            part="snippet",
            body=body
        )
        
        return request.execute()
    
    def update_comment(self, comment_id: str, text: str) -> dict:
        """Update a comment.
        
        Args:
            comment_id: Comment ID.
            text: New comment text.
        
        Returns:
            Updated comment information.
        """
        body = {
            "id": comment_id,
            "snippet": {
                "textOriginal": text
            }
        }
        
        request = self.youtube.comments().update(
            part="snippet",
            body=body
        )
        
        return request.execute()
    
    def delete_comment(self, comment_id: str) -> bool:
        """Delete a comment.
        
        Args:
            comment_id: Comment ID.
        
        Returns:
            True if successful.
        """
        request = self.youtube.comments().delete(id=comment_id)
        request.execute()
        return True
    
    def mark_comment_as_spam(self, comment_id: str) -> bool:
        """Mark a comment as spam.
        
        Args:
            comment_id: Comment ID.
        
        Returns:
            True if successful.
        """
        request = self.youtube.comments().markAsSpam(id=comment_id)
        request.execute()
        return True
    
    def set_comment_moderation_status(self, comment_id: str, 
                                       moderation_status: str,
                                       ban_author: bool = False) -> bool:
        """Set comment moderation status.
        
        Args:
            comment_id: Comment ID.
            moderation_status: New status (published, heldForReview, rejected).
            ban_author: Whether to ban the comment author.
        
        Returns:
            True if successful.
        """
        request = self.youtube.comments().setModerationStatus(
            id=comment_id,
            moderationStatus=moderation_status,
            banAuthor=ban_author
        )
        request.execute()
        return True
