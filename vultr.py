#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    # python3
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
except ImportError:
    # python2
    from urllib2 import Request, urlopen
    from urllib import urlencode

from fabric.api import local, env, run, settings, hosts, execute
import json
import time
import logging

logging.basicConfig(level=logging.INFO)


def can_access(api_key):
    req = Request('https://api.vultr.com/v1/auth/info')
    req.add_header('API-Key', api_key)

    try:
        f = urlopen(req)

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


def get_server_by_label(api_key, label):
    server_list = _get_server_list(api_key)
    if server_list is None:
        logging.error('No server exist')
        return None

    for server, info in server_list.items():
        if label == info['label']:
            logging.info('Label %s ip %s.' % (label, info['main_ip']))
            return info

    logging.error('Label %s not exist.' % label)
    return None


def _get_server_list(api_key):
    req = Request('https://api.vultr.com/v1/server/list')
    req.add_header('API-Key', api_key)

    try:
        f = urlopen(req)
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

        return obj
    except BaseException as e:
        logging.error(e)
        return None


def get_server_list(api_key):
    server_list = _get_server_list(api_key)
    if not server_list:
        return

    for server, info in server_list.items():
        logging.info('Server SUBID %s:' % server)
        logging.info('\t' + 'label: ' + info['label'])
        logging.info('\t' + 'status: ' + info['power_status'])
        logging.info('\t' + 'os: ' + info['os'])
        logging.info('\t' + 'ram: ' + info['ram'])
        logging.info('\t' + 'disk: ' + info['disk'])
        logging.info('\t' + 'ip: ' + info['main_ip'])
        logging.info('\t' + 'cpu: ' + info['vcpu_count'])
        logging.info('\t' + 'pwd: ' + info['default_password'])
        logging.info('\t' + 'pending charge: ' + info['pending_charges'])
        logging.info('\t' + 'cost per month: ' + info['cost_per_month'])
        logging.info('\t' + 'use bandwidth: ' + str(info['current_bandwidth_gb']))
        logging.info('\t' + 'total bandwidth: ' + str(info['allowed_bandwidth_gb']))
        logging.info('')


def _get_region_list():
    req = Request('https://api.vultr.com/v1/regions/list')

    try:
        f = urlopen(req)
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

        return obj
    except BaseException as e:
        logging.error(e)
        return None


def get_region_list():
    region_list = _get_region_list()
    if not region_list:
        return

    logging.info('DCID\tBLOCK_STORAGE\tDDOS_PROTECTION\tCOUNTRY\t\tDCNAME\t\tCONTINENT')

    for dcid, info in region_list.items():
        logging.info(info['DCID'] +
                     '\t' + str(info['block_storage']) +
                     '\t\t' + str(info['ddos_protection']) +
                     '\t\t' + info['country'] +
                     '\t\t' + info['name'] +
                     '\t\t' + info['continent'])


def _get_plan_list():
    req = Request('https://api.vultr.com/v1/plans/list')

    try:
        f = urlopen(req)
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

        return obj
    except BaseException as e:
        logging.error(e)
        return None


def get_plan_list():
    plan_list = _get_plan_list()
    if not plan_list:
        return

    logging.info('ID\tPRICE\tCPU\tDESCRIPTION\tPLAN_TYPE')

    for plan_id, info in plan_list.items():
        logging.info(info['VPSPLANID'] +
                     '\t' + info['price_per_month'] +
                     '\t' + info['vcpu_count'] +
                     '\t' + info['name'] +
                     '\t' + info['plan_type'])


def is_region_available_plan(dc_id, plan_id):
    req = Request('https://api.vultr.com/v1/regions/availability?DCID=%s' % dc_id)

    try:
        f = urlopen(req)
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


def _get_os_list():
    req = Request('https://api.vultr.com/v1/os/list')

    try:
        f = urlopen(req)
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

        return obj
    except BaseException as e:
        logging.error(e)
        return None


def get_os_list():
    os_list = _get_os_list()
    if not os_list:
        return

    logging.info('ID\tARCH\tFAMILY\tNAME')

    for os_id, info in os_list.items():
        logging.info(os_id +
                     '\t' + info['arch'] +
                     '\t' + info['family'] +
                     '\t' + info['name'])


def create_server(api_key, label, dc_id, plan_id, os_id, hostname=None):
    server = get_server_by_label(api_key, label)
    if server:
        logging.error('Label %s already exists.' % label)
        return None

    if not is_region_available_plan(dc_id, plan_id):
        logging.error('DC %s is not available plan %s.' % (dc_id, plan_id))
        return None

    os_list = _get_os_list()
    if os_list is None:
        return None

    if os_id not in os_list:
        logging.error('OS %s is not available.')
        return None

    req = Request('https://api.vultr.com/v1/server/create')
    req.add_header('API-Key', api_key)

    post = urlencode([
        ('DCID', dc_id),
        ('VPSPLANID', plan_id),
        ('OSID', os_id),
        ('label', label),
        ('hostname', hostname if hostname else label)])

    try:
        f = urlopen(req, data=post.encode('utf-8'))
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

        if obj.get('SUBID', None) is None:
            logging.error('Create server fail.')
            return None
        else:
            logging.info('Create server success, SUBID=%s.' % obj['SUBID'])
            return obj['SUBID']
    except BaseException as e:
        logging.error(e)
        return None


def wait_until_ok(api_key, label, wait=300):
    '''
    status: pending | active | suspended | closed
    -> active -> power status: running/stopped/starting
    -> active -> server status: none | locked | installingbooting | isomounting | ok

    fab -f vultr.py create_server:KEY,shadowsocks,5,29,167
    fab -f vultr.py print_server_list:KEY

    status  powerstatus serverstatus
    pending running     none
    active  running     ok      <- All state is ok but not installed
    active  stopped     locked
    active  starting    ok
    active  runnnig     ok

    '''

    # get server
    server = get_server_by_label(api_key, label)
    if server is None:
        logging.error('Label %s not exist.' % label)
        return False

    # test server ping
    def test_ping(ip):
        with settings(warn_only=True):
            result = local('ping -c 1 %s' % ip)
            if result.failed:
                logging.info('Ping ip %s fail.' % ip)
                return False
            else:
                logging.info('Ping ip %s success.' % ip)
                return True

    # test server status
    start_time = time.time()
    while True:
        if time.time() > start_time + wait:
            logging.error('Server %s start timeout.' % label)
            return False

        try:
            server = get_server_by_label(api_key, label)
            status = server['status']
            power_status = server['power_status']
            server_state = server['server_state']
            server_ip = server['main_ip']
        except BaseException as e:
            logging.error(e)
            continue

        logging.info('Server %s, status: %s, power status: %s, server status: %s, ip: %s'
                     % (label, status, power_status, server_state, server_ip))
        if 'active' == status and 'running' == power_status and 'ok' == server_state and '0' != server_ip:
            logging.info('Server %s status ok' % label)
            if test_ping(server_ip):
                logging.info('Server %s start success.' % label)
                break
            else:
                logging.info('Left %s seconds timeout.' % str(start_time + wait - time.time()))
                time.sleep(10)
        else:
            logging.info('Left %s seconds timeout.' % str(start_time + wait - time.time()))
            time.sleep(10)

    # get ip and password from new server info, init ip is 0
    server_ip = server['main_ip']
    server_password = server['default_password']

    # test server connect
    try:
        def test_task():
            run('uname -n')

        with settings(user='root', hosts=[server_ip], password=server_password, no_keys=True):
            execute(test_task)
            logging.info('Connect server success.')
            return True

    except BaseException as e:
        logging.error('Connect server fail.')
        logging.error(e)
        return False


def destroy_server_by_id(api_key, id):
    req = Request('https://api.vultr.com/v1/server/destroy')
    req.add_header('API-Key', api_key)
    post = urlencode([('SUBID', id), ])

    try:
        f = urlopen(req, data=post.encode('utf-8'))
        logging.debug(f.info())
        logging.info('Destroy server success, SUBID=%s.' % id)
        return True
    except BaseException as e:
        logging.info('Destroy server fail, SUBID=%s.' % id)
        logging.error(e)
        return False


def destroy_server_by_label(api_key, label):
    server = get_server_by_label(api_key, label)
    if server is None:
        logging.error('No server exist')
        return False

    logging.info('Find label %s, SUBID %s.' % (label, server['SUBID']))
    return destroy_server_by_id(api_key, server['SUBID'])


def reboot_server_by_id(api_key, id):
    req = Request('https://api.vultr.com/v1/server/reboot')
    req.add_header('API-Key', api_key)
    post = urlencode([('SUBID', id), ])

    try:
        f = urlopen(req, data=post.encode('utf-8'))
        logging.debug(f.info())
        logging.info('Reboot server success, SUBID=%s.' % id)
        return True
    except BaseException as e:
        logging.info('Reboot server fail, SUBID=%s.' % id)
        logging.error(e)
        return False


def reboot_server_by_label(api_key, label):
    server = get_server_by_label(api_key, label)
    if server is None:
        logging.error('No server exist')
        return False

    logging.info('Find label %s, SUBID %s.' % (label, server['SUBID']))
    return reboot_server_by_id(api_key, server['SUBID'])
