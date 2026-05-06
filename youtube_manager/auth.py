"""OAuth2 authentication for YouTube API."""

import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtubepartner",
]

DEFAULT_TOKEN_PATH = "token.json"
DEFAULT_CLIENT_SECRETS_PATH = "client_secrets.json"


def get_credentials_path() -> str:
    """Get the path to store credentials."""
    return os.environ.get("YOUTUBE_TOKEN_PATH", DEFAULT_TOKEN_PATH)


def get_client_secrets_path() -> str:
    """Get the path to client secrets file."""
    return os.environ.get("YOUTUBE_CLIENT_SECRETS", DEFAULT_CLIENT_SECRETS_PATH)


def load_credentials() -> Credentials | None:
    """Load saved credentials from file."""
    token_path = get_credentials_path()
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            return creds
        except Exception:
            return None
    return None


def save_credentials(creds: Credentials) -> None:
    """Save credentials to file."""
    token_path = get_credentials_path()
    with open(token_path, "w") as f:
        f.write(creds.to_json())


def authenticate(client_secrets_path: str | None = None, headless: bool = False) -> Credentials:
    """Authenticate with YouTube API using OAuth2.
    
    Args:
        client_secrets_path: Path to client_secrets.json file.
        headless: If True, use console-based auth flow (no browser).
    
    Returns:
        Valid credentials object.
    """
    creds = load_credentials()
    
    if creds and creds.valid:
        return creds
    
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            save_credentials(creds)
            return creds
        except Exception:
            creds = None
    
    secrets_path = client_secrets_path or get_client_secrets_path()
    
    if not os.path.exists(secrets_path):
        raise FileNotFoundError(
            f"Client secrets file not found: {secrets_path}\n"
            f"Download it from Google Cloud Console:\n"
            f"https://console.cloud.google.com/apis/credentials\n"
            f"Save as: {DEFAULT_CLIENT_SECRETS_PATH}"
        )
    
    flow = InstalledAppFlow.from_client_secrets_file(secrets_path, SCOPES)
    
    if headless:
        creds = flow.run_console()
    else:
        creds = flow.run_local_server(port=0)
    
    save_credentials(creds)
    return creds


def revoke_credentials() -> bool:
    """Revoke stored credentials."""
    creds = load_credentials()
    if creds:
        try:
            creds.revoke(Request())
        except Exception:
            pass
        token_path = get_credentials_path()
        if os.path.exists(token_path):
            os.remove(token_path)
        return True
    return False
