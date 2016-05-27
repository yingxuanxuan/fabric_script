#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request, parse
import logging
import json

logging.basicConfig(level=logging.INFO)


def _get_domain_list(token_id, token, **kw):
    req = request.Request('https://dnsapi.cn/Domain.List')
    param_list = [('login_token', token_id + ',' + token), ('format','json')]
    for k, v in kw.items():
        if k in ['type', 'offset', 'length', 'group_id', 'keyword' ]:
            param_list.append((k, v))

    try:
        with request.urlopen(req, data=parse.urlencode(param_list).encode('utf-8')) as f:
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

            if '1' != obj['status']['code']:
                logging.error(obj['status']['message'])
                return None

            return obj

    except BaseException as e:
        logging.error(e)
        return None


def get_domain_list(token_id, token, **kw):
    response = _get_domain_list(token_id, token, **kw)
    if response is None:
        return None

    try:
        domain_list = response['domains']
        logging.info('DOMAIN_ID\tSTATUS\tRECORDS\tDOMAIN_NAME\tOWNER')
        for info in domain_list:
            logging.info(str(info['id'])
                         + '\t' + info['status']
                         + '\t' + info['records']
                         + '\t' + info['name']
                         + '\t' + info['owner'])
        return

    except BaseException as e:
        logging.error(e)
        return


def _get_domain_id_by_domain_name(token_id, token, domain_name):
    response = _get_domain_list(token_id, token, keyword = domain_name)
    if response is None:
        return None

    try:
        domain_list = response['domains']
        for info in domain_list:
            logging.info('Domain %s id %s' % (domain_name, info['id']))
            return info['id']
    except BaseException as e:
        logging.error(e)

    return None


def _get_record_list(token_id, token, domain_id, **kw):
    req = request.Request('https://dnsapi.cn/Record.List')
    param_list = [('login_token', token_id + ',' + token), ('format','json'), ('domain_id', domain_id)]
    for k, v in kw.items():
        if k in ['offset', 'length', 'sub_domain', 'keyword' ]:
            param_list.append((k, v))

    try:
        with request.urlopen(req, data=parse.urlencode(param_list).encode('utf-8')) as f:
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

            if '1' != obj['status']['code']:
                logging.error(obj['status']['message'])
                return None

            return obj

    except BaseException as e:
        logging.error(e)
        return None


def get_record_list(token_id, token, domain_name, **kw):

    domain_id = _get_domain_id_by_domain_name(token_id, token, domain_name)
    if domain_id is None:
        return

    response = _get_record_list(token_id, token, domain_id, **kw)
    if response is None:
        return None

    try:
        domain = response['domain']
        domain_info = response['info']
        record_list = response['records']
        logging.info('domain_id:%s, name:%s, owner:%s, sub_domains:%s, record_total:%s' %
                     (domain['id'], domain['name'], domain['owner'], domain_info['sub_domains'], domain_info['record_total']))
        logging.info('RECORD_ID\tNAME\tLINE\tTYPE\tTTL\tMX\tENABLED\tVALUE')
        for record in record_list:
            logging.info(record['id'] +
                         '\t' + record['name'] +
                         '\t' + record['line'] +
                         '\t' + record['type'] +
                         '\t' + record['ttl'] +
                         '\t' + record['mx'] +
                         '\t' + record['enabled'] +
                         '\t' + record['value'])
        return

    except BaseException as e:
        logging.error(e)
        return


def _get_record_id_by_sub_domain_name(token_id, token, domain_id, sub_domain_name):
    response = _get_record_list(token_id, token, domain_id, sub_domain=sub_domain_name)
    if response is None:
        return None

    try:
        record_list = response['records']
        for info in record_list:
            logging.info('Domain id %s sub domain %s id %s' % (domain_id, sub_domain_name, info['id']))
            return info['id']
    except BaseException as e:
        logging.error(e)

    return None


def _create_record(token_id, token, domain_id, sub_domain, record_type, value, record_line='默认', **kw):
    req = request.Request('https://dnsapi.cn/Record.Create')
    param_list = [('login_token', token_id + ',' + token),
                  ('format', 'json'),
                  ('domain_id', domain_id),
                  ('sub_domain', sub_domain),
                  ('record_type', record_type),
                  ('record_line', record_line),
                  ('value', value)]
    for k, v in kw.items():
        if k in ['mx', 'ttl', 'status', 'weight']:
            param_list.append((k, v))

    try:
        with request.urlopen(req, data=parse.urlencode(param_list).encode('utf-8')) as f:
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

            if '1' != obj['status']['code']:
                logging.error(obj['status']['message'])
                return False

            logging.info('Create record success, record id %s' % obj['record']['id'])
            return True

    except BaseException as e:
        logging.error(e)
        return False


def create_record(token_id, token, domain_name, sub_domain, record_type, value, **kw):
    domain_id = _get_domain_id_by_domain_name(token_id, token, domain_name)
    if domain_id is None:
        return False

    return _create_record(token_id, token, domain_id, sub_domain, record_type, value, **kw)


def _modify_record(token_id, token, domain_id, record_id, new_sub_domain, new_record_type, new_value,
                   new_record_line='默认', **kw):
    req = request.Request('https://dnsapi.cn/Record.Modify')
    param_list = [('login_token', token_id + ',' + token),
                  ('format', 'json'),
                  ('domain_id', domain_id),
                  ('record_id', record_id),
                  ('sub_domain', new_sub_domain),
                  ('record_type', new_record_type),
                  ('record_line', new_record_line),
                  ('value', new_value)]
    for k, v in kw.items():
        if k in ['new_mx', 'new_ttl', 'new_status', 'new_weight']:
            param_list.append((k[4:], v))

    try:
        with request.urlopen(req, data=parse.urlencode(param_list).encode('utf-8')) as f:
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

            if '1' != obj['status']['code']:
                logging.error(obj['status']['message'])
                return False

            logging.info('Modify record success')
            return True

    except BaseException as e:
        logging.error(e)
        return False


def modify_record(token_id, token, domain_name, sub_domain_name, new_record_type, new_value, **kw):
    domain_id = _get_domain_id_by_domain_name(token_id, token, domain_name)
    if domain_id is None:
        return False

    record_id = _get_record_id_by_sub_domain_name(token_id, token, domain_id, sub_domain_name)
    if record_id is None:
        return False

    return _modify_record(token_id, token, domain_id, record_id, sub_domain_name, new_record_type, new_value, **kw)


def _ddns_record(token_id, token, domain_id, record_id, new_sub_domain, new_value, new_record_line='默认'):
    req = request.Request('https://dnsapi.cn/Record.Ddns')
    param_list = [('login_token', token_id + ',' + token),
                  ('format', 'json'),
                  ('domain_id', domain_id),
                  ('record_id', record_id),
                  ('sub_domain', new_sub_domain),
                  ('record_line', new_record_line),
                  ('value', new_value)]

    try:
        with request.urlopen(req, data=parse.urlencode(param_list).encode('utf-8')) as f:
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

            if '1' != obj['status']['code']:
                logging.error(obj['status']['message'])
                return False

            logging.info('Ddns record success')
            return True

    except BaseException as e:
        logging.error(e)
        return False


def ddns_record(token_id, token, domain_name, sub_domain_name, new_value):
    domain_id = _get_domain_id_by_domain_name(token_id, token, domain_name)
    if domain_id is None:
        return False

    record_id = _get_record_id_by_sub_domain_name(token_id, token, domain_id, sub_domain_name)
    if record_id is None:
        return False

    return _ddns_record(token_id, token, domain_id, record_id, sub_domain_name, new_value)
