"""YouTube Channel Manager - A Python tool for managing YouTube channels."""

from .client import YouTubeClient
from .auth import authenticate

__version__ = "1.0.0"
__all__ = ["YouTubeClient", "authenticate"]
