import fabric.api

fabric.api.env.user = 'ubuntu'
fabric.api.env.hosts = ['50.56.12.248']


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
