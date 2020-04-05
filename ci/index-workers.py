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
    instanceTaskCount = len(instance['tc']['recentTasks']) if 'tc' in instance and 'recentTasks' in instance['tc'] else 0

    if not project in pools:
      pools[project] = {'count': {'instance': 1, 'task': instanceTaskCount}}
    else:
      pools[project]['count']['instance'] =+ 1
      pools[project]['count']['task'] =+ instanceTaskCount
    if not domain in pools[project]:
      pools[project][domain] = {'count': {'instance': 1, 'task': instanceTaskCount}}
    else:
      pools[project][domain]['count']['instance'] =+ 1
      pools[project][domain]['count']['task'] =+ instanceTaskCount
    if not pool in pools[project][domain]:
      pools[project][domain][pool] = {'count': {'instance': 1, 'task': instanceTaskCount}}
    else:
      pools[project][domain][pool]['count']['instance'] =+ 1
      pools[project][domain][pool]['count']['task'] =+ instanceTaskCount

    if not instance['WorkerPool'] in workers:
      workers[instance['WorkerPool']] = []
    worker = {
      'id': instance['InstanceId'],
      'launch': instance['LaunchTime'],
    }
    if 'tc' in instance:
      if 'firstClaim' in instance['tc']:
        worker['claim'] = instance['tc']['firstClaim']
      if 'expires' in instance['tc']:
        worker['expires'] = instance['tc']['expires']
      if 'recentTasks' in instance['tc']:
        worker['tasks'] = list(map(lambda x: '{}/{}'.format(x['taskId'], x['runId']), instance['tc']['recentTasks']))
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

for project in filter(lamdba x: x != 'count', pools.keys()):
  for domain in filter(lamdba x: x != 'count', pools[project].keys()):
    for pool in filter(lamdba x: x != 'count', pools[project][domain].keys()):
      pool_index_path = '{}-{}.json'.format(domain, pool)
      try:
        os.remove(pool_index_path)
      except OSError:
        pass
      with open(pool_index_path, 'w') as pool_file:
        json.dump(workers['{}/{}'.format(domain, pool)], pool_file, indent = 2)
      print('{} saved'.format(pool_index_path))