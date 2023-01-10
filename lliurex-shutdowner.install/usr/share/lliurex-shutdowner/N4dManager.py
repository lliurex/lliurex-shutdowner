import n4d.client
import threading
import subprocess
import time


class N4dManager:
	
	def __init__(self,ticket,passwd=None):

		self.debug=True
		ticket=ticket.replace('##U+0020##',' ')
		self.detected_clients=0
		self.local_passwd=passwd
		self.set_server(ticket)
		self.load_info()
		
	#def init
	
	def dprint(self,msg):
		
		if self.debug:
			print(str(msg))
			
	#def dprint
		
	
	def set_server(self,ticket):
		
		tk=n4d.client.Ticket(ticket)
		self.client=n4d.client.Client(ticket=tk)
		
	#def set_server
	
	
	def load_info(self):

		self.get_shutdowner_values()
	
		if not self.is_standalone_mode():
			self.get_client_list()
			t=threading.Thread(target=self.update_client_list_thread)
			t.daemon=True
			t.start()
		
	
	#def load_info
	
	
	def get_shutdowner_values(self):
		
		self.shutdowner_var=self.client.get_variable("SHUTDOWNER")
	
	#def get_shutdowner_values
	
	
	def is_cron_enabled(self):
		
		return self.shutdowner_var["cron_enabled"]
		
	#def is_cron_enabled
	
	
	def get_cron_values(self):
		
		if self.shutdowner_var["cron_content"]!=None:
			return self.shutdowner_var["cron_values"]
		return None
		
	#def get_cron_values

	def get_server_cron_values(self):

		return self.shutdowner_var["server_cron"]["cron_server_values"]

	#def get_server_cron_values	

	
	def get_client_list(self):
		
		self.client.ShutdownerManager.manual_client_list_check()
		ret=self.client.get_client_list()
		
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
		
		self.client.ShutdownerManager.save_variable(self.shutdowner_var)
		
	#def set_shutdowner_values
	
	def shutdown_clients(self):
		
		self.client.ShutdownerManager.update_shutdown_signal()
		
	#def shutdown_clients
	
	
	def is_standalone_mode(self):

		standAlone=False
		isClient=False
	
		try:
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
					isClient=True
					break
				elif 'desktop' in item:
					standAlone=True
			
			return standAlone,isClient
			
		except Exception as e:
			print(str(e))
			return True,isClient
	
		
	#def is_standalone_mode

	def is_server_shut(self):

		ret=self.client.ShutdownerManager.is_server_shutdown_enabled()
		
		return [ret['status'],ret['custom_shutdown']]
	#def is_custom_server_shut
	
#class N4dManager
