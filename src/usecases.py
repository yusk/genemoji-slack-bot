import os

from .genemoji import make_img_for_slack2
from .env import FONT_PATH
from .slack import SlackAPIWrapper

GENEMOJI_TEXTS = [
    "絵文字作って",
    "gen emoji",
    "genemoji",
    "make emoji",
    "makeemoji",
]


def gen_d_upload_emoji(slack: SlackAPIWrapper,
                       name,
                       char,
                       color,
                       font_path=FONT_PATH,
                       dirpath="./local"):
    img = make_img_for_slack2(char, font_path, color=color)
    filepath = f"{dirpath}/{char}.png"
    os.makedirs(dirpath, exist_ok=True)
    img.save(filepath)
    slack.upload_emoji(name, filepath)
    os.remove(filepath)
