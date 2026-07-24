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
		self.adiServer="/usr/bin/natfree-adi"
		self.adiClient="/usr/bin/natfree-tie"
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
		
		if not self.isClient:
			return True
		
		if 'https://localhost' in ticket:
			return False
		
		localUser=ticket.split(' ')[2]
		self.localClient=n4d.client.Client("https://localhost:9779",localUser,passwd)
		
		try:
			local_t=self.localClient.get_ticket()
			self.localClient=n4d.client.Client(ticket=local_t)
		except Exception as e:
			pass

		return True

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
		except Exception as e:
			return False
	
	#def getShutdownerValues
	
	def isCronEnabled(self):
		
		return self.shutdownerVar["cron_enabled"]
		
	#def isCronEnabled
	
	def getCronValues(self):
		
		if not hasattr(self,"shutdownerVar") or self.shutdownerVar is None:
			return None
	
		if self.shutdownerVar.get("cron_content",None) is not None:
				return self.shutdownerVar.get("cron_values")
		
		return None
		
	#def getCronValues

	def getServerCronValues(self):

		if not hasattr(self,"shutdownerVar") or self.shutdownerVar is None:
			return None
		
		serverCron=self.shutdownerVar.get("server_cron")
		if not isinstance(serverCron,dict):
			return None
		
		return serverCron.get("cron_server_values")
		
	#def getServerCronValues	

	def getClientList(self):
		
		count=0
		try:
			self.client.ShutdownerManager.manual_client_list_check()
			ret=self.client.get_client_list()
			
			if isinstance(ret,dict):
				for clientData in ret.values():
					if isinstance(clientData,dict) and clientData.get("missed_pings",0)<1:
						count+=1
		except Exception as e:
			pass
			
		self.detectedClients=count
		
	#def getClientList
	
	def updateClientListThread(self):
		
		while True:
			time.sleep(20)
			self.getClientList()
			
	#def updateClientListThread
	
	def setShutdownerValues(self,newVar):
		
		self.shutdownerVar=newVar
		try:
			self.client.ShutdownerManager.save_variable(self.shutdownerVar)
		except Exception as e:
			print(f"ERROR: {e}")
			pass
		
	#def setShutdownerValues
	
	def shutdownClients(self):
		
		self.client.ShutdownerManager.update_shutdown_signal()
		
	#def shutdownClients
	
	def isStandaloneMode(self):

		self.standAlone=False
		self.isClient=False

		if os.path.exists(self.adiServer):
			return self.standAlone

		if os.path.exists(self.adiClient):
			if self._checkConnectionWithADI():
				self.isClient=True
				return self.standAlone
		
		self.standAlone=True

		return self.standAlone
		
	#def isStandaloneMode

	def isServerShut(self):

		try:
			ret=self.client.ShutdownerManager.is_server_shutdown_enabled()
			return {"status":ret.get('status'),"data":ret.get('custom_shutdown')}
		except:
			return {"status":False,"data":""}
	
	#def isServerShut

	def isClientShutdownOverride(self):

		if not self.isClient:
			self.isShutdownOverrideEnabled=False
			return self.isShutdownOverrideEnabled
 
		try:
			self.isShutdownOverrideEnabled=self.localClient.ShutdownerClient.is_shutdown_override_enabled()
		except Exception as e:
			self.isShutdownOverrideEnabled=False

		return self.isShutdownOverrideEnabled

	#def isClientShutdownOverride

	def switchOverrideShutdown(self,value):

		ret=False
		action="Enable" if value else "Disable"

		if value==self.isShutdownOverrideEnabled:
			return {"action":action,"status":ret}
		try:
			ret=self.localClient.ShutdownerClient.enable_override_shutdown() if value else self.localClient.ShutdownerClient.disable_override_shutdown()

		except Exception as e:
			pass

		return {"action":action,"status":ret}
			
	#def switchOverrideShutdown
	
	def _checkConnectionWithADI(self):

		try:
			context=ssl._create_unverified_context()
			client=n4dclient.ServerProxy('https://server:9779',context=context,allow_none=True)
			test=client.is_cron_enabled('','ShutdownerManager')
			return True
		except Exception as e:
			return False

	#def _checkConnectionWithADI
	

#class N4dManager
