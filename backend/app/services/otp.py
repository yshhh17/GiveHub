from redis import Redis
import random
from ..core.config import settings
import asyncio

redis_client = Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)

def generate_otp():
    return str(random.randint(100000, 999999))

def store_otp(email: str, otp: str):
    redis_client.setex(
        f"otp:{email}",
        int(settings.otp_exp),
        otp
    )