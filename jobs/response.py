import jobs.webpagetests as webpagetests
from db.database import Schedule, Request, Response
import db.config
import time
import sys


def response_schedule():
    session = db.config.Session()
    wpt = webpagetests.WebPageTests()

    query = session.query(Request).filter(Request.returned == False)
    result = query.all()
    for row in result:
        try:
            result_request = wpt.test_result(row.key)
            if result_request['statusCode'] != 200:
                print('Not Ready Key:{}'.format(row.key))
                continue
            first = result_request['data']['runs']['1']['firstView']
            repeat = result_request['data']['runs']['1']['repeatView']

            response_first = create_response(first, row, True)
            response_repeat = create_response(repeat, row, False)
            session.add(response_first)
            session.add(response_repeat)

            row.returned = True
            print('Success:{}'.format(row.key))
        except:
            print('Error Key:{} - Unexpected error: {}'.format(row.key, sys.exc_info()[0]))
            row.returned = True
            row.erros = True
        session.commit()


def create_response(data, request, first):
    date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(data['date'])))

    resp = Response(bytesout=data['bytesOut'], requestsfull=data['requestsFull'], bytesoutdoc=data['bytesOutDoc'],
                    basepagessltime=data['basePageSSLTime'], doctime=data['docTime'],
                    requestsdoc=data['requestsDoc'], firstmeaningfulpaint=data['firstMeaningfulPaint'],
                    firsttextpaint=data['firstTextPaint'], loadtime=data['loadTime'],
                    firstcontentfulpaint=data['firstContentfulPaint'], firstlayout=data['firstLayout'],
                    bytesindoc=data['bytesInDoc'], firstimagepaint=data['firstImagePaint'],
                    fullyloaded=data['fullyLoaded'], ttfb=data['TTFB'], bytesin=data['bytesIn'],
                    domelements=data['domElements'], speedindex=data['SpeedIndex'],
                    visualcomplete85=data['visualComplete85'], visualcomplete90=data['visualComplete90'],
                    visualcomplete95=data['visualComplete95'], visualcomplete99=data['visualComplete99'],
                    visualcomplete=data['visualComplete'], render=data['render'], date_response=date_time, first=first,
                    request=request)
    return resp


if __name__ == '__main__':
    response_schedule()
