import glob
import json
import os
import urllib.request


pool = os.environ['pool']
print(pool)


for instance_file_path in glob.glob('workers/{}/*.json'.format(pool)):
  with open(instance_file_path, 'r') as instance_file_read:
    instance = json.load(instance_file_read)
    print('{}/{} with {} in {} was launched at {}'.format(instance['WorkerPool'], instance['InstanceId'], instance['ImageId'], instance['AvailabilityZone'], instance['LaunchTime']))
    workerDomain, workerType = pool.split('/')
    instance_queue_url = 'https://firefox-ci-tc.services.mozilla.com/api/queue/v1/provisioners/{}/worker-types/{}/workers/aws/{}'.format(workerDomain, workerType, instance['InstanceId'])
    with urllib.request.urlopen(instance_queue_url) as response:
      instance_queue_data = json.loads(response.read().decode())
      if 'code' in instance_queue_data and instance_queue_data['code'] == 'ResourceNotFound':
        print(instance_queue_data['message'])
      else:
        instance['tc'] = instance_queue_data
        with open(instance_file_path, 'w') as instance_file_write:
          json.dump(instance, instance_file_write)
        print(instance)