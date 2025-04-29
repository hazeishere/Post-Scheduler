# Post Scheduler

A simple project to queue and publish posts with specific timing requirements using Python, Flask, and Redis.

## Features
- Schedule posts for future publishing
- Queue management using Redis
- REST API for scheduling and status
- Worker process to publish posts at the right time

## Project Structure
- `config.py` - Centralized configuration settings
- `redis_client.py` - Shared Redis client instance
- `posts.py` - Core post scheduling functionality
- `producer.py` - Adds tasks to the queue and checks status
- `worker.py` - Processes tasks from the queue
- `app.py` - Flask API for interacting with the system

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Redis server:**
   Make sure you have Redis running locally (default: localhost:6379).

3. **Run the Flask app:**
   ```bash
   python app.py
   ```

4. **Start the worker in another terminal:**
   ```bash
   python worker.py
   ```

## API Usage

### Schedule a Post
- **POST** `/schedule`
- **Body:**
  ```json
  {
    "post_data": {"content": "Hello, world!", "platform": "twitter"},
    "schedule_time": "2024-03-20T15:30:00"
  }
  ```
- **Response:**
  ```json
  {"task_id": "..."}
  ```

### Check Queue Status
- **GET** `/queue_status`
- **Response:**
  ```json
  {
    "task_queue": 1,
    "completed_queue": 0,
    "failed_queue": 0, 
    "scheduled_posts": 1
  }
  ```

### Check Post Status
- **GET** `/post_status/<task_id>`
- **Response:**
  ```json
  {
    "id": "...",
    "content": "Hello, world!",
    "platform": "twitter",
    "schedule_time": "2024-03-20T15:30:00",
    "status": "scheduled",
    "created_at": "..."
  }
  ```

## Command Line Usage
You can also use the modules directly:

```bash
# Start the worker
python worker.py

# Check queue status
python producer.py
```

## Notes
- This is a learning/demo project. For production, use persistent storage for posts and add authentication.
- The worker currently processes tasks as they are added to the queue. 