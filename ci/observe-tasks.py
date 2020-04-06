import glob
import json
import os
import urllib.request
from urllib.error import HTTPError


pool = os.environ['pool']
print(pool)

if not os.path.isdir('tasks/{}'.format(pool))
  os.makedirs('tasks/{}'.format(pool))

for instance_file_path in glob.glob('workers/{}/*.json'.format(pool)):
  with open(instance_file_path, 'r') as instance_file_read:
    instance = json.load(instance_file_read)
    workerDomain, workerType = pool.split('/')
    print('{}/{}/{} with {} in {} was launched at {}'.format(workerDomain, workerType, instance['InstanceId'], instance['ImageId'], instance['AvailabilityZone'], instance['LaunchTime']))
    instance_queue_url = 'https://firefox-ci-tc.services.mozilla.com/api/queue/v1/provisioners/{}/worker-types/{}/workers/aws/{}'.format(workerDomain, workerType, instance['InstanceId'])
    try:
      with urllib.request.urlopen(instance_queue_url) as response:
        queue_response = json.loads(response.read().decode())
        if queue_response is not None:
          instance_queue_data = {}
          if 'firstClaim' in queue_response:
            instance_queue_data['claim'] = queue_response['firstClaim']
          if 'expires' in queue_response:
            instance_queue_data['expires'] = queue_response['expires']
          if 'recentTasks' in queue_response and len(queue_response['recentTasks']) > 0:
            instance_queue_data['tasks'] = map(lambda x: { 'task': x['taskId'], 'run': x['runId'] }, queue_response['recentTasks'])

          instance_tasks_file_path = instance_file_path.replace('/workers/', '/tasks/')
          with open(instance_tasks_file_path, 'w') as instance_tasks_file_write:
            json.dump(instance_queue_data, instance_tasks_file_write, indent = 2)
    except urllib.error.HTTPError as err:
      print('error reading: {}'.format(instance_queue_url))
