"""Password and opaque session-token primitives used by authentication routes."""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from pwdlib import PasswordHash

from app.core.config import settings


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def generate_token() -> str:
    """Generate a high-entropy opaque token safe to send to a client once."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """Create a deterministic database-safe representation of an opaque token."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def verification_expiry() -> datetime:
    return utc_now() + timedelta(minutes=settings.verification_token_ttl_minutes)


def session_expiry() -> datetime:
    return utc_now() + timedelta(minutes=settings.session_token_ttl_minutes)
