from __future__ import print_function


def handler(event, context):
    print("jobs: {}".format(event['call']))
    # if event['call'] == 'request':
    #     request.request_schedule()
    # if event['call'] == 'result':
    #     result.retrieve()

    return "jobs: {} Success".format(event['call'])


if __name__ == '__main__':
    event_call = {
        'call': 'request'
    }
    handler(event_call, {})
