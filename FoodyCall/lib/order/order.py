from flask import make_response
from flask import jsonify
from flask import Blueprint
from flask import request
from lib.menu.menu import MongoClient
from bson.objectid import ObjectId
import sender

client = MongoClient()
db = client.menudb


order = Blueprint('order', __name__, template_folder = 'templates')

#@order.route('',methods = ['POST'])
#def index():
#  data = request.get_json()
   #destination_num = data.get(destination)
#  phone_num = data.get(number)
#  food_id = data.get(item_id)
#  special_requests = data.get(special)

#  sender.send_text(phone_num, phone_num)

