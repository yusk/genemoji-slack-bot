import re
from time import sleep

import requests
from bs4 import BeautifulSoup


class SlackAPIWrapper:
    SLACK_API_URL = "https://slack.com/api"

    URL_CUSTOMIZE = "https://{team_name}.slack.com/customize/emoji"
    URL_ADD = "https://{team_name}.slack.com/api/emoji.add"
    URL_LIST = "https://{team_name}.slack.com/api/emoji.adminList"

    API_TOKEN_REGEX = r'.*(?:\"?api_token\"?):\s*\"([^"]+)\".*'
    API_TOKEN_PATTERN = re.compile(API_TOKEN_REGEX)

    def _fetch_api_token(self, session):
        """
        The MIT License (MIT)
        Copyright (c) 2015 Ash Wilson
        https://github.com/smashwilson/slack-emojinator/blob/master/LICENSE
        """
        r = session.get(session.url_customize)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        all_script = soup.findAll("script")
        for script in all_script:
            for line in str(script).splitlines():
                if 'api_token' in line:
                    match_group = self.API_TOKEN_PATTERN.match(line.strip())
                    if not match_group:
                        raise ValueError(
                            "Could not parse API token from remote data! "
                            "Regex requires updating.")

                    return match_group.group(1)

        raise ValueError("\n".join([
            "No api_token found in page. Search your https://<teamname>.slack.com/customize/emoji ",
            "page source for \"api_token\" and enter its value manually.",
            'need the api_token ("xoxs-12345-abcdefg....") from the page'
        ]))

    def __init__(self, bot_token, team_name, cookie):
        self.bot_token = bot_token
        self.team_name = team_name
        self.cookie = cookie

    def get_headers(self):
        return {"Authorization": f"Bearer {self.bot_token}"}

    def gen_url(self, endpoint):
        return f"{self.SLACK_API_URL}/{endpoint}"

    def gen_session(self):
        """
        The MIT License (MIT)
        Copyright (c) 2015 Ash Wilson
        https://github.com/smashwilson/slack-emojinator/blob/master/LICENSE
        """
        session = requests.session()
        session.headers = {'Cookie': self.cookie}
        session.url_customize = self.URL_CUSTOMIZE.format(
            team_name=self.team_name)
        session.url_add = self.URL_ADD.format(team_name=self.team_name)
        session.url_list = self.URL_LIST.format(team_name=self.team_name)
        session.api_token = self._fetch_api_token(session)
        return session

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

    def upload_emoji(self, emoji_name, filename):
        """
        The MIT License (MIT)
        Copyright (c) 2015 Ash Wilson
        https://github.com/smashwilson/slack-emojinator/blob/master/LICENSE
        """
        session = self.gen_session()
        data = {'mode': 'data', 'name': emoji_name, 'token': session.api_token}

        while True:
            with open(filename, 'rb') as f:
                files = {'image': f}
                resp = session.post(session.url_add,
                                    data=data,
                                    files=files,
                                    allow_redirects=False)

                if resp.status_code == 429:
                    wait = int(resp.headers.get('retry-after', 1))
                    print("429 Too Many Requests!, sleeping for %d seconds" %
                          wait)
                    sleep(wait)
                    continue

            resp.raise_for_status()

            response_json = resp.json()
            if not response_json['ok']:
                raise ValueError("Error with uploading %s: %s" %
                                 (emoji_name, response_json))

            break

    def print_emojis(self):
        res = self.emoji_list()
        for key, url in res.json()["emoji"].items():
            print(key, url)
