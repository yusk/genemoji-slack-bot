import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TEAM_NAME = os.environ.get("TEAM_NAME")
SLACK_EMAIL = os.environ.get("SLACK_EMAIL")
SLACK_PASSWORD = os.environ.get("SLACK_PASSWORD")
FONT_PATH = os.environ.get("FONT_PATH")
