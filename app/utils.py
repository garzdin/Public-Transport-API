__all__ = ['seconds_to_minutes', 'request']

def seconds_to_minutes(seconds):
    from time import strftime, gmtime

    return "{minutes} minutes".format(minutes=strftime("%M:%S", gmtime(seconds)))

def request(url):
    from urllib2 import Request, urlopen
    from json import loads

    headers = {}

    headers[session_id_key] = session_id

    request = Request(url, headers=headers)

    response = urlopen(request).read()
    return loads(response)
