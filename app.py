"""
Flask API for the post scheduler system.
"""

from flask import Flask, request, jsonify
import os
from datetime import datetime
import json
from producer import add_task, get_queue_status, get_post_status

app = Flask(__name__)

@app.route('/schedule', methods=['POST'])
def schedule():
    """
    Schedule a post to be published later
    """
    data = request.json
    post_data = data.get('post_data')
    schedule_time = data.get('schedule_time')
    if not post_data or not schedule_time:
        return jsonify({'error': 'Missing post_data or schedule_time'}), 400
    try:
        task_id = add_task(post_data, schedule_time)
        return jsonify({'task_id': task_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/queue_status', methods=['GET'])
def queue_status():
    """
    Get status of all queues
    """
    status = get_queue_status()
    return jsonify(status)

@app.route('/post_status/<post_id>', methods=['GET'])
def post_status(post_id):
    """
    Get status of a specific post
    """
    try:
        status = get_post_status(post_id)
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)