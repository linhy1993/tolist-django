from fabric.api import run, env
from fabric.context_managers import settings

env.key_filename = ['/home/hng/PycharmProjects/tdd_ch1/tdd_key.pem']


def _get_manage_dot_py(host):
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'


def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'ubuntu@{host}'):
        run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'ubuntu@{host}'):
        session_key = run(f'{manage_dot_py} create_session {email}')
        return session_key.strip()
