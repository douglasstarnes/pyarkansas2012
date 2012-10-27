from mongoengine import Document, IntField, StringField, ListField, ReferenceField, BooleanField

class FeedDocument(Document):
	sequence_id = IntField()

	meta = {"allow_inheritance": True}

class Feed(FeedDocument):
	title = StringField()
	url = StringField()

class User(FeedDocument):
	email = StringField()
	first_name = StringField()
	last_name = StringField()
	friends = ListField(ReferenceField('self'))

class UserFeed(FeedDocument):
	fave = BooleanField()
	user = ReferenceField(User)
	feed = ReferenceField(Feed)
