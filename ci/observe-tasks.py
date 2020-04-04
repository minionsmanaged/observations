import glob
import json
import os
import urllib.request
from urllib.error import HTTPError


pool = os.environ['pool']
print(pool)


for instance_file_path in glob.glob('workers/{}/*.json'.format(pool)):
  with open(instance_file_path, 'r') as instance_file_read:
    instance = json.load(instance_file_read)
    workerDomain, workerType = pool.split('/')
    print('{}/{}/{} with {} in {} was launched at {}'.format(workerDomain, workerType, instance['InstanceId'], instance['ImageId'], instance['AvailabilityZone'], instance['LaunchTime']))
    instance_queue_url = 'https://firefox-ci-tc.services.mozilla.com/api/queue/v1/provisioners/{}/worker-types/{}/workers/aws/{}'.format(workerDomain, workerType, instance['InstanceId'])
    try:
      with urllib.request.urlopen(instance_queue_url) as response:
        instance_queue_data = json.loads(response.read().decode())
        if 'code' in instance_queue_data and instance_queue_data['code'] == 'ResourceNotFound':
          print(instance_queue_data['message'])
        else:
          instance['tc'] = instance_queue_data
          with open(instance_file_path, 'w') as instance_file_write:
            json.dump(instance, instance_file_write)
          print(instance)
    except urllib.error.HTTPError as err:
      print('error reading: {}'.format(instance_queue_url))