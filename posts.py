"""
Post scheduling and publishing core functionality.
"""

import time
from datetime import datetime
import json
import uuid

class PostScheduler:
    """
    Manages the scheduling and publishing of posts to various platforms.
    """
    
    def __init__(self):
        """Initialize the post scheduler with an empty scheduled posts dict"""
        self.scheduled_posts = {}

    def schedule_post(self, post_data, schedule_time):
        """
        Schedule a post for publishing at a specific time.
        
        Args:
            post_data (dict): The post content and metadata
            schedule_time (str): ISO format datetime string when the post should be published
            
        Returns:
            dict: Scheduled post information
            
        Raises:
            ValueError: If schedule time is invalid
            Exception: For other scheduling errors
        """
        try:
            # Convert schedule_time to datetime object
            schedule_datetime = datetime.fromisoformat(schedule_time)
            
            # Validate schedule time is in the future
            if schedule_datetime <= datetime.now():
                raise ValueError("Schedule time must be in the future")
            
            # Create post object
            post = {
                'id': str(uuid.uuid4()),
                'content': post_data.get('content', ''),
                'platform': post_data.get('platform', 'default'),
                'schedule_time': schedule_time,
                'status': 'scheduled',
                'created_at': datetime.now().isoformat()
            }
            
            # Store the post
            self.scheduled_posts[post['id']] = post
            
            return post
            
        except ValueError as e:
            raise ValueError(f"Invalid schedule time: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to schedule post: {str(e)}")

    def publish_post(self, post_id):
        """
        Publish a scheduled post.
        
        Args:
            post_id (str): The ID of the post to publish
            
        Returns:
            bool: True if post was published successfully
            
        Raises:
            ValueError: If post ID is not found
            Exception: For publishing errors
        """
        if post_id not in self.scheduled_posts:
            raise ValueError(f"Post {post_id} not found")
            
        post = self.scheduled_posts[post_id]
        
        try:
            # Here you would implement the actual publishing logic
            # For example, posting to social media platforms
            print(f"Publishing post {post_id}: {post['content']}")
            
            # Update post status
            post['status'] = 'published'
            post['published_at'] = datetime.now().isoformat()
            
            return True
            
        except Exception as e:
            post['status'] = 'failed'
            post['error'] = str(e)
            raise Exception(f"Failed to publish post: {str(e)}")

    def get_scheduled_posts(self):
        """
        Get all scheduled posts
        
        Returns:
            list: All scheduled posts
        """
        return list(self.scheduled_posts.values())

    def get_post_status(self, post_id):
        """
        Get the status of a specific post
        
        Args:
            post_id (str): The ID of the post
            
        Returns:
            dict: Post status information
            
        Raises:
            ValueError: If post ID is not found
        """
        if post_id not in self.scheduled_posts:
            raise ValueError(f"Post {post_id} not found")
        return self.scheduled_posts[post_id]
    