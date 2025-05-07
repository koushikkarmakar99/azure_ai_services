import argparse
import sys
from flask import Flask, request, jsonify

sys.path.append('src')
from azure_image_analysis import image_analysis
from setup_logger import setup_logger

app = Flask(__name__)
logger = setup_logger()

@app.route('/')
def index():
    logger.info('Api is up and running')
    return 'Api is up and running'

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    if request.is_json:
        data = request.get_json()
        service_name = data.get('service_name')
        subscription_key = data.get('subscription_key')
        features = data.get('features')
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



    # data = request.get_json()
    # service_name = data.get('service_name') or request.form.get('service_name')
    # subscription_key = data.get('subscription_key') or request
    # features = data.get('features') or request.form.get('features')
    # image_url = data.get('image_url')
    # image_data = None
    
    # if not image_url:
    #     image = request.files.get('image')
    #     image_data = image.read()
    #     image_url = None
    
    try:
        logger.info(f'Service name: {service_name}')
        logger.info(f'Image path: {image_url}')
        logger.info(f'Features: {features}')
        response = image_analysis(service_name, subscription_key, features, image_url, image_data)
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
