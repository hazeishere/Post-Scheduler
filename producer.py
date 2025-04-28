#  Queue and publish posts with specific timing requirements.

from redis import Redis
import os
import uuid
from datetime import datetime
import json
from posts import PostScheduler

redis_client = Redis(host='localhost', port=6379, db=0)
post_scheduler = PostScheduler()

TASK_QUEUE = 'task_queue'

def add_task(task_data, schedule_time):
    """
    Add a task to the regular queue
    
    Args:
        task_data (dict): Post content and metadata
        schedule_time (str): ISO format datetime string
        
    Returns:
        str: Task ID
    """
    try:
        # Schedule the post
        post = post_scheduler.schedule_post(task_data, schedule_time)
        
        # Create task object
        task = {
            'id': post['id'],
            'data': post,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }

        # Add to Redis queue
        redis_client.lpush(TASK_QUEUE, json.dumps(task))
        print(f"Added task {task['id']} to queue")
        return task['id']
        
    except Exception as e:
        print(f"Failed to add task: {str(e)}")
        raise

def get_queue_status():
    """Get the status of all queues"""
    status = {
        'task_queue': redis_client.llen(TASK_QUEUE),
        'scheduled_posts': len(post_scheduler.get_scheduled_posts())
    }
    return status

def print_queue_status():
    """Print the status of all queues"""
    status = get_queue_status()
    print(f"Queue status: {status}")
    
def get_post_status(post_id):
    """Get the status of a specific post"""
    try:
        return post_scheduler.get_post_status(post_id)
    except Exception as e:
        print(f"Failed to get post status: {str(e)}")
        raise
    
