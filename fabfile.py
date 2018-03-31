import fabric
import os

PROJECT_ROOT = os.path.join('/home', 'www-data', 'sites', 'production', 'obelektrike')
ENV_ROOT = os.path.join(PROJECT_ROOT, 'env')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

fabric.api.env.roledefs['production'] = ['185.22.62.11']


def production_env():
    fabric.api.env.project_root = PROJECT_ROOT
    fabric.api.env.shell = '/bin/bash -c'
    fabric.api.env.python = os.path.join(ENV_ROOT, 'bin', 'python')
    fabric.api.env.pip = os.path.join(ENV_ROOT, 'bin', 'pip')
    fabric.api.env.uwsgi = os.path.join(ENV_ROOT, 'bin', 'uwsgi')  
    fabric.api.env.always_use_pty = False


def deploy():
    with fabric.api.cd(fabric.api.env.project_root):
        fabric.api.run('git pull origin master')
        fabric.api.run('{pip} install -r requirements.txt'.format(pip=fabric.api.env.pip))
        fabric.api.run('{python} manage.py initenv'.format(python=fabric.api.env.python))
        fabric.api.sudo('{uwsgi} --reload devops/wsgi.pid'.format(uwsgi=fabric.api.env.uwsgi))


def download_snapshot():
    snapshot_folder = '/tmp/snapshot'
    with fabric.api.cd(fabric.api.env.project_root):
        fabric.api.run('rm -rf %s.zip' % snapshot_folder)
        fabric.api.run('rm -rf %s' % snapshot_folder)
        fabric.api.run('mkdir %s' % snapshot_folder)
        fabric.api.run('pg_dump -U django_person dbobelektrike > %s/dbobelektrike.pgsql' % snapshot_folder)
        fabric.api.run('cp -rf %s/media %s/media' % (PROJECT_ROOT, snapshot_folder))
        fabric.api.run('zip -r %s.zip %s' % (snapshot_folder, snapshot_folder))
        fabric.api.get('%s.zip' % snapshot_folder, './')
        fabric.api.run('rm -rf %s' % snapshot_folder)


@fabric.api.roles('production')
def prod():
    production_env()
    deploy()


@fabric.api.roles('production')
def snapshot():
    production_env()
    download_snapshot()


def apply_snapshot():
    """
    sudo apt install unzip postgresql
    add trust for postgres in vim /etc/postgresql/9.5/main/pg_hba.conf
    sudo service postgresql restart

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'obelektrike',
            'USER': 'django_person',
            'PASSWORD': 'django_person',
            'HOST': 'localhost',
        }
    }
    """
    fabric.api.local('rm -rf %s/tmp' % BASE_DIR)
    fabric.api.local('rm -rf %s/media' % BASE_DIR)
    fabric.api.local('unzip %s/snapshot.zip' % BASE_DIR)
    fabric.api.local('mv %s/tmp/snapshot/media %s/media' % (BASE_DIR, BASE_DIR))
    fabric.api.local('psql -U postgres -c "DROP DATABASE IF EXISTS obelektrike"')
    fabric.api.local('psql -U postgres -c "DROP USER IF EXISTS django_person;"')
    fabric.api.local('psql -U postgres -c "CREATE USER django_person WITH PASSWORD \'django_person\'"')
    fabric.api.local('psql -U postgres -c "ALTER USER django_person CREATEDB;"')
    fabric.api.local('psql -U postgres -c "CREATE DATABASE obelektrike OWNER django_person"')
    fabric.api.local('psql -U django_person obelektrike < %s/tmp/snapshot/dbobelektrike.pgsql' % BASE_DIR)
    fabric.api.local('rm -rf %s/tmp' % BASE_DIR)