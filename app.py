from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import configparser
from utils import Scraping

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/update-key', methods=['POST'])
def update_key():
    try:
        data = request.json
        api_key = data.get('api_key')
        
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # Create API section if it doesn't exist
        if 'API' not in config:
            config['API'] = {}
            
        # Set the OpenAI key under the API section
        config['API']['OpenAIKey'] = api_key
        
        with open('config.ini', 'w') as f:
            config.write(f)
        
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error updating config: {str(e)}")  # Add logging
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/get-config', methods=['GET'])
def get_config():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        api_key = config.get('API', 'OpenAIKey', fallback='')
        return jsonify({
            'api_key': api_key if api_key != 'Your-OpenAI-Key-Here' else ''
        })
    except Exception as e:
        print(f"Error reading config: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/remove-key', methods=['POST'])
def remove_key():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        if 'API' in config:
            config['API']['OpenAIKey'] = 'Your-OpenAI-Key-Here'
            with open('config.ini', 'w') as f:
                config.write(f)
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error removing key: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/scraping')
def scraping():
    return render_template('scraping.html')

@app.route('/api/process-metadata', methods=['POST'])
def api_process_metadata():
    try:
        data = request.json
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        result = Scraping.process_metadata(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/youtube-search', methods=['POST'])
def api_youtube_search():
    try:
        data = request.json
        query = data.get('query')
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        results = Scraping.Youtube_search(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
