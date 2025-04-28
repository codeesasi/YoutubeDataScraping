from flask import Flask, render_template, request, jsonify, Response
import redis
import json
import time
from threading import Thread
import youtubeMetadata
import youtubeComments
from utils import Scraping
app = Flask(__name__, static_folder='static', template_folder='templates')

# Configure Jinja2 to use different delimiters to avoid conflicts with Angular
app.jinja_env.variable_start_string = '{{'
app.jinja_env.variable_end_string = '}}'
app.jinja_env.block_start_string = '{%'
app.jinja_env.block_end_string = '%}'
app.jinja_env.comment_start_string = '{#'
app.jinja_env.comment_end_string = '#}'

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def process_url_in_background(url, task_id):
    try:
        # Update status to processing
        redis_client.set(f"task:{task_id}:status", "Fetching metadata...")
        metadata = youtubeMetadata.process_metadata(url)
        
        redis_client.set(f"task:{task_id}:status", "Downloading comments...")
        Scraping.process_comments(url)
        
        redis_client.set(f"task:{task_id}:status", "Completed")
    except Exception as e:
        redis_client.set(f"task:{task_id}:status", f"Error: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/submit-url', methods=['POST'])
def submit_url():
    data = request.get_json()
    url = data.get('url')
    task_id = str(time.time())  # Simple task ID generation
    
    # Start background processing
    Thread(target=process_url_in_background, args=(url, task_id)).start()
    
    return jsonify({
        'status': 'processing',
        'task_id': task_id,
        'message': 'Processing started'
    })

@app.route('/api/status/<task_id>')
def status_stream(task_id):
    def event_stream():
        while True:
            status = redis_client.get(f"task:{task_id}:status")
            metadata_bytes = redis_client.get(f"task:{task_id}:metadata")
            
            if status:
                status = status.decode('utf-8')
                response_data = {'status': status}
                
                if metadata_bytes:
                    metadata = json.loads(metadata_bytes.decode('utf-8'))
                    response_data['metadata'] = metadata
                
                yield f"data: {json.dumps(response_data)}\n\n"
                
                if status == "Completed" or status.startswith("Error"):
                    break
            time.sleep(0.5)
    
    return Response(event_stream(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)