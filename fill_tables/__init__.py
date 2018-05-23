import json
import requests
from db.database import Location, Browser, LocationBrowser, LocationGroup, Speed, Url, Schedule
import db.config


def insert_location():
    action = "http://www.webpagetest.org/getLocations.php?f=json"
    r = requests.get(action)
    data = json.loads(r.text)

    for location in data['data']:
        group = session.query(LocationGroup).filter_by(name=data['data'][location]['group']).first()
        loc = Location(name=data['data'][location]['labelShort'], location=location,
                       location_group_id=group.id)
        session.add(loc)
        session.commit()
        id_location = loc.id
        for browser in data['data'][location]['Browsers'].split(','):
            br = session.query(Browser).filter_by(name=browser).first()
            loc_browser = LocationBrowser(location_id=id_location, browser_id=br.id)
            session.add(loc_browser)
        session.commit()


def insert_browsers_and_location_group():
    action = "http://www.webpagetest.org/getLocations.php?f=json"
    r = requests.get(action)
    data = json.loads(r.text)
    browser_compare = []
    browser_db = []
    group_compare = []
    group_db = []
    for location in data['data']:
        group = data['data'][location]['group']
        if group not in group_compare:
            group_compare.append(group)
            group_db.append(LocationGroup(name=group))
        for browser in data['data'][location]['Browsers'].split(','):
            if browser.lower() not in browser_compare:
                browser_compare.append(browser.lower())
                browser_db.append(Browser(name=browser))

    session.add_all(browser_db)
    session.add_all(group_db)
    session.commit()


def insert_speeds():
    speeds = []
    speeds.append(Speed(name='DSL', description='1.5 Mbps down, 384 Kbps up, 50 ms first-hop RTT, 0% packet loss'))
    speeds.append(Speed(name='Cable', description='5 Mbps down, 1 Mbps up, 28ms first-hop RTT, 0% packet loss'))
    speeds.append(Speed(name='FIOS', description='20 Mbps down, 5 Mbps up, 4 ms first-hop RTT, 0% packet loss'))
    speeds.append(Speed(name='Dial', description='49 Kbps down, 30 Kbps up, 120 ms first-hop RTT, 0% packet loss'))
    speeds.append(Speed(name='Edge', description='240 Kbps down, 200 Kbps up, 840 ms first-hop RTT, 0% packet loss'))
    speeds.append(Speed(name='2G', description='280 Kbps down, 256 Kbps up, 800 ms first-hop RTT, 0% packet loss'))
    speeds.append(Speed(name='3GSlow', description='400 Kbps down and up, 400 ms first-hop RTT, 0% packet loss'))
    speeds.append(Speed(name='3G', description='1.6 Mbps down, 768 Kbps up, 300 ms first-hop RTT, 0% packet loss'))
    speeds.append(Speed(name='3GFast', description='1.6 Mbps down, 768 Kbps up, 150 ms first-hop RTT, 0% packet loss'))
    speeds.append(Speed(name='4G', description='9 Mbps down and up, 170 ms first-hop RTT, 0% packet loss'))
    speeds.append(Speed(name='LTE', description='12 Mbps down and up, 70 ms first-hop RTT, 0% packet loss'))
    speeds.append(Speed(name='Native', description='No synthetic traffic shaping applied'))
    session.add_all(speeds)
    session.commit()


def create_schedule():
    # create url to search
    url = []
    url.append(Url(name='http://www.facebook.com/'))
    url.append(Url(name='http://www.yahoo.com/'))
    url.append(Url(name='http://www.wikipedia.org/'))
    session.add_all(url)
    session.commit()

    # location_group_id = 173 -  Dulles, VA / Dulles/ Chrome
    # speed = 2 Cable
    schedule = []
    schedule.append(Schedule(name='Facebook', active=True, url_id=1, speed_id=2, location_browser_id=173))
    schedule.append(Schedule(name='Yahoo', active=True, url_id=2, speed_id=2, location_browser_id=173))
    schedule.append(Schedule(name='Wikipedia', active=True, url_id=3, speed_id=2, location_browser_id=173))
    session.add_all(schedule)
    session.commit()


if __name__ == '__main__':
    session = db.config.Session()
    # insert_browsers_and_location_group()
    # insert_location()
    # insert_speeds()
    create_schedule()
    session.close()
