from fabric.api import *

env.user = 'admin'
env.key_filename = '~/.ssh/id_rsa'

@hosts('trystram.net')
def deploy_dist(dist_dir='/home/web/koken/dl/', bundle_name='netscriptgen.tar.gz'):
    local('tar czvf /tmp/{0} ~/ownCloud/Developpement/NetScriptGen/target/dist/NetScriptGen-0.1.0/'.format(bundle_name))
    put(local_path="/tmp/{0}".format(bundle_name), remote_path='/tmp')
    with cd(dist_dir):
        with settings(warn_only=True):
            result = run('find {0}{1}'.format(dist_dir, bundle_name))
            # If the file already exists, we delete it
            if result.return_code == 0:
                print('Deleting the old bundle on remote host...')
                run('rm {0}'.format(bundle_name))
            print('Moving the new bundle from /tmp to {0}...'.format(dist_dir))
            run('mv /tmp/{0} .'.format(bundle_name))
    print('Removing the old bundle on local host.')
    local("rm /tmp/{0}".format(bundle_name))
