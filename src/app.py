import argparse
import sys
from flask import Flask, request, jsonify

sys.path.append('src')
# Adding custom modules
from setup_logger import setup_logger
from azure_image_analysis import image_analysis
from azure_text_analysis_nlp import text_analysis_nlp

app = Flask(__name__)
logger = setup_logger()

@app.route('/')
def index():
    logger.info('Api is up and running')
    return 'Api is up and running'

@app.route('/computer-vision/analyze-image/<features>', methods=['POST'])
def analyze_image(features):
    if request.is_json:
        data = request.get_json()
        service_name = data.get('service_name')
        subscription_key = data.get('subscription_key')
        image_url = data.get('image_url')
        image_data = None

        if not all([service_name, subscription_key, image_url, features]):
            return jsonify({'error': 'Missing required parameters'}), 400
    else:
        service_name = request.form.get('service_name')
        subscription_key = request.form.get('subscription_key')
        features = request.form.get('features')
        image = request.files.get('image')
        image_data = image.read()
        image_url = None

        if not all([service_name, subscription_key, image, features]):
            return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        logger.info(f'Service name: {service_name}')
        logger.info(f'Image path: {image_url}')
        logger.info(f'Features: {features}')
        response = image_analysis(service_name, subscription_key, features, image_url, image_data)
        return jsonify(response), 200

    except Exception as error:
        return jsonify({'error': str(error)}), 500

@app.route('/computer-vision/optical-character-recognition', methods=['POST'])
def optical_character_recognition():
    if request.is_json:
        data = request.get_json()
        service_name = data.get('service_name')
        subscription_key = data.get('subscription_key')
        image_url = data.get('image_url')
        image_data = None

        if not all([service_name, subscription_key, image_url]):
            return jsonify({'error': 'Missing required parameters'}), 400
    else:
        service_name = request.form.get('service_name')
        subscription_key = request.form.get('subscription_key')
        image = request.files.get('image')
        image_data = image.read()
        image_url = None

        if not all([service_name, subscription_key, image]):
            return jsonify({'error': 'Missing required parameters'}), 400

    try:
        logger.info(f'Service name: {service_name}')
        logger.info(f'Image path: {image_url}')
        response = image_analysis(service_name, subscription_key, 'read', image_url, image_data)
        return jsonify(response), 200

    except Exception as error:
        return jsonify({'error': str(error)}), 500

@app.route('/nlp/analyze-text/<functionality>', methods=['POST'])
def analyze_text(functionality):
    if request.is_json:
        data = request.get_json()
        service_name = data.get('service_name')
        subscription_key = data.get('subscription_key')
        text = data.get('text')

        if not all([service_name, subscription_key, text]):
            return jsonify({'error': 'Missing required parameters'}), 400
    else:
        service_name = request.form.get('service_name')
        subscription_key = request.form.get('subscription_key')
        text = request.form.get('text')

        if not all([service_name, subscription_key, text]):
            return jsonify({'error': 'Missing required parameters'}), 400

    try:
        logger.info(f'Service name: {service_name}')
        logger.info(f'Text: {text}')
        logger.info(f'Functionality: {functionality}')
        response = text_analysis_nlp(service_name, subscription_key, text, functionality)
        return jsonify(response), 200

    except Exception as error:
        return jsonify({'error': str(error)}), 500

if __name__ == '__main__':
    logger.info('App is starting...')
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    parser.add_argument('--ssl', action='store_true', help='Use SSL')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    if args.ssl:
        logger.info('Using SSL...')
        context = ('cert.pem', 'key.pem')
    else:
        logger.info('Not using SSL...')
        context = None
    logger.info(f'Starting server on port {args.port}...')
    app.run(host='0.0.0.0', port=args.port, ssl_context=context, debug=args.debug)
