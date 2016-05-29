#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import sudo, put, cd
import os


def setup():
    # update
    sudo('yum -y update 1>/dev/null')

    # epel
    sudo('yum -y install epel-release 1>/dev/null')

    # install
    sudo('yum -y install supervisor 1>/dev/null')

    # enable
    sudo('systemctl enable supervisord')

    # start
    sudo('systemctl start supervisord')


def config(config_file_path):
    # get file name
    config_file_name = os.path.basename(config_file_path)

    # check file name
    if not config_file_path.endswith('.ini'):
        config_file_name += '.ini'

    # upload config file
    with cd('/etc/supervisord.d/'):
        put(config_file_path, config_file_name)

    # reload
    sudo('systemctl reload supervisord')