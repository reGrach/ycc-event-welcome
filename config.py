import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'real-secret-key'
    PHOTO_DIR = os.environ.get('PHOTO_DIR') or 'photo_dataset'
    THRESHOLD_REC = os.environ.get('THRESHOLD_REC') or 0.7
    SAVE_IMG_FOLDER = os.environ.get('SAVE_IMG_FOLDER') or 'photo_saved'