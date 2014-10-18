import twilio
from twilio.rest import TwilioRestClient

#ACCOUNT_SID = key1
#AUTH_TOKEN = key2

def send_text(destination,origin,message):
  try:
    client = TwilioRestClient(ACCOUNT_SID,AUTH_TOKEN)
    client.messages.create(
        to = destination,
        from_= origin,
        body = message
        )
    return "success"
  except twilio.TwilioRestException as e:
    print e
    return "fail"
