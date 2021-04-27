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
		self.shutdowner_var={}
		
		if server!=None:
			self.set_server(server)
		
	#def init
	
	
	def dprint(self,msg):
		
		if self.debug:
			print(str(msg))
			
	#def dprint


	def is_standalone_mode(self):

		try:
			client=self.client.get_variable("SRV_IP")
			return False
			
		except Exception as e:
			return True	
		
	#def is_standalone_mode



	def load_info(self):

		pp=self.get_shutdowner_values()
	
		if not self.is_standalone_mode():
			self.get_client_list()
			t=threading.Thread(target=self.update_client_list_thread)
			t.daemon=True
			t.start()
	
	#def load_info

		
	
	def set_server(self,server_ip):
		
		try:
			context=ssl._create_unverified_context()
			if server_ip in {'',None}:
				server_ip="server"
			if server_ip in {'localhost'}:
				proxy="https://localhost:9779"
				#print proxy
				self.client=xmlrpc.client.ServerProxy(proxy,allow_none=True,context=context)
			else:
				proxy="https://%s:9779"%server_ip
				#print proxy
				self.client=xmlrpc.client.ServerProxy(proxy,allow_none=True,context=context)
			
			self.server=server_ip

		except Exception as e:
			print(e)
			return [False,str(e)]

	#def set_server
	
	
	def validate_user(self,user,password):
			
		ret=self.client.validate_user(user,password)
		user_validated,self.user_groups=ret
			
		
		if user_validated:
			self.validation=(user,password)
			self.load_info()
		
		return ret

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
			self.shutdowner_var["server_cron"]["cron_server_values"]={}
			self.shutdowner_var["server_cron"]["cron_server_values"]["minute"]=''
			self.shutdowner_var["server_cron"]["cron_server_values"]["hour"]=''
			self.shutdowner_var["server_cron"]["cron_server_values"]["weekdays"]=['','','','','']
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
			
			if client.get_variable("","VariablesManager","SRV_IP") == None:
				return True
			else:
				return False
			
		except:
			
			return True
		
	#def is_standalone_mode


	def is_server_shut(self):

		try:
			ret=self.client.is_server_shutdown_enabled(self.validation,"ShutdownerManager")
			return [ret['status'],ret['custom_shutdown']]
		except Exception as e:
			print('Exception: %s'%e)

	#def is_custom_server_shut
	
	
#class N4dManager
