from urllib import request, response, parse
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
                return None
            else:
                logging.info('Get server success.')
                return obj
    except BaseException as e:
        logging.error(e)
        return None


def get_server_list(api_key):
    req = request.Request('https://api.vultr.com/v1/server/list')
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

            summary = {}
            for server, info in obj.items():
                summary[server] = {}
                for k, v in info.items():
                    if k in ['SUBID',
                             'os',
                             'ram',
                             'disk',
                             'main_ip',
                             'vcpu_count',
                             'location',
                             'default_password',
                             'pending_charges',
                             'status',
                             'cost_per_month',
                             'current_bandwidth_gb',
                             'allowed_bandwidth_gb',
                             'power_status',
                             'server_state',
                             'label']:
                        summary[server][k] = v

            logging.info('Get server list:')
            logging.info(json.dumps(summary, indent=2))
            return obj
    except BaseException as e:
        logging.error(e)
        return None


def get_region_list():
    req = request.Request('https://api.vultr.com/v1/regions/list')

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

            logging.info('Get region list:')
            logging.info(json.dumps(obj, indent=2))
            return obj
    except BaseException as e:
        logging.error(e)
        return None


def get_plan_list():
    req = request.Request('https://api.vultr.com/v1/plans/list')

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

            logging.info('Get plan list:')
            logging.info(json.dumps(obj, indent=2))
            return obj
    except BaseException as e:
        logging.error(e)
        return None


def is_region_available_plan(dc_id, plan_id):
    req = request.Request('https://api.vultr.com/v1/regions/availability?DCID=%s' % dc_id)

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

            if int(plan_id) not in obj:
                logging.error('Plan %s not available in dc %s.' % (plan_id, dc_id))
                return False
            else:
                logging.info('Plan %s available in dc %s.' % (plan_id, dc_id))
                return True
    except BaseException as e:
        logging.error(e)
        return False


def get_os_list():
    req = request.Request('https://api.vultr.com/v1/os/list')

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

            logging.info('Get os list:')
            logging.info(json.dumps(obj, indent=2))
            return obj
    except BaseException as e:
        logging.error(e)
        return None


def create_server(api_key, label, dc_id, plan_id, os_id, hostname=None):
    req = request.Request('https://api.vultr.com/v1/server/create')
    req.add_header('API-Key', api_key)

    post = parse.urlencode([
        ("DCID", dc_id),
        ("VPSPLANID", plan_id),
        ("OSID", os_id),
        ("label", label),
        ("hostname", hostname if hostname else label)
    ])

    try:
        with request.urlopen(req, data=post.encode('utf-8')) as f:
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

            if None == obj.get('SUBID', None):
                logging.error('Create server fail.')
                return None
            else:
                logging.info('Create server success, SUBID=%s.' % obj['SUBID'])
                return obj['SUBID']
    except BaseException as e:
        logging.error(e)
        return None


def wait_until_ok(api_key, label):
    '''
    power status running/installing/
    '''
    #test_state()
    #ping()
    #run('uname -a')
    pass


def destroy_server_by_label(api_key, label):
    server_list = get_server_list(api_key)
    if None == server_list:
        logging.error("No Server exist")
        return False

    SUBID = None
    for server,info in server_list.items():
        if label == info["label"]:
            SUBID = info["SUBID"]
            break

    if None == SUBID:
        logging.error("Label %s not exist." % label)
        return False

    logging.info("Find label %s, SUBID %s." % (label, SUBID))
    destroy_server_by_id(SUBID)
    return True


def destroy_server_by_id(api_key, id):
    req = request.Request('https://api.vultr.com/v1/server/destroy')
    req.add_header('API-Key', api_key)
    post = parse.urlencode([
        ("SUBID", id), ])

    try:
        with request.urlopen(req, data=post.encode('utf-8')) as f:
            logging.debug(f.info())
            logging.info('Destroy server success, SUBID=%s.' % id)
            return True
    except BaseException as e:
        logging.info('Destroy server fail, SUBID=%s.' % id)
        logging.error(e)
        return False


def get_ip_by_label(api_key, label):
    server_list = get_server_list(api_key)
    if None == server_list:
        logging.error("No Server exist")
        return False

    for server,info in server_list.items():
        if label == info["label"]:
            logging.info("Label %s ip %s." % (label, info["main_ip"]))
            return info["main_ip"]

    logging.error("Label %s not exist." % label)
    return None


