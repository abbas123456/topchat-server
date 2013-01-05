from fabric.api import local, run, sudo, env, settings
from fabric.colors import green
from fabric.context_managers import cd
from fabric.operations import put, prompt
from datetime import datetime
from fabconfig import *
from fabric.colors import _wrap_with

def deploy():
    env.user = prompt('Username for remote host?')
    print(green('Got user %s' % env.user))
    archive_file_path = '/tmp/build-%s.tar.gz' % datetime.now()
    archive_file_path = archive_file_path.replace(' ', '')
    print(green("Archiving file"))
    archive(archive_file_path, env.branch)
    print(green("Uploading file"))
    upload(archive_file_path, archive_file_path)
    print(green("Unpacking archive"))
    unpack(archive_file_path)
    print(green("Setting symlinks"))
    set_production_symlinks()
    print(green("Applying permissions"))
    apply_production_permissions()
    print(green("Reloading apache"))
    reload_apache()


def archive(archive_file, reference):
    local('git archive %s | gzip > %s ' % (reference, archive_file))


def upload(local_path, remote_path):
    put(local_path, remote_path)
    local('rm -f %s' % local_path)


def unpack(archive_path, temp_folder='/tmp/build_temp'):
    run('if [ -d "%s" ]; then rm -rf "%s"; fi' % (temp_folder, temp_folder))
    run('mkdir -p %s' % temp_folder)

    with cd('%s' % temp_folder):
        run('tar xzf %s' % archive_path)
        sudo('if [ -d "%(BuildRoot)s" ]; then rm -rf "%(BuildRoot)s"; fi'
             % env)
        sudo('mkdir -p %s' % env.BuildRoot)

    sudo('mv %s/* %s' % (temp_folder, env.BuildRoot))

    run('rm -rf %s' % temp_folder)
    run('rm -f %s' % archive_path)


def set_production_symlinks():
    sudo('if [ -h %(AppRoot)s/builds/live/production ]; then unlink %(AppRoot)s/builds/live/production; fi' % env)
    sudo('ln -sv %(AppRoot)s/builds/live/%(tag)s %(AppRoot)s/builds/live/production' % env)


def apply_production_permissions():
    sudo('chown -R www-data:www-data %(BuildRoot)s' % env)


def reload_apache():
    sudo('/etc/init.d/apache2 reload')
