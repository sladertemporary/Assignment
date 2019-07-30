from flask import Flask, request, jsonify
import requests 
import json 
import redis
from datetime import datetime
from rq import Queue, Connection
from database import db_session
from sqlalchemy.orm import sessionmaker
from task import *

app = Flask(__name__)

REDIS_URL = 'redis://localhost:6379'
REDIS_QUEUES = ['default']

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

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
	session = sessionmaker()
	session.configure(bind=engine)

	query = session()

	datefrom = request.args.get('datefrom')
	dateto = request.args.get('dateto')

	if request.args.get('city'):
		results = query.query(Geolocation).filter(Geolocation.city==request.args.get('city'))
		return(results[0].city)

	if request.args.get('country_name'):
		results = query.query(Geolocation).filter(Geolocation.country_name==request.args.get('country_name'))
		return(results[0].city)

	if request.args.get('country_iso'):
		results = query.query(Geolocation).filter(Geolocation.country_iso==request.args.get('country_iso'))
		return(results[0].city)

	if datefrom is not None and dateto is not None:
		if results:
			results = results.filter()
		else:
			results = query.query(Geolocation).filter()
			return(results[0].city)

	return jsonify(isError= True, message= "No valid parameters!", statusCode=400,data=request.data)

if __name__ == '__main__':
    app.run(debug=True)


