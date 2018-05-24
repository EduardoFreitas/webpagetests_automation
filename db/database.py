from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import db.config
import datetime

Base = declarative_base()


class Url(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    update = Column(DateTime, default=datetime.datetime.utcnow)


class LocationGroup(Base):
    __tablename__ = 'location_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    update = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<LocationGroup instance: %(id)s>" % self.__dict__


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    location_group_id = Column(Integer, ForeignKey('location_group.id'))
    update = Column(DateTime, default=datetime.datetime.utcnow)
    location_group = relationship(LocationGroup)

    def __repr__(self):
        return "<Location instance: %(id)s>" % self.__dict__


class Browser(Base):
    __tablename__ = 'browsers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    def __repr__(self):
        return "<Browser instance: %(id)s>" % self.__dict__


class LocationBrowser(Base):
    __tablename__ = 'locations_browser'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    browser_id = Column(Integer, ForeignKey('browsers.id'))
    update = Column(DateTime, default=datetime.datetime.utcnow)
    location = relationship(Location)
    browser = relationship(Browser)

    def __repr__(self):
        return "<LocationBrowser instance: %(id)s>" % self.__dict__


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
    speed_id = Column(Integer, ForeignKey('speeds.id'))
    location_browser_id = Column(Integer, ForeignKey('locations_browser.id'))

    update = Column(DateTime, default=datetime.datetime.utcnow)
    url = relationship(Url)
    speed = relationship(Speed)
    location_browser = relationship(LocationBrowser)

    def __repr__(self):
        return "<Schedule instance: %(id)s>" % self.__dict__


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

    def __repr__(self):
        return "<Request instance: %(id)s>" % self.__dict__


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

    def __repr__(self):
        return "<Response instance: %(id)s>" % self.__dict__


Base.metadata.create_all(db.config.engine)
