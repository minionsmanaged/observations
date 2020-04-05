import glob
import json
import os

workers = {}
projects = {}
for instance_file_path in glob.glob('workers/**/*.json', recursive = True):
  with open(instance_file_path, 'r') as instance_file_read:
    instance = json.load(instance_file_read)
    domain, worker = instance['WorkerPool'].split('/')
    project = domain[:domain.rindex('-')] if '-' in domain else domain
    if not project in projects:
      projects[project] = {}
    if not domain in projects[project]:
      projects[project][domain] = {}
    if not worker in projects[project][domain]:
      projects[project][domain][worker] = 1
    else:
      projects[project][domain][worker] += 1
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

pools_index_path = 'pools.json'
try:
  os.remove(pools_index_path)
except OSError:
  pass
with open(pools_index_path, 'w') as pools_file:
  json.dump(pools, pools_file, indent = 2)
for project in projects:
  for domain in project:
    for worker in domain:
      pool_index_path = '{}-{}.json'.format(domain, worker)
      try:
        os.remove(pool_index_path)
      except OSError:
        pass
      with open(pool_index_path, 'w') as pool_file:
        json.dump(workers['{}/{}'.format(domain, worker)], pool_file, indent = 2)