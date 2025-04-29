"""
Centralized configuration for the post scheduler system.
"""

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Queue names
TASK_QUEUE = 'task_queue'
PROCESSING_QUEUE = 'processing_queue'
COMPLETED_QUEUE = 'completed_queue'
FAILED_QUEUE = 'failed_queue' 