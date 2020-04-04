import glob
import json
import os


pool = os.environ['pool']
print(pool)


for instance_file_path in glob.glob('workers/{}/*.json'.format(pool)):
  with open(instance_file_path) as instance_file:
    instance = json.load(instance_file)
    print('{}/{} with {} in {} was launched at {}'.format(instance['WorkerPool'], instance['InstanceId'], instance['ImageId'], instance['AvailabilityZone'], instance['LaunchTime']))