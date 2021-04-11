# py-pulse-sms-api [![Python package](https://github.com/perara-libs/py-pulse-sms-api/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/perara-libs/py-pulse-sms-api/actions/workflows/python-package.yml)
A unofficial API for pulse-sms in python.


## Install
`pip install git+https://github.com/perara-libs/py-pulse-sms-api.git`


## Usage
```python
from pulsesms import PulseSMSAPI

api = PulseSMSAPI(username=os.getenv("PULSESMS_USERNAME"), password=os.getenv("PULSESMS_PASSWORD"))
api.login()

print(api.settings())
print(api.get_conversations())
print(api.get_unread_messages())
print(api.get_archived_messages())
print(api.scheduled_messages())
print(api.templates())
print(api.blacklists())
for conv in api.get_conversations():
    print(api.get_messages(conversation_id=conv["device_id"]))
```
