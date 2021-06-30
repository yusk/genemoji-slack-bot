import re
import os
from time import sleep

import requests
import chromedriver_binary  # nopa
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class SlackAPIWrapper:
    SLACK_API_URL = "https://slack.com/api"

    URL_CUSTOMIZE = "https://{team_name}.slack.com/customize/emoji"
    URL_ADD = "https://{team_name}.slack.com/api/emoji.add"
    URL_LIST = "https://{team_name}.slack.com/api/emoji.adminList"

    API_TOKEN_REGEX = r'.*(?:\"?api_token\"?):\s*\"([^"]+)\".*'
    API_TOKEN_PATTERN = re.compile(API_TOKEN_REGEX)

    def __init__(self, bot_token, team_name, email, password):
        self.bot_token = bot_token
        self.team_name = team_name
        self.email = email
        self.password = password

    def get_headers(self):
        return {"Authorization": f"Bearer {self.bot_token}"}

    def gen_url(self, endpoint):
        return f"{self.SLACK_API_URL}/{endpoint}"

    def chat_post_message(self, text, channel):
        """
        https://api.slack.com/methods/chat.postMessage
        """
        headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {self.bot_token}"
        }
        data = {
            "text": text,
            "channel": channel,
        }
        return requests.post(self.gen_url("chat.postMessage"),
                             json=data,
                             headers=headers)

    def emoji_list(self):
        url = self.gen_url("emoji.list")
        headers = self.get_headers()
        return requests.get(url, headers=headers)

    def _driver_after_login(self, opt_args="--headless"):
        options = webdriver.ChromeOptions()
        if opt_args:
            options.add_argument(opt_args)

        driver = webdriver.Chrome(options=options)
        driver.get(self.URL_CUSTOMIZE.format(team_name=self.team_name))

        sleep(1)
        email = driver.find_element_by_id("email")
        email.send_keys(self.email)
        password = driver.find_element_by_id("password")
        password.send_keys(self.password)
        submit = driver.find_element_by_id('signin_btn')
        submit.submit()

        sleep(3)
        return driver

    def upload_emoji(self, emoji_name, filename, opt_args="--headless"):
        driver = self._driver_after_login(opt_args=opt_args)

        add_btn = driver.find_element_by_xpath(
            '//button[@data-qa="customize_emoji_add_button"]')
        add_btn.click()
        sleep(1)

        emojiname = driver.find_element_by_id("emojiname")
        emojiname.send_keys(emoji_name)
        emojiimg = driver.find_element_by_id("emojiimg")
        emojiimg.send_keys(os.path.join(os.getcwd(), filename))
        save_btn = driver.find_element_by_xpath(
            '//button[@data-qa="customize_emoji_add_dialog_go"]')
        save_btn.click()
        sleep(1)

        driver.quit()
        return True

    def delete_emoji(self, emoji_name, opt_args="--headless"):
        driver = self._driver_after_login(opt_args=opt_args)

        search = driver.find_element_by_id("customize_emoji_wrapper_search")
        search.send_keys(emoji_name)
        sleep(1)
        search.send_keys(Keys.ENTER)
        sleep(3)

        x_btn = driver.find_element_by_xpath(
            f'//button[@data-emoji-name="{emoji_name}"]')
        x_btn.click()
        sleep(1)

        delete_btn = driver.find_element_by_xpath(
            '//button[@data-qa="customize_emoji_single_delete_dialog_go"]')
        delete_btn.click()
        sleep(1)

        driver.quit()
        return True

    def print_emojis(self):
        res = self.emoji_list()
        for key, url in res.json()["emoji"].items():
            print(key, url)
