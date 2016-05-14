from urllib import request, response
import json

def can_access(api_key):
    req = request.Request('https://api.vultr.com/v1/auth/info')
    req.add_header('API-Key', api_key)

    try:
        with request.urlopen(req) as f:

            data = f.read()
            if not data:
                print('Read data fail.')
                return False

            obj = json.loads(data.decode('utf-8'))
            if not obj:
                print('Parser json fail.')
                return False

            print('Access success.')
            print('User: %s' % obj['name'])
            print('Email: %s' % obj['email'])
            return True

    except BaseException as e:
        print('Access fail.')
        print(e)
        return False

def get_server_by_id(api_key, id):
    url = 'https://api.vultr.com/v1/server/list'

    if id:
        url += '?SUBID=%s' % id

    req = request.Request(url)
    req.add_header('API-Key', api_key)

    try:
        with request.urlopen(req) as f:
            data = f.read()
            if not data:
                print('Read data fail.')
                return None

            obj = json.loads(data.decode('utf-8'))
            if not obj:
                print('Parser json fail.')
                return None

            if str(id) != obj.get('SUBID', None):
                print('Get server error.')
            else:
                print('Get server success.')
                return obj
    except BaseException as e:
        print(e)
        return None

def get_server_by_tag(api_key, tag):
    url = 'https://api.vultr.com/v1/server/list'

    if tag:
        url += '?tag=%s' % tag

    req = request.Request(url)
    req.add_header('API-Key', api_key)

    try:
        with request.urlopen(req) as f:
            data = f.read()
            if not data:
                print('Read data fail.')
                return None

            obj = json.loads(data.decode('utf-8'))
            if not obj:
                print('Parser json fail.')
                return None

            if 0 == len(obj):
                print('Get server error.')
            else:
                print('Get server success.')
                return obj
    except BaseException as e:
        print(e)
        return None
