import glob
import json
import os

workers = {}
pools = []
for instance_file_path in glob.glob('workers/**/*.json'):
  with open(instance_file_path, 'r') as instance_file_read:
    instance = json.load(instance_file_read)
    workerDomain, workerType = instance['WorkerPool'].split('/')
    if not instance['WorkerPool'] in pools:
      pools.append(instance['WorkerPool'])
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
        worker['tasks'] = map(lambda x: '{}/{}'.format(x['taskId'], x['runId']), instance['tc']['recentTasks'])
    workers[instance['WorkerPool']].append(worker)

pools_index_path = 'pools.json'
try:
  os.remove(pools_index_path)
except OSError:
  pass
with open(pools_index_path, 'w') as pools_file:
  json.dump(pools, pools_file, indent = 2)
for pool in pools:
  pool_index_path = '{}.json'.format(pool.replace('/', '-'))
  try:
    os.remove(pool_index_path)
  except OSError:
    pass
  with open(pool_index_path, 'w') as pool_file:
    json.dump(workers[pool], pool_file, indent = 2)