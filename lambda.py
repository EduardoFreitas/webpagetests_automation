from __future__ import print_function
import jobs.response
import jobs.request


def handler(event, context):
    call = event['call']
    print('Called: {}'.format(call))
    if call == 'Request':
        jobs.request.request_schedule()
    if call == 'Response':
        jobs.response.response_schedule()

    print('Success')


if __name__ == '__main__':
    event_call = {
        'call': 'Response'
    }
    handler(event_call, {})
