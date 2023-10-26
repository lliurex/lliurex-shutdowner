import n4d.client
import threading
import subprocess
import time


class N4dManager:
	
	def __init__(self):

		self.debug=False
	
		self.detectedClients=0
		
	#def init
	
	def dprint(self,msg):
		
		if self.debug:
			print(str(msg))
			
	#def dprint
		
	def setServer(self,ticket,passwd):

		ticket=ticket.replace('##U+0020##',' ')
		tk=n4d.client.Ticket(ticket)
		self.client=n4d.client.Client(ticket=tk)
		
		if self.isStandaloneMode()[1]:
			localUser=ticket.split(' ')[2]
			self.localClient=n4d.client.Client("https://localhost:9779",localUser,passwd)
			local_t=self.localClient.get_ticket()
			self.localClient=n4d.client.Client(ticket=local_t)
		
	#def setServer
	
	def loadInfo(self):

		self.getShutdownerValues()

		if not self.isStandaloneMode()[0]:
			self.getClientList()
			t=threading.Thread(target=self.updateClientListThread)
			t.daemon=True
			t.start()
		
	#def loadInfo
	
	def getShutdownerValues(self):
		
		self.shutdownerVar=self.client.get_variable("SHUTDOWNER")
	
	#def getShutdownerValues
	
	def isCronEnabled(self):
		
		return self.shutdownerVar["cron_enabled"]
		
	#def isCronEnabled
	
	def getCronValues(self):
		
		if self.shutdownerVar["cron_content"]!=None:
			return self.shutdownerVar["cron_values"]
		return None
		
	#def getCronValues

	def getServerCronValues(self):

		return self.shutdownerVar["server_cron"]["cron_server_values"]

	#def getServerCronValues	

	def getClientList(self):
		
		self.client.ShutdownerManager.manual_client_list_check()
		ret=self.client.get_client_list()
		
		count=0
		for item in ret:
			if ret[item]["missed_pings"]<1:
				count+=1
				
		self.detectedClients=count
		
	#def getClientList
	
	def updateClientListThread(self):
		
		while True:
			time.sleep(20)
			self.getClientList()
			
	#def updateClientListThread
	
	def setShutdownerValues(self):
		
		self.client.ShutdownerManager.save_variable(self.shutdownerVar)
		
	#def setShutdownerValues
	
	def shutdownClients(self):
		
		self.client.ShutdownerManager.update_shutdown_signal()
		
	#def shutdownClients
	
	def isStandaloneMode(self):

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
			return True,isClient
	
	#def isStandaloneMode

	def isServerShut(self):

		ret=self.client.ShutdownerManager.is_server_shutdown_enabled()
		
		return [ret['status'],ret['custom_shutdown']]
	
	#def isServerShut

	def isClientShutdownOverride(self):

		self.isShutdownOverrideEnabled=False

		if self.isStandaloneMode()[1]:
			try:
				self.isShutdownOverrideEnabled=self.localClient.ShutdownerClient.is_shutdown_override_enabled()
			except:
				pass

		return self.isShutdownOverrideEnabled

	#def isClientShutdownOverride

	def switchOverrideShutdown(self,value):

		ret=False
		action="Enable"

		try:
			if value!=self.isShutdownOverrideEnabled:
				if value:
					action="Enable"
					ret=self.localClient.ShutdownerClient.enable_override_shutdown()

				else:
					action="Disable"
					ret=self.localClient.ShutdownerClient.disable_override_shutdown()
		except:
			pass

		return [action,ret]
			
	#def switchOverrideShutdown

#class N4dManager
