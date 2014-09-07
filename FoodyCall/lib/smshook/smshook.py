from flask import make_response
from flask import jsonify
from flask import Blueprint
from flask import request
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, time
from twilio.rest import TwilioRestClient
from twilio.twiml import Response

ACCOUNT_SID = "AC726a67eecb3d307a9cc172793aab1104"
AUTH_TOKEN = "37569632fdf06701470f0d1c27c77a0a"
ORIGIN = "9783783121"

client = MongoClient()
db = client.menudb
menu_items = db.menu_items
order_history = db.order_history
smshook = Blueprint('smshook', __name__, template_folder = 'templates')


TwilioClient = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

def send_text(destination,origin,message):
  try:
    TwilioClient.messages.create(
        to = destination,
        from_= origin,
        body = message
        )
    return True
  except:
    return False


@smshook.route('',methods = ['GET'])
def index():
    received = filter(lambda s: s.status == "received",
                      TwilioClient.sms.messages.list())

    incoming = received[0].body

    oldest = order_history.find_one({"$query":   {"replied": False},
                                     "$orderby": {"date"   : -1 } })

    # Send an SMS to `oldest.phone` with `incoming`
    result = send_text(oldest.get('phone'), ORIGIN, incoming)
    if(result):
      print "Text sent to ", oldest.get('phone')
    else:
      print "Couldn't send text"

    order_history.update({"_id": ObjectId(oldest.get('_id'))},
                         {"$set": {"replied": True}})

    # Respond to Twilio with some TwiML stuff
    resp = Response()
    return str(resp)
