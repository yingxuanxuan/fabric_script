#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from fabric.api import sudo, cd

logging.basicConfig(level=logging.INFO)


def virtual_local_python(path=None, with_site_package=False):
    try:
        virtualenv_path = path if path else '/usr/local/pylocal_env'
        site_package = '' if with_site_package else '--no-site-package'

        sudo('hash yum')
        sudo('hash python')
        sudo('yum -y update')
        sudo('yum -y install python-setuptools')
        sudo('easy_install pip')
        sudo('pip install virtualenv')
        sudo('virtualenv %s %s' % (site_package, virtualenv_path))

    except BaseException as e:
        logging.error(e)
        return False

    return True


def virtual_python3(path=None, with_site_package=False):
    try:
        virtualenv_path = path if path else '/usr/local/py3_env'
        site_package = '' if with_site_package else '--no-site-package'

        sudo('hash yum')
        sudo('hash python')
        sudo('yum -y update 1>/dev/null')
        sudo('yum -y install python-setuptools 1>/dev/null')
        sudo('easy_install pip 1>/dev/null')
        sudo('pip install virtualenv 1>/dev/null')
        sudo('wget https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tar.xz -O Python-3.5.1.tar.xz')
        sudo('tar -Jxf Python-3.5.1.tar.xz')
        with cd("Python-3.5.1"):
            sudo('yum -y install make 1>/dev/null')
            sudo('yum -y install gcc 1>/dev/null')
            sudo('yum -y install gcc-c++ 1>/dev/null')
            sudo('yum -y install zlib-devel 1>/dev/null')
            sudo('yum -y install openssl-devel 1>/dev/null')
            sudo('./configure --prefix=/usr/local 1>/dev/null')
            sudo('make 1>/dev/null')
            sudo('make altinstall 1>/dev/null')
        sudo('virtualenv -p /usr/local/bin/python3.5 %s %s' % (site_package, virtualenv_path))
        sudo('rm -rf Python-3.5.1')
        sudo('rm -f Python-3.5.1.tar.xz')

    except BaseException as e:
        logging.error(e)
        return False

    return True


def virtual_python2(path=None, with_site_package=False):
    try:
        virtualenv_path = path if path else '/usr/local/py2_env'
        site_package = '' if with_site_package else '--no-site-package'

        sudo('hash yum')
        sudo('hash python')
        sudo('yum -y update 1>/dev/null')
        sudo('yum -y install python-setuptools 1>/dev/null')
        sudo('easy_install pip 1>/dev/null')
        sudo('pip install virtualenv 1>/dev/null')
        sudo('wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tar.xz -O Python-2.7.11.tar.xz')
        sudo('tar -Jxf Python-2.7.11.tar.xz')
        with cd("Python-2.7.11"):
            sudo('yum -y install make 1>/dev/null')
            sudo('yum -y install gcc 1>/dev/null')
            sudo('yum -y install gcc-c++ 1>/dev/null')
            sudo('yum -y install zlib-devel 1>/dev/null')
            sudo('yum -y install openssl-devel 1>/dev/null')
            sudo('./configure --prefix=/usr/local 1>/dev/null')
            sudo('make 1>/dev/null')
            sudo('make altinstall 1>/dev/null')
        sudo('virtualenv -p /usr/local/bin/python2.7 %s %s' % (site_package, virtualenv_path))
        sudo('rm -rf Python-2.7.11')
        sudo('rm -f Python-2.7.11.tar.xz')

    except BaseException as e:
        logging.error(e)
        return False

    return True
