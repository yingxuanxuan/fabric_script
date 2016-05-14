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
