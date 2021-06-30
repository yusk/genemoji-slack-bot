import unittest

from src.slack import SlackAPIWrapper
from src.env import BOT_TOKEN, SLACK_EMAIL, SLACK_PASSWORD, TEAM_NAME


class TestSlack(unittest.TestCase):
    def setUp(self):
        self.slack = SlackAPIWrapper(BOT_TOKEN, TEAM_NAME, SLACK_EMAIL,
                                     SLACK_PASSWORD)
        self.emoji_name = "lgtm12345"
        self.opt_args = None

    def _upload_emoji(self):
        return self.slack.upload_emoji(self.emoji_name,
                                       "sample/lgtm.png",
                                       opt_args=self.opt_args)

    def _delete_emoji(self):
        return self.slack.delete_emoji(self.emoji_name, opt_args=self.opt_args)

    def test_upload_delete_emoji(self):
        self.assertTrue(self._upload_emoji())
        self.assertTrue(self._delete_emoji())


if __name__ == "__main__":
    unittest.main()
