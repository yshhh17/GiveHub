from redis import Redis
import random
from ..core.config import settings

redis_client = Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)

def generate_otp():
    return str(random.randint(100000, 999999))

def store_otp(email: str, otp: str):
    redis_client.setex(f"otp:{email}", settings.otp_exp, otp)

def verify_otp(email: str, otp: str):
    stored_otp = redis_client.get(f"otp:{email}")
    if stored_otp == otp:
        redis_client.delete(f"otp:{email}")
        return True
    return False