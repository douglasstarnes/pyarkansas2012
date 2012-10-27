from pymongo import Connection

def get_next_sequence(name):
	# VERY inefficient
	conn = Connection("localhost")
	ret = conn.feeds.counters.find_and_modify(
		query={"_id":"name"},
		update={"$inc":{"next":1}},
		upsert=True,
		new=True
	)
	return ret["next"]