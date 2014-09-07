from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

# Create Blueprint
ratings = Blueprint('ratings', __name__, template_folder='templates')
client = MongoClient()
db = client.menudb
menu_items=db.menu_items

@ratings.route('',methods=['POST'])
def index():
		new_id = request.form.get("item")
		rating = int(request.form.get("rate"))
		avg = 0
		for item in menu_items.find():
	 		if new_id == str(item['_id']):
	 			old_avg = item['rating_avg']
	 			num = item['rater_count']
	 			avg = (old_avg*num + rating) / (num + 1)
		 	if avg>0:
		 	  db.menu_items.update({'_id': new_id}, 
		 		  {
		 			  '$set': { 'rating_avg': avg, 'rater_count': num+1 }
		 		  }
		 		)
		 	avg = 0

	 	return json.dumps(avg)