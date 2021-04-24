import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
SLACK_COOKIE = os.environ.get("SLACK_COOKIE")
TEAM_NAME = os.environ.get("TEAM_NAME")
FONT_PATH = os.environ.get("FONT_PATH")
