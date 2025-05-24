from flask import json
import requests
import sys
import argparse

sys.path.append('src')
from image_analysis import image_analysis
from setup_logger import setup_logger
logger = setup_logger()
def optical_character_recognition(service_name, subscription_key, image_url=None, image_data=None):
    logger.debug(f'Service name: {service_name}')
    logger.debug(f'Image path: {image_url}')
    features = 'read'
    return image_analysis(service_name, subscription_key, features, image_url, image_data)

