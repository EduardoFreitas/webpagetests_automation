import jobs.response
import jobs.request


def lambda_handler(event, context):
    call = event['call']
    print('Called: {}'.format(call))
    if call == 'Request':
        jobs.request.request_schedule()
    if call == 'Response':
        jobs.response.response_schedule()

    print('Success')