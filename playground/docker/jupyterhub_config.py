import os
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = 'jupyter/datascience-notebook'
c.DockerSpawner.debug = True
c.JupyterHub.hub_ip = '192.168.0.116'
#c.JupyterHub.spawner_class = 'dockerspawner.SystemUserSpawner'
#c.SystemUserSpawner.host_homedir_format_string = '/app/{username}'
c.DockerSpawner.container_ip = '192.168.0.116'


#from pwd import getpwnam
#def fix_dir_hook(spawner):
#    username = spawner.user.name # get the username
#    home_path = os.path.join('/app', username)
#    if not os.path.exists(home_path):
#        os.chdir('/app')
#        os.mkdir(username)
#    uid = getpwnam(username).pw_uid
#    #os.chown(home_path, uid, 100)
#    os.chmod(home_path, 0o0777)
#    pass

#c.Spawner.pre_spawn_hook = fix_dir_hook
