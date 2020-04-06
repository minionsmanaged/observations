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
        instance_queue_data = json.loads(response.read().decode())
        if instance_queue_data is not None:
          if 'recentTasks' in instance_queue_data and len(instance_queue_data['recentTasks']) > 0:
            instance_tasks = map(lambda x: { 'task': x['taskId'], 'run': x['runId'] }, instance_queue_data['recentTasks'])
            instance_tasks_file_path = instance_file_path.replace('/workers/', '/tasks/')
            with open(instance_tasks_file_path, 'w') as instance_tasks_file_write:
              json.dump({ 'claim': instance_queue_data['firstClaim'], 'expires': instance_queue_data['expires'], 'tasks': instance_tasks }, instance_tasks_file_write, indent = 2)
    except urllib.error.HTTPError as err:
      print('error reading: {}'.format(instance_queue_url))
