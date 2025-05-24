import argparse
import sys
from flask import json
import requests

sys.path.append('src')
from setup_logger import setup_logger
logger = setup_logger()

def image_analysis(service_name, subscription_key, features, image_url = None, image_data = None):
    logger.debug(f'Service name: {service_name}')
    logger.debug(f'Image path: {image_url}')
    logger.debug(f'Features: {features}')
    #url = 'https://ai102azureaiservices002.cognitiveservices.azure.com/vision/v3.2/analyze' # V3.2
    #url = 'https://ai102azureaiservices002.cognitiveservices.azure.com/computervision/imageanalysis:analyze' # V4.0
    url = f'https://{service_name}.cognitiveservices.azure.com/computervision/imageanalysis:analyze'

    if image_url:
        content_type = 'application/json'
        data = {"url": image_url}
    else:
        content_type = 'application/octet-stream'
        data = image_data


    headers = {
        "Content-Type": content_type,
        "Ocp-Apim-Subscription-Key": subscription_key
    }

    # V4.0 Parameters
    params = {
        "api-version": "2024-02-01",
        #"features": "tags,read,caption,denseCaptions,smartCrops,objects,people",
        "features": features,
        "model-version": "latest",
        "details": "Brands",
        "gender-neutral-caption": "true",
        "language": "en"
    }

    try:
        response = requests.post(url=url, json=data, headers=headers, params=params) if image_url else requests.post(url=url, data=data, headers=headers, params=params)
        logger.debug(f'Response text: {response.text}')
        logger.debug(f'Response code: {response.status_code}')
        logger.debug(f'Response headers: {json.dumps(dict(response.headers), indent=4, ensure_ascii=False)}')
        logger.debug(f'Response body: {json.dumps(response.json(), indent=4, ensure_ascii=False)}')
        return response.json()

    except Exception as error:
        logger.error(f'Error: {error}')
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--service-name', type=str, help='Service name')
    parser.add_argument('--subscription-key', type=str, help='Subscription key')
    parser.add_argument('--image-url', type=str, help='Image URL')
    parser.add_argument('--features', type=str, default='tags,read,caption,denseCaptions,smartCrops,objects,people', help='Comma-separated list of features to analyze')
    args = parser.parse_args()
    response = image_analysis(args.service_name, args.subscription_key, args.image_url, args.features)
    
    print(response)
        
