#!/usr/bin/env python

from fabric.api import env, run, cd, prefix
from contextlib import contextmanager

PROJECT_DIR = '/home/davidciani/wordgame'
WSGI_SCRIPT = 'dispatch.fcgi'

env.hosts = ['chopin']
env.activate = 'source .env/bin/activate'

@contextmanager
def virtualenv(directory):
    with cd(directory):
        with prefix(env.activate):
            yield

def deploy():
    with virtualenv(PROJECT_DIR):
        run('git pull')
        run('pip install -r requirements.txt')
        run('touch %s' % WSGI_SCRIPT)

