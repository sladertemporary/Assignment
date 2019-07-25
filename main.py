from flask import Flask, request, jsonify
import requests 
import json 
import redis
from datetime import datetime
from rq import Queue, Connection
from task import *

app = Flask(__name__)

REDIS_URL = 'redis://localhost:6379'
REDIS_QUEUES = ['default']

@app.route('/event/submit/', methods = ['POST'])
def user():
	if not request.json:
		return jsonify(isError= True, message= "Not JSON", statusCode=400,data=request.data)

	postdata = request.json
	source_ip = request.remote_addr

	with Connection(redis.from_url(REDIS_URL)):
		q = Queue()
		task = q.enqueue(DBCommit, postdata, source_ip)

		response_object = {
				'status': 'success',
				'data': {
				'task_id': task.get_id()
			}
		}

	return jsonify(response_object), 202

@app.route('/event/fetch/', methods = ['GET'])
def fetch():
	datemin = request.args.get('datefrom')
	datestart = request.args.get('dateto')

	city_name = request.args.get('city_name')
	country_name = request.args.get('country_name')
	iso_code = request.args.get('iso_code')

	session = sessionmaker()
	session.configure(bind=engine)
	Base.metadata.create_all(engine)

	query = session()

	results = query.query(Event).filter_by(source_ip = '127.0.0.1').all()

	print (results[0].name)
	return(results[0].name)

if __name__ == '__main__':
    app.run(debug=True)


