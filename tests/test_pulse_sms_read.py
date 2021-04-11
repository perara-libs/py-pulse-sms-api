import unittest
from pulsesms import PulseSMSAPI
import os


class PulseSMSReadTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = PulseSMSAPI(
            username=os.getenv("PULSESMS_USERNAME"),
            password=os.getenv("PULSESMS_PASSWORD")
        )

        self.api.login()

    def test_login(self):
        self.api = PulseSMSAPI(
            username=os.getenv("PULSESMS_USERNAME"),
            password=os.getenv("PULSESMS_PASSWORD")
        )
        ret_val = self.api.login()
        self.assertIsInstance(ret_val, dict)

    def test_get_settings(self):
        self.assertIsInstance(self.api.settings(), dict)

    def test_get_conversations(self):
        self.assertIsInstance(self.api.get_conversations(), list)

    def test_get_unread_messages(self):
        self.assertIsInstance(self.api.get_unread_messages(), list)

    def test_get_archived_messages(self):
        self.assertIsInstance(self.api.get_archived_messages(), list)

    def test_get_scheduled_messages(self):
        self.assertIsInstance(self.api.scheduled_messages(), list)

    def test_get_templates(self):
        self.assertIsInstance(self.api.templates(), list)

    def test_get_blacklists(self):
        self.assertIsInstance(self.api.blacklists(), list)

    def test_get_conversation_messages(self):
        convs = self.api.get_conversations()
        self.assertIsInstance(convs, list)
        messages = self.api.get_messages(conversation_id=convs[-1]["device_id"])
        self.assertIsInstance(messages, list)

if __name__ == '__main__':
    unittest.main()
