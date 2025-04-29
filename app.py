import os
from datetime import datetime
from flask import Flask, request, jsonify
import redis
import json
import threading
import time
import requests  # For actual social media posting

app = Flask(__name__)

# Configure Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Mock social media platforms - in a real app, you'd use actual API clients
PLATFORMS = ['twitter', 'facebook', 'instagram', 'linkedin']

@app.route('/schedule', methods=['POST'])
def schedule_post():
    """Schedule a social media post for later delivery"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    required_fields = ['content', 'platform', 'scheduled_time']
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields. Need: {', '.join(required_fields)}"}), 400
        
    if data['platform'].lower() not in PLATFORMS:
        return jsonify({"error": f"Platform must be one of: {', '.join(PLATFORMS)}"}), 400
    
    try:
        scheduled_time = datetime.fromisoformat(data['scheduled_time'])
        if scheduled_time < datetime.now():
            return jsonify({"error": "Cannot schedule posts in the past"}), 400
    except ValueError:
        return jsonify({"error": "Invalid time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}), 400
    
    # Create a task with a unique ID
    task_id = f"post:{int(time.time())}"
    task_data = {
        "id": task_id,
        "content": data['content'],
        "platform": data['platform'].lower(),
        "scheduled_time": data['scheduled_time'],
        "status": "scheduled",
        "created_at": datetime.now().isoformat()
    }
    
    # Add to Redis sorted set with score as unix timestamp for scheduled time
    score = int(scheduled_time.timestamp())
    redis_client.zadd("scheduled_posts", {json.dumps(task_data): score})
    
    return jsonify({"message": "Post scheduled successfully", "task_id": task_id}), 201

@app.route('/posts', methods=['GET'])
def get_scheduled_posts():
    """Get all scheduled posts"""
    posts = []
    # Get all posts from the Redis sorted set
    raw_posts = redis_client.zrange("scheduled_posts", 0, -1, withscores=True)
    
    for post_json, score in raw_posts:
        post = json.loads(post_json)
        post['scheduled_timestamp'] = score
        posts.append(post)
    
    return jsonify({"posts": posts})

@app.route('/posts/<task_id>', methods=['DELETE'])
def delete_post(task_id):
    """Delete a scheduled post"""
    found = False
    posts = redis_client.zrange("scheduled_posts", 0, -1)
    
    for post_json in posts:
        post = json.loads(post_json)
        if post['id'] == task_id:
            redis_client.zrem("scheduled_posts", post_json)
            found = True
            break
    
    if found:
        return jsonify({"message": "Post deleted successfully"}), 200
    else:
        return jsonify({"error": "Post not found"}), 404

def post_to_social_media(platform, content):
    """
    Mock function to post to social media
    In a real app, this would use the appropriate API client for each platform
    """
    print(f"Posting to {platform}: {content}")
    # Example implementation for actual API calls would go here
    # e.g., twitter_client.post(content) or facebook_client.post(content)
    return True

def worker():
    """Background worker that checks for posts that are due"""
    while True:
        current_time = int(time.time())
        # Get all posts that are due (score <= current time)
        due_posts = redis_client.zrangebyscore("scheduled_posts", 0, current_time)
        
        for post_json in due_posts:
            post = json.loads(post_json)
            print(f"Processing post: {post['id']}")
            
            try:
                # Post to the social media platform
                success = post_to_social_media(post['platform'], post['content'])
                
                # Remove the post from the queue regardless of success
                # In a real app, you might want to handle failures differently
                redis_client.zrem("scheduled_posts", post_json)
                
                # Store the result
                post['status'] = "completed" if success else "failed"
                post['completed_at'] = datetime.now().isoformat()
                redis_client.hset("post_history", post['id'], json.dumps(post))
                
            except Exception as e:
                print(f"Error processing post {post['id']}: {str(e)}")
                # Could implement retry logic here
        
        # Sleep for a while before checking again
        time.sleep(5)

@app.route('/history', methods=['GET'])
def get_post_history():
    """Get history of posted items"""
    history = []
    all_history = redis_client.hgetall("post_history")
    
    for _, post_json in all_history.items():
        history.append(json.loads(post_json))
    
    return jsonify({"history": history})

if __name__ == '__main__':
    # Start the worker in a background thread
    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()
    
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
