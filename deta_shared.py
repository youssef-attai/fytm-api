import os

from deta import Deta
from dotenv import load_dotenv

load_dotenv()

MY_DETA_PROJECT_KEY = os.environ['MY_DETA_PROJECT_KEY']

deta = Deta(MY_DETA_PROJECT_KEY)
