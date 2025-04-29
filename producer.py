"""
Producer module for adding tasks to the queue and checking their status.
"""

import os
import uuid
from datetime import datetime
import json
from posts import PostScheduler
from redis_client import client as redis_client
from config import TASK_QUEUE, COMPLETED_QUEUE, FAILED_QUEUE

post_scheduler = PostScheduler()

def add_task(task_data, schedule_time):
    """
    Add a task to the queue for later processing
    
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
    """
    Get the status of all queues
    
    Returns:
        dict: Queue status information
    """
    status = {
        'task_queue': redis_client.llen(TASK_QUEUE),
        'completed_queue': redis_client.llen(COMPLETED_QUEUE),
        'failed_queue': redis_client.llen(FAILED_QUEUE),
        'scheduled_posts': len(post_scheduler.get_scheduled_posts())
    }
    return status

def print_queue_status():
    """Print the status of all queues"""
    status = get_queue_status()
    print(f"Queue status: {status}")
    
def get_post_status(post_id):
    """
    Get the status of a specific post
    
    Args:
        post_id (str): The ID of the post
        
    Returns:
        dict: Post status information
    """
    try:
        return post_scheduler.get_post_status(post_id)
    except Exception as e:
        print(f"Failed to get post status: {str(e)}")
        raise

if __name__ == "__main__":
    print("Producer module - use this to add tasks or check status")
    print_queue_status()
    
