import yaml
import os
import threading

settings = {}
with open("arbuzov/rebuild.yml", 'r') as stream:
    try:
        settings = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

docker_path = settings['builder']['docker_main_path']
source_path = settings['builder']['source_main_path']

if not os.path.exists(source_path):
	os.makedirs(source_path)
	
os.chdir(docker_path)
os.system('docker-compose down')
#/home/arb/pragmatic/docker-bp

class ThreadBuilder(threading.Thread):
    def __init__(self, service):
        super(ThreadBuilder, self).__init__()
        self.service = service

    def run(self):
        try:
			self.process()
            
        except:
            print "!!!!!!!!!!!!!!!!!!!!!exception for type '%s' found!!!!!!!!!!!!!!!!!!!!!!!!!"%self.service

    def process(self):
		self.process_git()
		self.process_build()
	
    def process_git(self):
		path = self.service['source_path'] + '/' + self.service['project_dir']
		if not os.path.exists(path):
			print("creating dir `" + path + "`")
			os.makedirs(path)
			os.chdir(path)
			os.system('git clone ' + self.service['git'] + ' .')
			
		
		os.chdir(path)
		os.system('git reset --hard')
		os.system('git checkout  -f ' + self.service['branch'])
		os.system('git pull')
		
    def process_build(self):
		path = self.service['source_path'] + '/' + self.service['project_dir']

		os.chdir(path)
		os.system('mvn build')
		
		print (path)
		
		
		
workers = []
services = settings['builder']['services']
for service_name in services:
    #os.chdir(docker_path)
	service = settings['builder']['services'][service_name]
	service['source_path'] = source_path
	
	worker = ThreadBuilder(service)
	worker.start()
	workers.append(worker)
	print ()
    