
from twilio.rest import TwilioRestClient

#ACCOUNT_SID =
#AUTH_TOKEN =
def send_text(destination,origin,message):
    client = TwilioRestClient(ACCOUNT_SID,AUTH_TOKEN)
    client.messages.create(
        to = 6036864110,
        from_= origin,
        body = message
        )
