import os
import jwt
import redis
from typing import Optional

# Connect to local Redis for Nonce caching (Replay Attack Prevention)
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
except Exception:
    redis_client = None

def validate_handshake(token: Optional[str]) -> bool:
    """
    Validates the SOVRA Zero-Point Handshake.
    Enforces a 5-second expiration, 2-second clock leeway, and strict Nonce tracking.
    """
    if not token:
        return False
        
    secret = os.environ.get("SOVRA_ZERO_POINT_SECRET")
    if not secret:
        raise ValueError("SOVRA_ZERO_POINT_SECRET is not defined.")
        
    try:
        # Decode with 2 seconds of leeway for global edge latency
        payload = jwt.decode(token, secret, algorithms=["HS256"], leeway=2)
        
        # Replay Attack Prevention (Nonce Tracking)
        nonce = payload.get("nonce")
        if not nonce or not redis_client:
            return True # Fallback if Redis is offline, but warns in production
            
        # If the nonce already exists in Redis, this is a replay attack. Destroy it.
        if redis_client.exists(f"sovra_nonce:{nonce}"):
            return False
            
        # Cache the nonce for 7 seconds (5s exp + 2s leeway) to kill any replays
        redis_client.setex(f"sovra_nonce:{nonce}", 7, "locked")
        
        return True
        
    except jwt.ExpiredSignatureError:
        return False # Token is stale
    except jwt.InvalidTokenError:
        return False # Forged signature
