"""
Shared Redis client module for the post scheduler system.
"""

from redis import Redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

# Create a shared Redis client instance
client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB) 