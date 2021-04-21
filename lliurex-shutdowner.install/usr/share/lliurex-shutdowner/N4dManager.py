import xmlrpc.client
import ssl
import threading
import time


class N4dManager:
	
	def __init__(self,server=None):
		
		self.debug=True
		
		self.client=None
		self.user_validated=False
		self.user_groups=[]
		self.detected_clients=0
		self.validation=None
		
		if server!=None:
			self.set_server(server)
		
	#def init
	
	
	def dprint(self,msg):
		
		if self.debug:
			print(str(msg))
			
	#def dprint
		
	
	def set_server(self,server):
		
		context=ssl._create_unverified_context()	
		self.client=xmlrpc.client.ServerProxy("https://%s:9779"%server,allow_none=True,context=context)
		
	#def set_server
	
	
	def validate_user(self,user,password):
			
		ret=self.client.validate_user(user,password)
		user_validated,self.user_groups=ret
			
		
		if user_validated:
			self.validation=(user,password)
		
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
			
			if client.get_variable("","VariablesManager","SRV_IP") == None:
				return True
			else:
				return False
			
		except:
			
			return True
		
	#def is_standalone_mode


	def is_server_shut(self):

		ret=self.client.ShutdownerManager.is_server_shutdown_enabled()
		
		return [ret['status'],ret['custom_shutdown']]
	#def is_custom_server_shut
	
	
#class N4dManager
