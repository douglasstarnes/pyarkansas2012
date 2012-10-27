from flask import Flask, request
from flask.views import MethodView
from mongoengine import connect

from feed_models_v2 import Feed, User, UserFeed
from feed_utils import get_next_sequence

import os
import json

app = Flask(__name__)

class FeedView(MethodView):
	def get(self, id):
		if id == None:
			return json.dumps(
				[
					{
						"id": f.sequence_id,
						"title": f.title,
						"url": f.url
					}
					for f in Feed.objects
				]
			)
		else:
			f = Feed.objects(sequence_id=id).first()
			if f == None:
				return json.dumps(
					{
						"error":"no feed with id %d" % (id)
					}
				)
			else:
				return json.dumps(
					{
						"id": f.sequence_id,
						"title": f.title,
						"url": f.url
					}
				)

	def post(self):
		sequence_id = get_next_sequence("feed")
		f = Feed(sequence_id=sequence_id, title=request.json["title"], url=request.json["url"])
		f.save()
		return json.dumps({"id":sequence_id})

	def put(self, id):
		f = Feed.objects(sequence_id=id).first()
		if f == None:
			return json.dumps(
				{
					"error":"no feed with id %d" % (id)
				}
			)
		else:
			for key in request.json.keys():
				if key == "title":
					f.update(set__title=request.json[key])
				elif key == "url":
					f.update(set__url=request.json[key])
			return json.dumps({"id":id})

	def delete(self, id):
		f = Feed.objects(sequence_id=id).first()
		if f == None:
			return json.dumps(
				{
					"error":"no feed with id %d" % (id)
				}
			)
		else:
			f.delete()
			return json.dumps({"id":id})

class UserView(MethodView):
	pass

feed_view = FeedView.as_view("feed_view")

app.add_url_rule("/feed/", 
	defaults={"id": None}, 
	view_func=feed_view, 
	methods=["GET",])
app.add_url_rule("/feed/", 
	view_func=feed_view, 
	methods=["POST",])
app.add_url_rule("/feed/<int:id>", 
	view_func=feed_view, 
	methods=["PUT", "GET", "DELETE",])

if __name__ == "__main__":
	# mongoengine
	connect("feeds")
	app.debug = True
	app.run()
