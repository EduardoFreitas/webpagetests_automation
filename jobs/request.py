import jobs.webpagetests as webpagetests
from db.database import Schedule, Request
import db.config


def request_schedule():
    session = db.config.Session()
    wpt = webpagetests.WebPageTests()

    query = session.query(Schedule).filter(Schedule.active == True)
    result = query.all()
    for row in result:
        req = dict(
            location=row.location_browser.location.location,
            browser=row.location_browser.browser.name,
            speed=row.speed.name,
            alias=row.name,
            url=row.url.name
        )
        print('Requested: {}'.format(req))
        id_test = wpt.run_tests(req)
        session.add(Request(schedule=row, key=id_test))
        session.commit()


if __name__ == '__main__':
    request_schedule()
