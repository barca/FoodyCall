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

def send_text(destination,origin,message):
  try:
    TwilioClient = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    TwilioClient.messages.create(
        to = destination,
        from_= origin,
        body = message
        )
    return True
  except:
    return False

def parse(msg):
  order_number = [int(s) for s in msg.split() if s.isdigit()]
  num = int(''.join(map(str,order_number)))
  new_msg = "Thanks for using FoodyCall! Your order number is " + str(num) + "."
  return new_msg

@smshook.route('', methods = ['GET'])
def index():
    incoming = request.args.get('Body')
    oldest = order_history.find_one({"$query":   {"replied": False},
                                     "$orderby": {"date"   : -1 } })

    # Send an SMS to `oldest.user` with `incoming`
    result = send_text(oldest.get('user'), ORIGIN, parse(incoming))
    if(result):
      print "Text sent to ", oldest.get('user')
    else:
      print "Couldn't send text"

    order_history.update({"_id": ObjectId(oldest.get('_id'))},
                         {"$set": {"replied": True}})

    # Respond to Twilio with some TwiML stuff
    resp = Response()
    return str(resp)
