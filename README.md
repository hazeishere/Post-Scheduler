# Social Media Post Scheduler

A simple Flask API that allows scheduling social media posts using Redis as a task queue.

## Setup

1. Make sure you have Python 3.8+ installed
2. Install Redis on your system
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Start the Redis server
5. Run the application:
   ```
   python app.py
   ```

## API Endpoints

### Schedule a Post

```
POST /schedule
```

Request body:
```json
{
  "content": "Your post content here",
  "platform": "twitter",
  "scheduled_time": "2028-09-15T14:30:00"
}
```

Supported platforms: twitter, facebook, instagram, linkedin

### Get Scheduled Posts

```
GET /posts
```

Returns all currently scheduled posts.

### Delete a Scheduled Post

```
DELETE /posts/{task_id}
```

Deletes a scheduled post with the given task ID.

### Get Post History

```
GET /history
```

Returns the history of all posts that have been processed.

## How It Works

1. The app uses a Redis sorted set to store scheduled posts with the scheduled time as the score
2. A background worker thread continuously checks for posts that are due
3. When a post is due, it's processed (posted to social media) and removed from the queue
4. Post results are stored in Redis for history tracking 