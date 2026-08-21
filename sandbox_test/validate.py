import os
import json
import jwt
import redis
import sys

os.environ["SOVRA_ZERO_POINT_SECRET"] = "TEST_SECRET_KEY_12345"
from sovra_lock.core import validate_handshake

try:
    data = json.load(sys.stdin)
except Exception as e:
    print(f"JSON Error: {e}")
    sys.exit(1)

valid_token = data.get("valid")
expired_token = data.get("expired")
replay_token = data.get("replay")

print("--- SOVRA SANDBOX AUDIT ---")
print("1. Testing Valid Token...")
res1 = validate_handshake(valid_token)
print(f"Result: {'PASS' if res1 else 'FAIL'}")

print("\n2. Testing Expired Token...")
res2 = validate_handshake(expired_token)
print(f"Result: {'PASS' if not res2 else 'FAIL'} (Expected False)")

print("\n3. Testing Replay Attack (First Attempt)...")
res3 = validate_handshake(replay_token)
print(f"Result: {'PASS' if res3 else 'FAIL'} (Expected True)")

print("\n4. Testing Replay Attack (Second Attempt with same Token)...")
res4 = validate_handshake(replay_token)
print(f"Result: {'PASS' if not res4 else 'FAIL'} (Expected False - Blocked by Redis Nonce)")

if res1 and not res2 and res3 and not res4:
    print("\nOVERALL STATUS: ALL TESTS PASSED. LOCK IS SECURE.")
else:
    print("\nOVERALL STATUS: FAILED. HOLES DETECTED.")
