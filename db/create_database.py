from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from settings import load_configuration

import datetime
import os

Base = declarative_base()


class Url(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    update = Column(DateTime, default=datetime.datetime.utcnow)


class LocationGroup(Base):
    __tablename__ = 'location_groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    update = Column(DateTime, default=datetime.datetime.utcnow)


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    location_group_id = Column(Integer, ForeignKey('location_groups.id'))
    update = Column(DateTime, default=datetime.datetime.utcnow)
    location_group = relationship(LocationGroup)


class Browser(Base):
    __tablename__ = 'browsers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'))
    update = Column(DateTime, default=datetime.datetime.utcnow)
    location = relationship(Location)


class Speed(Base):
    __tablename__ = 'speeds'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(150), nullable=False)
    update = Column(DateTime, default=datetime.datetime.utcnow)


class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    active = Column(Boolean, default=True)

    url_id = Column(Integer, ForeignKey('urls.id'))
    browser_id = Column(Integer, ForeignKey('browsers.id'))
    speed_id = Column(Integer, ForeignKey('speeds.id'))
    # not normalized for performance
    location_id = Column(Integer, ForeignKey('locations.id'))

    update = Column(DateTime, default=datetime.datetime.utcnow)
    url = relationship(Url)
    browser = relationship(Browser)
    speed = relationship(Speed)
    location = relationship(Location)


class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey('schedules.id'))
    key = Column(String(50), nullable=False)
    request_start = Column(DateTime, default=datetime.datetime.utcnow)
    request_returned = Column(DateTime, default=datetime.datetime.utcnow)
    returned = Column(Boolean, default=False)
    erros = Column(Boolean, default=False)
    update = Column(DateTime, default=datetime.datetime.utcnow)
    schedule = relationship(Schedule)


class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey('requests.id'))

    bytesout = Column(Integer)
    requestsfull = Column(Integer)
    bytesoutdoc = Column(Integer)
    basepagessltime = Column(Integer)
    doctime = Column(Integer)
    requestsdoc = Column(Integer)
    firstmeaningfulpaint = Column(Integer)
    firsttextpaint = Column(Integer)
    loadtime = Column(Integer)
    firstcontentfulpaint = Column(Integer)
    firstlayout = Column(Integer)
    bytesindoc = Column(Integer)
    firstimagepaint = Column(Integer)
    fullyloaded = Column(Integer)
    ttfb = Column(Integer)
    bytesin = Column(Integer)
    domelements = Column(Integer)
    speedindex = Column(Integer)
    visualcomplete85 = Column(Integer)
    visualcomplete90 = Column(Integer)
    visualcomplete95 = Column(Integer)
    visualcomplete99 = Column(Integer)
    visualcomplete = Column(Integer)
    render = Column(Integer)

    date_response = Column(DateTime)
    first = Column(Boolean)
    update = Column(DateTime, default=datetime.datetime.utcnow)
    request = relationship(Request)


load_configuration()

db_username = os.environ["db_username"]
db_password = os.environ["db_password"]
db_name = os.environ["db_name"]
host = os.environ["host"]

conn_data = 'mysql+pymysql://{}:{}@{}/{}'.format(db_username, db_password, host, db_name)

engine = create_engine(conn_data)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
