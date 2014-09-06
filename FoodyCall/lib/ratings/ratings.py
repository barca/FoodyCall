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
		item_id = request.form.get("item_id")
		rating = request.form.get("rate")
		avg = {}
		for item in menu_items.find():
	 		if item_id == str(item['_id']):
	 			avg = (item['rating_avg']*item['rater_count']+rating)/(item['rater_count']+1)
	 	if avg:
	 	  db.menu.update({item_id: item_id}, 
	 		  {
	 			  '$set': { rating_avg: avg, 
	 				  			rater_count: rater_count+1 
	 					  	}
	 		  })
	 	return json.dumps(avg)