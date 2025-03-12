import os
import n4d.client
import threading
import subprocess
import time
import xmlrpc.client as n4dclient
import ssl

class N4dManager:
	
	def __init__(self):

		self.debug=False
		self.adiServer="/usr/bin/natfree-server"
		self.adiClient="/usr/bin/natfree-client"
		self.detectedClients=0
		self.standAlone=False
		self.isClient=False
		self.isStandaloneMode()

	#def init
	
	def dprint(self,msg):
		
		if self.debug:
			print(str(msg))
			
	#def dprint
		
	def setServer(self,ticket,passwd):

		ticket=ticket.replace('##U+0020##',' ')
		tk=n4d.client.Ticket(ticket)
		self.client=n4d.client.Client(ticket=tk)
		
		if self.isClient:
			localUser=ticket.split(' ')[2]
			self.localClient=n4d.client.Client("https://localhost:9779",localUser,passwd)
			try:
				local_t=self.localClient.get_ticket()
				self.localClient=n4d.client.Client(ticket=local_t)
			except:
				pass
		
	#def setServer
	
	def loadInfo(self):

		ret=self.getShutdownerValues()

		if ret:
			if not self.standAlone:
				self.getClientList()
				t=threading.Thread(target=self.updateClientListThread)
				t.daemon=True
				t.start()

		return ret
		
	#def loadInfo
	
	def getShutdownerValues(self):
		
		try:
			self.shutdownerVar=self.client.get_variable("SHUTDOWNER")
			return True
		except:
			return False
	
	#def getShutdownerValues
	
	def isCronEnabled(self):
		
		return self.shutdownerVar["cron_enabled"]
		
	#def isCronEnabled
	
	def getCronValues(self):
		
		try:
			if self.shutdownerVar["cron_content"]!=None:
				return self.shutdownerVar["cron_values"]
		except:
			pass
			
		return None
		
	#def getCronValues

	def getServerCronValues(self):

		try:
			if self.shutdownerVar["server_cron"]["cron_server_values"]!=None:
				return self.shutdownerVar["server_cron"]["cron_server_values"]
		except:
			pass

		return None

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

		self.standAlone=False
		self.isClient=False
		isDesktop=False
	
		try:
			cmd='lliurex-version -v'
			p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			result=p.communicate()[0]

			if type(result) is bytes:
				result=result.decode()

			flavours = [ x.strip() for x in result.split(',') ]

			for item in flavours:
				if 'server' in item:
					self.standAlone=False
					break
				elif 'client' in item:
					self.isClient=True
				elif 'desktop' in item:
					isDesktop=True
					if os.path.exists(self.adiClient):
						self.isClient=True
					else:
						if not os.path.exists(self.adiServer):
							self.standAlone=True
			
			if self.isClient:
				if isDesktop:
					if self._checkConnectionWithServer():
						self.standAlone=False
					else:
						self.isClient=False
						self.standAlone=True
			
			return self.standAlone,self.isClient

		except Exception as e:
			self.standAlone=True
			self.isClient=False
	
	#def isStandaloneMode

	def isServerShut(self):

		ret=self.client.ShutdownerManager.is_server_shutdown_enabled()
		
		return [ret['status'],ret['custom_shutdown']]
	
	#def isServerShut

	def isClientShutdownOverride(self):

		self.isShutdownOverrideEnabled=False

		if self.isClient:
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
	
	def _checkConnectionWithServer(self):

		try:
			context=ssl._create_unverified_context()
			client=n4dclient.ServerProxy('https://server:9779',context=context,allow_none=True)
			test=client.is_cron_enabled('','ShutdownerManager')
			return True
		except Exception as e:
			return False

	#def _checkConnectionWithServer
	

#class N4dManager
