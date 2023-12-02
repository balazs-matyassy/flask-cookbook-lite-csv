import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_NAME = os.environ.get('APP_NAME') or 'Flask Cookbook'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
