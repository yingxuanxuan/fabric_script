#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging; logging.basicConfig(level=logging.INFO)
from fabric.api import reboot, sudo, settings

def ssserver(port, password, method):
    try:
        sudo('hash yum')
        sudo('hash python')
        sudo('yum -y update')
        sudo('yum -y install python-setuptools')
        sudo('yum -y install m2crypto')
        sudo('easy_install pip')
        sudo('pip install shadowsocks')
        sudo('hash ssserver')

        cmd = '/usr/bin/python /usr/bin/ssserver -p %s -k %s -m %s --user nobody -d start' % \
              (port, password, method)
        sudo("sed -i '$a %s' /etc/rc.d/rc.local" % cmd)
        sudo("chmod +x /etc/rc.d/rc.local")
        sudo("firewall-cmd --zone=public --add-port=%s/tcp --permanent" % port)

        with settings(warn_only=True):
            reboot()
        sudo('ps -ef | grep ssserver')
        return True

    except BaseException as e:
        logging.error(e)
        return False

def sslocal(server_addr, server_port, password, method, local_port):
    try:
        sudo('hash yum')
        sudo('hash python')
        sudo('yum -y update')
        sudo('yum -y install python-setuptools')
        sudo('yum -y install m2crypto')
        sudo('easy_install pip')
        sudo('pip install shadowsocks')
        sudo('hash sslocal')

        cmd = '/usr/bin/python /usr/bin/sslocal -s %s -p %s -k %s -m %s -l %s --user nobody -d start' % \
              (server_addr, server_port, password, method, local_port)
        sudo("sed -i '$a %s' /etc/rc.d/rc.local" % cmd)
        sudo("chmod +x /etc/rc.d/rc.local")
        sudo("firewall-cmd --zone=public --add-port=%s/tcp --permanent" % local_port)

        with settings(warn_only=True):
            reboot()
        sudo('ps -ef | grep sslocal')
        return True

    except BaseException as e:
        logging.error(e)
        return False