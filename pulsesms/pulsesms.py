import base64
import hashlib
import requests
from loguru import logger
from Crypto.Cipher import AES
import dotenv

dotenv.load_dotenv(".env")
import os


class PulseCrypt:

    def __init__(self, api: "PulseSMSAPI"):
        self.api = api
        self.secret_key = self._decryptor()

    @staticmethod
    def unpad(s):
        ord_ = ord(s[len(s) - 1:])
        return s[:-ord_]

    def _decryptor(self):
        derived_key = hashlib.pbkdf2_hmac('SHA1', self.api.password.encode("utf-8"),
                                          self.api.auth["salt2"].encode("utf-8"), 10000, 32)
        base64_hash = base64.b64encode(derived_key)

        combined_key = b"" + self.api.auth["account_id"].encode("utf-8") + b":" + base64_hash + b"\n"
        secret_key = hashlib.pbkdf2_hmac('SHA1', combined_key, self.api.auth["salt1"].encode("utf-8"), 10000, 32)

        return secret_key

    def decrypt(self, data: str):
        if not data:
            return None
        iv, ciphertext = [base64.b64decode(x) for x in data.split("-:-")]
        aes = AES.new(key=self.secret_key, mode=AES.MODE_CBC, iv=iv)
        output = PulseCrypt.unpad(aes.decrypt(ciphertext)).decode("utf-8")
        return output


class PulseSMSAPI:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.crypto = None
        self.auth = None

    def login(self):
        resp = self.session.post(
            "https://api.pulsesms.app/api/v1/accounts/login/",
            json=dict(
                username=self.username,
                password=self.password
            )
        )
        if resp.status_code == 200:
            self.auth = resp.json()
            self.crypto = PulseCrypt(self)
        else:
            raise RuntimeError(resp.text)
        return self.auth

    def _get(self, path, limit=75, decrypt_keys=None, append_arg=None):
        if append_arg is not None:
            append_arg = f"&{append_arg}"
        else:
            append_arg = ""

        if decrypt_keys is None:
            decrypt_keys = []
        data = self.session.get(
            f"https://api.pulsesms.app/api/v1/{path}?account_id={self.auth['account_id']}&limit={limit}{append_arg}"
        ).json()

        for item in data:
            for key in decrypt_keys:
                if key in item:
                    item[key] = self.crypto.decrypt(item[key])
                else:
                    logger.warning(f"Could not find key: {key} in item.")

        return data

    def settings(self):
        return self._get("accounts/settings")

    def get_unread_messages(self, limit=75):
        return self._get("conversations/index_public_unread", limit=limit,
                         decrypt_keys=["title", "snippet", "phone_numbers"])

    def get_archived_messages(self, limit=75):
        return self._get("conversations/index_archived", limit=limit,
                         decrypt_keys=["title", "snippet", "phone_numbers"])

    def get_conversations(self, limit=75):
        return self._get("conversations/index_public_unarchived", limit=limit,
                         decrypt_keys=["title", "snippet", "phone_numbers"])

    def get_messages(self, conversation_id, limit=75):
        return self._get("messages/", append_arg=f"conversation_id={conversation_id}&web=true&offset=0", limit=limit,
                         decrypt_keys=["data", "mime_type", "message_from"])

    def scheduled_messages(self, limit=75):
        return self._get("scheduled_messages", limit=limit, decrypt_keys=["data", "mime_type", "title", "to"])

    def templates(self, limit=75):
        return self._get("templates", limit=limit, decrypt_keys=["text"])

    def blacklists(self, limit=75):
        return self._get("blacklists", limit=limit, decrypt_keys=["phrase", "phone_number"])


if __name__ == "__main__":

    api_test = PulseSMSAPI(username=os.getenv("PULSESMS_USERNAME"), password=os.getenv("PULSESMS_PASSWORD"))
    api_test.login()
    print(api_test.settings())
    print(api_test.get_conversations())
    print(api_test.get_unread_messages())
    print(api_test.get_archived_messages())
    print(api_test.scheduled_messages())
    print(api_test.templates())
    print(api_test.blacklists())
    for conv in api_test.get_conversations():
        print(api_test.get_messages(conversation_id=conv["device_id"]))
