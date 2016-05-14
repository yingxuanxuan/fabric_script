from urllib import request, response
import json
import logging; logging.basicConfig(level=logging.DEBUG)

def can_access(api_key):
    req = request.Request('https://api.vultr.com/v1/auth/info')
    req.add_header('API-Key', api_key)

    try:
        with request.urlopen(req) as f:

            data = f.read()
            if not data:
                logging.error('Read data fail.')
                return False

            logging.debug(f.info())
            logging.debug(data.decode('utf-8'))

            obj = json.loads(data.decode('utf-8'))
            if not obj:
                logging.error('Parser json fail.')
                return False

            logging.info('Access success.')
            logging.info('User: %s, Email: %s' % (obj['email'], obj['name']))
            return True

    except BaseException as e:
        logging.error('Access fail.')
        logging.error(e)
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
                logging.error('Read data fail.')
                return None

            logging.debug(f.info())
            logging.debug(data.decode('utf-8'))

            obj = json.loads(data.decode('utf-8'))
            if not obj:
                logging.error('Parser json fail.')
                return None

            if str(id) != obj.get('SUBID', None):
                logging.error('Get server error.')
            else:
                logging.info('Get server success.')
                return obj
    except BaseException as e:
        logging.error(e)
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
                logging.error('Read data fail.')
                return None

            logging.debug(f.info())
            logging.debug(data.decode('utf-8'))

            obj = json.loads(data.decode('utf-8'))
            if not obj:
                logging.error('Parser json fail.')
                return None

            if 0 == len(obj):
                logging.error('Get server error.')
            else:
                logging.info('Get server success.')
                return obj
    except BaseException as e:
        logging.error(e)
        return None
