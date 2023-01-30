# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

verify_sid = "VAc6d479218a3f2f62b05df424b6bf8205"

# Download the helper library from https://www.twilio.com/docs/python/install
account_sid = "AC45d156351247e69c8ec8d90642de29e0"
auth_token = "668631755847f51ef1474f0f09b03b67"
verified_number = "+2203332050"

client = Client(account_sid, auth_token)

client = Client(account_sid, auth_token)

message = client.messages.create(
    body="Your Celesup verification code is 47585",
    from_="+1 720 650 0415",
    to="2203232556",
)

print(message.sid)
print(message.status)
