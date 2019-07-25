import time
import requests
from database import init_db
from models import *
from sqlalchemy.orm import sessionmaker
from database import engine

init_db()


GEOLOCATION_API_URL = "http://localhost:8080/info"

def GeolocateRequest(source_ip_value):
	parameters = {'ip' : source_ip_value} 
	r = requests.get(url = GEOLOCATION_API_URL, params = parameters) 
	data = r.json() 
	return data

def DBCommit(postdata, source_ip_value):
	start_time = time.time()
	print('Starting task')

	geodata = (GeolocateRequest(source_ip_value))

	session = sessionmaker()
	session.configure(bind=engine)
	Base.metadata.create_all(engine)

	query = session()


	newevent = Event(
		source_ip = source_ip_value,
		name = postdata['name'],
		status_code	= postdata['status_code'],
		)

	query.add(newevent)

	newgeolocation = Geolocation(
		city='city', 
		country_name='name', 
		country_iso='iso', 
		accuracy_radius='test', 
		latitude='55.0353535', 
		longitude='55.0353535', 
		metro_code='metro', 
		time_zone='timezone', 
		event=newevent)
	
	query.add(newgeolocation)
	query.commit()

	end_time = time.time()
	task_time = (end_time-start_time)
	if task_time < 0.2:
		time.sleep(0.2-task_time)

	print('Task complete!')