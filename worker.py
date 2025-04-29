"""
Worker module that processes tasks from the Redis queue and publishes posts.
"""

import json
import time
from datetime import datetime
from posts import PostScheduler
from redis_client import client as redis_client
from config import TASK_QUEUE, PROCESSING_QUEUE, COMPLETED_QUEUE, FAILED_QUEUE

post_scheduler = PostScheduler()

def process_task(task):
    """
    Process a single task: publish the post using PostScheduler
    
    Args:
        task (dict): Task data containing post information
        
    Returns:
        dict: Processed task with updated status
    """
    print(f"Processing task {task['id']}")
    try:
        # Actually publish the post
        post_id = task['id']
        post_scheduler.scheduled_posts[post_id] = task['data']
        post_scheduler.publish_post(post_id)
        task['status'] = 'completed'
        task['completed_at'] = datetime.now().isoformat()
        print(f"Completed task {task['id']}")
        return task
    except Exception as e:
        print(f"Error publishing post {task['id']}: {str(e)}")
        task['status'] = 'failed'
        task['error'] = str(e)
        task['failed_at'] = datetime.now().isoformat()
        return task

def work():
    """
    Main worker loop - continuously process tasks from the queue
    """
    print("Worker started. Waiting for tasks...")
    while True:
        result = redis_client.brpop(TASK_QUEUE, timeout=1)
        if not result:
            continue
        _, task_data = result
        task = json.loads(task_data)
        task['status'] = 'processing'
        task['processing_started'] = datetime.now().isoformat()
        redis_client.lpush(PROCESSING_QUEUE, json.dumps(task))
        processed_task = process_task(task)
        redis_client.lrem(PROCESSING_QUEUE, 1, json.dumps(task))
        if processed_task['status'] == 'completed':
            redis_client.lpush(COMPLETED_QUEUE, json.dumps(processed_task))
        else:
            redis_client.lpush(FAILED_QUEUE, json.dumps(processed_task))

if __name__ == "__main__":
    work()