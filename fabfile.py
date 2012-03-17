import os
import sys

import fabric.api


fabric.api.env.user = 'ubuntu'
fabric.api.env.hosts = [os.environ.get('CT_HOST')]


def provision():
    import novaclient.client
    import novaclient.exceptions

    user = os.environ.get('OS_USERNAME')
    password = os.environ.get('OS_PASSWORD')
    tenant = os.environ.get('OS_TENANT_NAME')
    auth_url = os.environ.get('OS_AUTH_URL')
    flavor_name = os.environ.get('CT_FLAVOR_NAME', 'm1.large')
    image_name = os.environ.get('CT_IMAGE_NAME',
                                'oneiric-server-cloudimg-amd64')
    key_name = os.environ.get('CT_KEY_NAME', 'cloudtee')
    sec_group_name = os.environ.get('CT_SEC_GROUP_NAME', 'cloudtee')

    client = novaclient.client.Client('2', user, password, tenant, auth_url)
    image = client.images.find(name=image_name)
    flavor = client.flavors.find(name=flavor_name)

    try:
        client.keypairs.find(name=key_name)
    except novaclient.exceptions.NotFound:
        print 'Importing keypair as %s' % key_name
        key_data = open('%s/.ssh/id_rsa.pub' % os.environ.get('HOME')).read()
        client.keypairs.create(key_name, public_key=key_data)

    try:
        sec_group = client.security_groups.find(name=sec_group_name)
    except novaclient.exceptions.NotFound:
        print 'Creating security group %s' % sec_group_name
        sec_group = client.security_groups.create(sec_group_name,
                                                  sec_group_name)
        pg_id = sec_group.id
        client.security_group_rules.create(pg_id, 'tcp', 22, 22,
                                           '0.0.0.0/0')
        client.security_group_rules.create(pg_id, 'tcp', 8080, 8080,
                                           '0.0.0.0/0')

    try:
        floating_ip = client.floating_ips.find(instance_id=None)
    except novaclient.exceptions.NotFound:
        print 'Allocating new floating ip'
        floating_ip = client.floating_ips.create()

    userdata = """#!/bin/sh

sudo apt-get update
sudo apt-get install -y python-pip python-eventlet"""

    server = client.servers.create('cloudtee', image, flavor,
                                   key_name=key_name,
                                   userdata=userdata,
                                   security_groups=[sec_group_name])
    server_id = server.id

    # Wait for instance to get fixed ip
    for i in xrange(60):
        server = client.servers.get(server_id)
        if len(server.networks):
            break
        if i == 59:
            print 'Could not get fixed ip. Exiting...'
            sys.exit(1)

    server.add_floating_ip(floating_ip)
    print 'Success! Instance running at %s' % floating_ip.ip


def deploy():
    fabric.api.local('python setup.py sdist --formats=gztar', capture=False)
    pkg_name = fabric.api.local('python setup.py --fullname', capture=True)

    # upload
    fabric.api.put('dist/%s.tar.gz' % pkg_name, '/tmp/')

    # create environment
    fabric.api.run('mkdir /tmp/cloudtee')

    # unzip and install
    with fabric.api.cd('/tmp/cloudtee'):
        fabric.api.run('tar xzf /tmp/%s.tar.gz' % pkg_name)
        fabric.api.run('ls')

    with fabric.api.cd('/tmp/cloudtee/%s' % pkg_name):
        fabric.api.run('sudo python setup.py install')

    # cleanup
    fabric.api.run('sudo rm -rf /tmp/cloudtee')


def start():
    fabric.api.run('nohup bash -c "cloudtee-server &"')


def stop():
    fabric.api.run('killall cloudtee-server')
