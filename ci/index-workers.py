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
    if not project in pools:
      pools[project] = {}
    if not domain in pools[project]:
      pools[project][domain] = {}
    if not pool in pools[project][domain]:
      pools[project][domain][pool] = 1
    else:
      pools[project][domain][pool] += 1
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
for project in pools:
  for domain in pools[project]:
    for pool in pools[project][domain]:
      pool_index_path = '{}-{}.json'.format(domain, pool)
      try:
        os.remove(pool_index_path)
      except OSError:
        pass
      with open(pool_index_path, 'w') as pool_file:
        json.dump(workers['{}/{}'.format(domain, pool)], pool_file, indent = 2)
      print('{} saved'.format(pool_index_path))