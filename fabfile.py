import fabric
import os

PROJECT_ROOT = os.path.join('/home', 'www-data', 'sites', 'production', 'obelektrike')
ENV_ROOT = os.path.join(PROJECT_ROOT, 'env')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = 'db_obelektrike'

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
        fabric.api.run('{pip} install -r requirements/prod.txt'.format(pip=fabric.api.env.pip))
        fabric.api.run('{python} manage.py initenv'.format(python=fabric.api.env.python))
        fabric.api.sudo('{uwsgi} --reload devops/wsgi.pid'.format(uwsgi=fabric.api.env.uwsgi))


def download_snapshot():
    snapshot_folder = '/tmp/snapshot'
    with fabric.api.cd(fabric.api.env.project_root):
        fabric.api.run('rm -rf %s.zip' % snapshot_folder)
        fabric.api.run('rm -rf %s' % snapshot_folder)
        fabric.api.run('mkdir %s' % snapshot_folder)
        fabric.api.run('pg_dump -U django_person %s > %s/%s.pgsql' % (DB_NAME, snapshot_folder, DB_NAME))
        fabric.api.run('cp -rf %s/media %s/media' % (PROJECT_ROOT, snapshot_folder))
        fabric.api.run('zip -r %s.zip %s' % (snapshot_folder, snapshot_folder))
        fabric.api.get('%s.zip' % snapshot_folder, './')
        fabric.api.run('rm -rf %s' % snapshot_folder)


def apply_snapshot():
    """
    sudo apt install unzip postgresql
    add trust for postgres in vim /etc/postgresql/9.5/main/pg_hba.conf
    sudo service postgresql restart

    DATABASE_URL=postgres:///db_obelektrike
    """
    mac = True
    psql_u = 'postgres' if mac else '-U postgres'
    fabric.api.local('rm -rf %s/tmp' % BASE_DIR)
    fabric.api.local('rm -rf %s/media' % BASE_DIR)
    fabric.api.local('unzip %s/snapshot.zip' % BASE_DIR)
    fabric.api.local('mv %s/tmp/snapshot/media %s/media' % (BASE_DIR, BASE_DIR))
    fabric.api.local('psql %s -c "DROP DATABASE IF EXISTS %s"' % (psql_u, DB_NAME))
    fabric.api.local('psql %s -c "DROP USER IF EXISTS django_person;"' % psql_u)
    fabric.api.local('psql %s -c "CREATE USER django_person WITH PASSWORD \'django_person\'"' % psql_u)
    fabric.api.local('psql %s -c "ALTER USER django_person CREATEDB;"' % psql_u)
    fabric.api.local('psql %s -c "CREATE DATABASE %s OWNER django_person"' % (psql_u, DB_NAME))
    fabric.api.local('psql %s < %s/tmp/snapshot/%s.pgsql' % (DB_NAME, BASE_DIR, DB_NAME))
    fabric.api.local('rm -rf %s/tmp' % BASE_DIR)
    fabric.api.local('rm -rf %s/snapshot.zip' % BASE_DIR)


@fabric.api.roles('production')
def prod():
    production_env()
    deploy()


@fabric.api.roles('production')
def snapshot():
    production_env()
    download_snapshot()
    apply_snapshot()
