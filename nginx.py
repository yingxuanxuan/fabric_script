#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import sudo, put, cd
import os


def setup():
    # update
    sudo('yum -y update 1>/dev/null')

    # key
    sudo('yum -y install wget')
    sudo('wget http://nginx.org/keys/nginx_signing.key -O nginx_signing.key')
    sudo('rpm --import nginx_signing.key')
    sudo('rm -f nginx_signing.key')

    # repo
    repo = '''[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/mainline/centos/7/$basearch/
gpgcheck=1
enabled=1'''

    sudo("echo '%s' > /etc/yum.repos.d/nginx.repo" % repo)
    sudo('yum -y install nginx 1>/dev/null')

    # enable
    sudo('systemctl enable nginx')

    # start
    sudo('systemctl start nginx')

    # firewall
    sudo('yum -y install firewalld 1>/dev/null')
    sudo('systemctl enable firewalld')
    sudo('systemctl start firewalld')
    sudo('firewall-cmd --zone=public --add-service=http --permanent')
    sudo('firewall-cmd --zone=public --add-service=https --permanent')
    sudo('firewall-cmd --reload')


def config(config_file_path):
    # get file name
    config_file_name = os.path.basename(config_file_path)

    # check file name
    if not config_file_path.endswith('.conf'):
        config_file_name += '.conf'

    # upload config file
    with cd('/etc/nginx/conf.d/'):
        put(config_file_path, config_file_name)

    # reload
    sudo('systemctl reload nginx')