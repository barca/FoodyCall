from flask import make_response
from flask import jsonify
from flask import Blueprint
from flask import request
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, time
from twilio.rest import TwilioRestClient
from twilio.twiml import Response
import re

#ACCOUNT_SID = key
#AUTH_TOKEN = key
#ORIGIN = phone num
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
  num = re.findall(r'\b\d+\b',msg)[0]
  return "Thanks for using FoodyCall! Your order number is " + str(num) + "."

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
