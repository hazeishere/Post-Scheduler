import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def test_schedule_post():
    # Schedule a post for 30 seconds from now
    scheduled_time = (datetime.now() + timedelta(seconds=30)).isoformat()
    
    payload = {
        "content": "This is a test post from our scheduler!",
        "platform": "twitter",
        "scheduled_time": scheduled_time
    }
    
    response = requests.post(f"{BASE_URL}/schedule", json=payload)
    print("Schedule post response:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    return response.json().get("task_id")

def test_get_scheduled_posts():
    response = requests.get(f"{BASE_URL}/posts")
    print("\nScheduled posts:")
    print(json.dumps(response.json(), indent=2))

def test_delete_post(task_id):
    response = requests.delete(f"{BASE_URL}/posts/{task_id}")
    print(f"\nDelete post {task_id} response:", response.status_code)
    print(json.dumps(response.json(), indent=2))

def test_get_history():
    response = requests.get(f"{BASE_URL}/history")
    print("\nPost history:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("Testing the Social Media Post Scheduler API")
    print("------------------------------------------")
    
    # Schedule a post
    task_id = test_schedule_post()
    
    # Get scheduled posts
    test_get_scheduled_posts()
    
    # Uncomment to test deleting a post
    # test_delete_post(task_id)
    # test_get_scheduled_posts()
    
    print("\nWait 40 seconds for the post to be processed...")
    
    # Wait for the worker to process the post
    import time
    time.sleep(40)
    
    # Check history
    test_get_history()
    
    print("\nTest complete!") 