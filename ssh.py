#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from fabric.api import sudo, settings, local, put, cd

logging.basicConfig(level=logging.INFO)


def _ssh_config(new_ssh_port):
    # 禁止密码登录
    sudo("sed -i '/^PasswordAuthentication/s/yes/no/' /etc/ssh/sshd_config")
    # 禁止root登录
    sudo("sed -i '/^PermitRootLogin /d' /etc/ssh/sshd_config")
    sudo("sed -i '/^#PermitRootLogin/a PermitRootLogin no' /etc/ssh/sshd_config")
    # 更换端口
    sudo("sed -i '/^Port /d' /etc/ssh/sshd_config")
    sudo("sed -i '/^#Port/a Port %s' /etc/ssh/sshd_config" % new_ssh_port)
    # 打开新端口
    sudo("firewall-cmd --zone=public --add-port=%s/tcp --permanent" % new_ssh_port)
    # 关闭旧端口
    sudo("firewall-cmd --zone=public --remove-service=ssh --permanent")
    # 重启sshd
    sudo("systemctl restart sshd.service")
    # 重启防火墙
    sudo("firewall-cmd --reload")


def _ssh_keygen(passphrase, key_filename):
    local('ssh-keygen -t rsa -N "%s" -f %s' % (passphrase, key_filename))


def _add_user(adduser):
    # 检查用户是否存在
    with settings(warn_only=True):
        result = sudo('id %s' % adduser)
        if result.failed:
            logging.info('user %s not exist.' % adduser)

            # 创建用户
            sudo('useradd %s' % adduser)
        else:
            logging.info('user %s already exist.' % adduser)

    # 添加到wheel组
    sudo('sudo usermod -G wheel %s ' % (adduser))


def set_ssh_with_upload_key(adduser, public_key_path, new_ssh_port):
    try:
        # add user
        _add_user(adduser)

        # get home path
        output = sudo('eval echo ~%s' % adduser)
        homepath = output.split("/n")[0]
        sudo("mkdir -p %s/.ssh/" % homepath)
        # add public key

        with cd('%s/.ssh/' % homepath):
            put(public_key_path, './%s.pub' % adduser)
            sudo('cat ./%s.pub >> authorized_keys' % adduser)
            sudo('chown %s:%s authorized_keys' % (adduser, adduser))
            sudo('rm %s.pub' % adduser)

        # ssh config
        _ssh_config(new_ssh_port)
    except BaseException as e:
        logging.error(e)
        return False
    return True


def set_ssh_with_new_key(adduser, passphrase, key_filename, new_ssh_port):
    try:
        _ssh_keygen(passphrase, key_filename)
        return set_ssh_with_upload_key(adduser, key_filename + '.pub', new_ssh_port)

    except BaseException as e:
        logging.error(e)
        return False
