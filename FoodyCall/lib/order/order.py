from flask import make_response
from flask import jsonify
from flask import Blueprint
from flask import request
from pymongo import MongoClient
from bson.objectid import ObjectId
import sender

client = MongoClient()
db = client.menudb
menu_items = db.menu_items
order = Blueprint('order', __name__, template_folder = 'templates')
print('dog')
@order.route('',methods = ['POST'])
def index():
 #destination_num = data.get(destination)
  msg = ""
  phone_num = request.form.get('number')
  print('cat')
  food_id = request.form.get('item_id')
  try:
     side_id = request.form.get('side_id')
  except:
     pass
  special_requests = request.form.get('special')
  print('crunch time')
  for items in menu_items.find():
    print('d')
    if food_id == str(items['_id']):
      msg = items['name']
  for dog in menu_items.find():
    if side_id == str(items['_id']):
      side = items['name']
      msg = side + msg
  if(len(msg)<=0):
    return jsonify({'ERROR':"ID not found"})
    to_send = msg + special
    rtn = sender.send_text(phone_num, phone_num,to_send)
    if (rtn != 'success'):
      return jonify({'ERROR':'a serious error has occurred, please inform creators of flaw'})
    else:
      return jsonify({'success':'expect your food shortly!'})
