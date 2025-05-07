import argparse
import sys
from flask import json
import requests

sys.path.append('src')
from setup_logger import setup_logger
logger = setup_logger()

def text_analysis_nlp(service_name, subscription_key, text, functionality):
    logger.info(f'Service name: {service_name}')
    logger.info(f'Text: {text}')
    logger.info(f'Functionality: {functionality}')
    url = f'https://{service_name}.cognitiveservices.azure.com/language/:analyze-text'

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Ocp-Apim-Subscription-Key": subscription_key
    }

    params = {
        "api-version": "2023-11-15-preview",
        "showStats": True
    }

    body = {
        "kind": functionality,
        "parameters": {
            "modelversion": "latest",
        },
        "analysisInput": {
            "documents": [
                {
                    "id": "1",
                    "text": text
                }
            ]
        }
    }

    try:
        response = requests.post(url=url, json=body, headers=headers, params=params)
        logger.info(f'Response text: {response.text}')
        logger.info(f'Response code: {response.status_code}')
        logger.info(f'Response headers: {json.dumps(dict(response.headers), indent=4, ensure_ascii=False)}')
        logger.info(f'Response body: {json.dumps(response.json(), indent=4, ensure_ascii=False)}')
        return response.json()

    except Exception as error:
        print(error)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--service-name', type=str, help='Service name')
    parser.add_argument('--subscription-key', type=str, help='Subscription key')
    parser.add_argument('--text', type=str, help='Text')
    parser.add_argument('--functionality', type=str, default='sentiment', help='Functionality')
    args = parser.parse_args()
    response = text_analysis_nlp(args.service_name, args.subscription_key, args.text, args.functionality)
    
    print(response)