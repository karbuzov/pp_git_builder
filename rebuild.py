import yaml
import os
import time
import threading

#settings = {}
#with open("arbuzov/rebuild.yml", 'r') as stream:
#    try:
#        settings = yaml.load(stream)
#    except yaml.YAMLError as exc:
#        print(exc)

#print(settings)
#docker_path = settings['builder']['docker_main_path']
#build_template = settings['builder']['build_template']
#source_path = settings['builder']['source_main_path']

#if not os.path.exists(source_path):
#    os.makedirs(source_path)
    
#os.chdir(docker_path)
#os.system('docker-compose down')
#/home/arb/pragmatic/docker-bp

class ThreadBuilder(threading.Thread):
#class ThreadBuilder():
    def __init__(self, service):
        super(ThreadBuilder, self).__init__()
        self.service = service

    def run(self):
        self.start()
        
    def start(self):
#        try:
        self.process()
        
#        except:
#            print "= = = = '%s' = = = ="%self.service

    def process(self):
        self.process_ansible()
#        self.process_git()
#        self.process_build()
#        self.process_copy()

    def process_ansible(self):
        runstr = "ansible-playbook buildfromgit.yml --extra-vars '" + self.service + "'"
        #os.chdir(path)
        os.system(runstr)
    
#    def process_git(self):
#        path = self.service['source_path'] + '/' + self.service['project_dir']
#        if not os.path.exists(path):
#            print("creating dir `" + path + "`")
#            os.makedirs(path)
#            os.chdir(path)
#            os.system('git clone ' + self.service['git'] + ' .')
#            
#        
#        os.chdir(path)
#        os.system('git reset --hard')
#        os.system('git checkout  -f ' + self.service['branch'])
#        os.system('git pull')
        
    def process_build(self):
        template = self.service['build_template']
        template = template.replace("{src_base_dir}", self.service['source_path'])
        template = template.replace("{src_dir}", self.service['project_dir'])
        
        os.system(template)
        
    def process_copy(self):
        path = self.service['source_path'] + '/' + self.service['project_dir']
        
        os.system(self.service['after_build'])
        
        
        
        

services = []
services.append('{branch: "develop",                localdir: "bingo", app: "bingo-gameserver", dockername: "bingo", "force": "false"}')
services.append('{branch: "develop",                localdir: "integration-service-emulator", app: "bingo-emulator", dockername: "emulator",  "force": "false"}')
services.append('{branch: "develop",                localdir: "integration-service", app: "bingo-integration-service", dockername: "integration-service",  "force": "false"}')
services.append('{branch: "develop",                localdir: "userservice", app: "bingo-user-service", dockername: "userservice",  "force": "false"}')
services.append('{branch: "develop",                localdir: "bingo-bonus-service", app: "bingo-bonus-service", dockername: "bingo-bonus-service",  "force": "false"}')
services.append('{branch: "develop",                localdir: "system-service", app: "bingo-system-service", dockername: "system-service", "force": "false"}')
services.append('{branch: "develop",                localdir: "bingo-chatserver", app: "bingo-chatserver", dockername: "bingo-chatserver", "force": "false"}')
services.append('{branch: "develop",                localdir: "bingo-generator", app: "bingo-generator", dockername: "bingo-generator", "force": "false"}')
services.append('{branch: "develop",                localdir: "bingo-generator", app: "bingo-generator", dockername: "bingo-generator", "force": "false"}')

workers = []
for item in services:
    #os.chdir(docker_path)
    #service = json.loads(item)

    
    worker = ThreadBuilder(item)
    worker.start()
    workers.append(worker)

for worker in workers:
    worker.join()
