
from twilio.rest import TwilioRestClient

# ACCOUNT_SID
# AUTH_TOKEN
def send_text(destination,origin,message):
  try:
    client = TwilioRestClient(ACCOUNT_SID,AUTH_TOKEN)
    client.messages.create(
        to = destination,
        from_= origin,
        body = message
        )
    return "success"
  except:
    return "fail"
