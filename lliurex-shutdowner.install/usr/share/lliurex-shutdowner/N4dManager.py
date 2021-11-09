import xmlrpc.client
import ssl
import threading
import time
import os
import subprocess
import shutil


class N4dManager:
	
	def __init__(self,server=None):
		
		self.debug=True
		
		self.client=None
		self.user_groups=[]
		self.detected_clients=0
		self.validation=None
		self.shutdowner_var={}
		
		if server!=None:
			self.set_server(server)
		
		self.clearCache()

	#def init
	
	
	def dprint(self,msg):
		
		if self.debug:
			print(str(msg))
			
	#def dprint

	
	
	def set_server(self,server):

		context=ssl._create_unverified_context()	
		self.client=xmlrpc.client.ServerProxy("https://%s:9779"%server,allow_none=True,context=context)


	#def set_server

	def clearCache(self):

		clear=False
		user=os.environ["USER"]
		versionFile="/home/%s/.config/lliurex-shutdowner.conf"%user
		cachePath="/home/%s/.cache/lliurex-shutdowner-gui.py"%user
		installedVersion=self.getPackageVersion()

		if not os.path.exists(versionFile):
			with open(versionFile,'w') as fd:
				fd.write(installedVersion)
				fd.close()

			clear=True

		else:
			with open(versionFile,'r') as fd:
				fileVersion=fd.readline()
				fd.close()

			if fileVersion!=installedVersion:
				with open(versionFile,'w') as fd:
					fd.write(installedVersion)
					fd.close()
				clear=True
		
		if clear:
			if os.path.exists(cachePath):
				shutil.rmtree(cachePath)

	#def clearCache

	def getPackageVersion(self):

		command = "LANG=C LANGUAGE=en apt-cache policy lliurex-shutdowner"
		p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		installed = None
		for line in iter(p.stdout.readline,b""):
			if type(line) is bytes:
				line=line.decode()

			stripedline = line.strip()
			if stripedline.startswith("Installed"):
				installed = stripedline.replace("Installed: ","")

		return installed

	#def getPackageVersion
	
	def validate_user(self,user,password,standAlone):
			
		user_validated=False
		try:
			ret=self.client.validate_user(user,password)
		except:
			return user_validated
			
		user_validated,self.user_groups=ret
			
		
		if user_validated:
			self.validation=(user,password)
			self.get_shutdowner_values()
			if not standAlone:
				self.get_client_list()
				t=threading.Thread(target=self.update_client_list_thread)
				t.daemon=True
				t.start()

		
		return user_validated

	#def validate_user
	
	
	def get_shutdowner_values(self):
		
		self.shutdowner_var=self.client.get_variable("","VariablesManager","SHUTDOWNER")
		
	#def get_shutdowner_values
	
	
	def is_cron_enabled(self):
		
		return self.shutdowner_var["cron_enabled"]
		
	#def cron_enabled
	
	
	def get_cron_values(self):
		
		if self.shutdowner_var["cron_content"]!=None:
			return self.shutdowner_var["cron_values"]
		return None
		
	#def get_cron_values


	def get_server_cron_values(self):

		try:
			return self.shutdowner_var["server_cron"]["cron_server_values"]
		except Exception as e:
			self.shutdowner_var["server_cron"]={}
			self.shutdowner_var["server_cron"]["custom_shutdown"]=False
			self.shutdowner_var["server_cron"]["cron_server_content"]=""
			self.shutdowner_var["server_cron"]["cron_server_values"]={}
			self.shutdowner_var["server_cron"]["cron_server_values"]["minute"]=0
			self.shutdowner_var["server_cron"]["cron_server_values"]["hour"]=0
			self.shutdowner_var["server_cron"]["cron_server_values"]["weekdays"]=[True,True,True,True,True]
			return self.shutdowner_var["server_cron"]["cron_server_values"]

	#def get_server_cron_values
	
	
	def get_client_list(self):
		
		self.client.manual_client_list_check(self.validation,"ShutdownerManager")
		ret=self.client.get_client_list("","VariablesManager")
		
		count=0
		for item in ret:
			if ret[item]["missed_pings"]<1:
				count+=1
				
		self.detected_clients=count
		
	#def get_client_list
	
	
	def update_client_list_thread(self):
		
		while True:
			time.sleep(20)
			self.get_client_list()
			
	#def update_client_list_thread
	
	
	def set_shutdowner_values(self):

		self.client.save_variable(self.validation,"ShutdownerManager",self.shutdowner_var)
		
	#def set_shutdowner_values
	
	def shutdown_clients(self):
		
		self.client.update_shutdown_signal(self.validation,"ShutdownerManager")
		
	#def shutdown_clients
	
	
	def is_standalone_mode(self):

		context=ssl._create_unverified_context()	
		client=xmlrpc.client.ServerProxy("https://localhost:9779",allow_none=True,context=context)
		
		try:
			
			ret=client.get_variable("","VariablesManager","SRV_IP")
			
			if ret!=None:
				return False
			else:
				
				standAlone=False
				cmd='lliurex-version -v'
				p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
				result=p.communicate()[0]

				if type(result) is bytes:
					result=result.decode()

				flavours = [ x.strip() for x in result.split(',') ]

				for item in flavours:
					if 'server' in item:
						standAlone=False
						break
					elif 'client' in item:
						standAlone=False
						break
					elif 'desktop' in item:
						standAlone=True
				
				return standAlone
			
		except Exception as e:
			return True
		
	#def is_standalone_mode


	def is_server_shut(self):

		
		try:
			ret=self.client.is_server_shutdown_enabled(self.validation,"ShutdownerManager")
			return [ret['status'],ret['custom_shutdown']]
		except Exception as e:
			print('Exception: %s'%e)
			return [False,False]

	#def is_custom_server_shut
	
	
#class N4dManager
