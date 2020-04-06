import glob
import json
import os

workers = {}
pools = {}
for instance_file_path in glob.glob('workers/**/*.json', recursive = True):
  with open(instance_file_path, 'r') as instance_file_read:
    instance = json.load(instance_file_read)
    domain, pool = instance['WorkerPool'].split('/')
    project = domain[:domain.rindex('-')] if '-' in domain else domain

    instanceTaskCount = 0
    instanceTasks = None
    instanceClaim = None
    instanceExpires = None
    instance_tasks_file_path = instance_file_path.replace('/workers/', '/tasks/')
    if os.path.isfile(instance_tasks_file_path):
      with open(instance_tasks_file_path, 'r') as instance_tasks_file_read:
        instance_tasks = json.load(instance_tasks_file_read)
        if 'tasks' in instance_tasks:
          instanceTasks = instance_tasks['tasks']
          instanceTaskCount = len(instanceTasks)
        if 'claim' in instance_tasks:
          instanceClaim = instance_tasks['claim']
        if 'expires' in instance_tasks:
          instanceClaim = instance_tasks['expires']

    if not project in pools:
      pools[project] = {'count': {'instance': 1, 'task': instanceTaskCount}}
    else:
      pools[project]['count']['instance'] += 1
      pools[project]['count']['task'] += instanceTaskCount
    if not domain in pools[project]:
      pools[project][domain] = {'count': {'instance': 1, 'task': instanceTaskCount}}
    else:
      pools[project][domain]['count']['instance'] += 1
      pools[project][domain]['count']['task'] += instanceTaskCount
    if not pool in pools[project][domain]:
      pools[project][domain][pool] = {'count': {'instance': 1, 'task': instanceTaskCount}}
    else:
      pools[project][domain][pool]['count']['instance'] += 1
      pools[project][domain][pool]['count']['task'] += instanceTaskCount

    if not instance['WorkerPool'] in workers:
      workers[instance['WorkerPool']] = []
    worker = {
      'id': instance['InstanceId'],
      'launch': instance['LaunchTime'],
    }
    if instanceClaim is not None:
      worker['claim'] = instanceClaim
    if instanceExpires is not None:
      worker['expires'] = instanceExpires
    if instanceTasks is not None:
      worker['tasks'] = list(map(lambda x: '{}/{}'.format(x['task'], x['run']), instanceTasks))
    workers[instance['WorkerPool']].append(worker)
    print('{}/{}/{}/{} indexed'.format(project, domain, pool, worker['id']))

pools_index_path = 'pools.json'
try:
  os.remove(pools_index_path)
except OSError:
  pass
with open(pools_index_path, 'w') as pools_file:
  json.dump(pools, pools_file, indent = 2)
print('{} saved'.format(pools_index_path))

for project in filter(lambda x: x != 'count', pools):
  for domain in filter(lambda x: x != 'count', pools[project]):
    for pool in filter(lambda x: x != 'count', pools[project][domain]):
      pool_index_path = '{}-{}.json'.format(domain, pool)
      try:
        os.remove(pool_index_path)
      except OSError:
        pass
      with open(pool_index_path, 'w') as pool_file:
        json.dump(workers['{}/{}'.format(domain, pool)], pool_file, indent = 2)
      print('{} saved'.format(pool_index_path))