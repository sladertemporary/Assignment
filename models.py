from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import datetime


class Event(Base):
	__tablename__ = 'Events'

	eventid = Column(Integer, primary_key=True, autoincrement=True)

	timestamp = Column(DateTime, default=datetime.datetime.utcnow)
	source_ip = Column(String(120))
	name = Column(String(120))
	status_code = Column(Integer)

	geolocation_child = relationship('Geolocation', uselist=False, backref='event')


class Geolocation(Base):
	__tablename__ = 'Geolocation'

	GeolocationID = Column(Integer, primary_key=True, autoincrement=True)

	city = Column(String(50))
	country_name = Column(String(120))
	country_iso = Column(String(2))
	accuracy_radius = Column(Integer())
	latitude = Column(Float())
	longitude = Column(Float())
	metro_code = Column(Integer(), nullable=True)
	time_zone = Column(String(120))

	eventid = Column(Integer, ForeignKey('Events.eventid'))