import os

import click

__folder = ''
__delimiter = '\t'


def init_app(app):
    global __folder, __delimiter

    __folder = app.config.get('DATA_FOLDER') or app.instance_path
    __delimiter = app.config.get('DATA_DELIMITER') or '\t'

    app.cli.add_command(__install_command)
    app.cli.add_command(__reset_admin_command)


def get_path(filename):
    return os.path.join(__folder, filename)


def get_delimiter():
    return __delimiter


@click.command('install')
def __install_command():
    __install()
    __reset_admin()

    click.echo('Application installation successful.')


@click.command('reset-admin')
def __reset_admin_command():
    __reset_admin()

    click.echo('Admin reset successful.')


def __install():
    os.makedirs(__folder, exist_ok=True)

    RecipeRepository.install()
    UserRepository.install()


def __reset_admin():
    user = UserRepository.find_by_username('admin')

    if not user:
        user = User(username='admin')

    user.password = 'Admin123.'
    user.admin = True

    UserRepository.save(user)


from persistence.model.user import User
from persistence.repository.recipe import RecipeRepository
from persistence.repository.user import UserRepository
