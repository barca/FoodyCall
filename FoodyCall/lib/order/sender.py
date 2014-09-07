import twilio
from twilio.rest import TwilioRestClient

ACCOUNT_SID = "AC726a67eecb3d307a9cc172793aab1104"
AUTH_TOKEN = "37569632fdf06701470f0d1c27c77a0a"

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
