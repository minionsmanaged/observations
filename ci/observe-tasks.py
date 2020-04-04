import glob
import os


pool = os.environ['pool']
print(pool)


for instance_file in glob.glob('workers/{}/*.json'.format(pool)):
  print(instance_file)

  #with open('workers/{}') as f:
  #  data = json.load(f)