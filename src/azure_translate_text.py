import argparse
import sys
from flask import json
import requests

sys.path.append('src')
from setup_logger import setup_logger
logger = setup_logger()

def language_detection(subscription_key, region, text):
    logger.debug(f'Text: {text}')
    url = 'https://api.cognitive.microsofttranslator.com/detect?api-version=3.0'

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Ocp-Apim-Subscription-Region": region
    }

    data = [{"text": text}]

    try:
        response = requests.post(url=url, json=data, headers=headers)
        logger.debug(f'Response text: {response.text}')
        logger.debug(f'Response code: {response.status_code}')
        logger.debug(f'Response headers: {json.dumps(dict(response.headers), indent=4, ensure_ascii=False)}')
        logger.debug(f'Response body: {json.dumps(response.json(), indent=4, ensure_ascii=False)}')
        return response.json()

    except Exception as error:
        logger.error(f'Error: {error}')
        return None

def text_translation(subscription_key, region, text, to_lang):
    logger.debug(f'Text: {text}')
    url = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Ocp-Apim-Subscription-Region": region,
        "charset": "UTF-8"
    }

    if not to_lang:
        logger.debug('Target language is not provided. Defaulting to English.')
        to_lang = 'en'
    else:
        logger.debug(f'Translating to: {to_lang}')

    data = [{"text": text}]

    # Detect the language of the text
    logger.debug(f'Detecting language for text: {text}')

    detected_language = language_detection(subscription_key, region, text)
    is_translation_suported = detected_language[0]['isTranslationSupported']
    logger.debug(f'Is translation supported: {is_translation_suported}')
    if not is_translation_suported:
        logger.error('Translation is not supported for the detected language.')
        return None

    if detected_language:
        from_lang = detected_language[0]['language']
        logger.debug(f'Detected language: {from_lang}')
    else:
        logger.error('Failed to detect language')
        return None
    logger.debug(f'Translating from {from_lang} to {to_lang}')

    params = {
        "from": from_lang,
        "to": to_lang
    }

    try:
        response = requests.post(url=url, json=data, headers=headers, params=params)
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
    parser.add_argument('--subscription-key', type=str, help='Subscription key')
    parser.add_argument('--region', type=str, help='Region')
    parser.add_argument('--text', type=str, help='Text to detect language for')
    parser.add_argument('--to-lang', type=str, help='Target language for translation')
    args = parser.parse_args()
    print(text_translation(args.subscription_key, args.region, args.text, args.to_lang))