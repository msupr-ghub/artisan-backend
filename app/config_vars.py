import os

from dotenv import load_dotenv, find_dotenv

env = os.getenv('ENV', 'test')
if env == 'test':
    env_file_name = find_dotenv('.env.test')
else:
    env_file_name = find_dotenv('.env')
load_dotenv(env_file_name)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
DATABASE_URL = os.getenv("DATABASE_URL")