#!/usr/bin/env python
# -*- coding: utf-8 -*

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GObject, GLib,Gdk,Gio

import signal
import gettext
import sys
import threading
import copy

import N4dManager

signal.signal(signal.SIGINT, signal.SIG_DFL)
gettext.textdomain('lliurex-shutdowner')
_ = gettext.gettext

CSS_FILE="/usr/share/lliurex-shutdowner/rsrc/style.css"

class LliurexShutdowner:
	
	def __init__(self,args_dic):
		
		self.shutdown_bin="/usr/sbin/shutdown-lliurex"
		self.cron_content="%s %s * * %s root %s >> /var/log/syslog\n"
		
		self.n4d_man=N4dManager.N4dManager()
		self.standalone_mode=self.is_standalone_mode()
		
		if self.standalone_mode:
			args_dic["server"]="localhost"
		
		self.n4d_man.set_server(args_dic["server"])
		
		
		
		if args_dic["gui"]:
			
			self.start_gui()
			GObject.threads_init()
			Gtk.main()
		
	#def __init__(self):
	
	
	def is_standalone_mode(self):
		
		return self.n4d_man.is_standalone_mode()
		
	#def is_standalone_mode
	
	
	def start_gui(self):

		builder=Gtk.Builder()
		builder.set_translation_domain('lliurex-shutdowner')
		builder.add_from_file("/usr/share/lliurex-shutdowner/rsrc/lliurex-shutdowner.ui")
		self.main_window=builder.get_object("main_window")
		
		self.main_box=builder.get_object("main_box")
		self.login_box=builder.get_object("login_box")
		self.cron_box=builder.get_object("cron_box")
		self.cron_box_data=builder.get_object("cron_box_data")
		self.cron_box_client=builder.get_object("cron_box_client")
		#self.cron_frame=builder.get_object("cron_frame")
		
		self.stack=Gtk.Stack()
		self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.stack.set_transition_duration(200)
		self.stack.add_titled(self.login_box,"login","Login")
		self.stack.add_titled(self.cron_box,"cron","Cron options")
		self.stack.show_all()
		
		self.main_box.pack_start(self.stack,True,True,0)
		
		#self.close_button=builder.get_object("close_button")
		self.login_button=builder.get_object("login_button")
		self.shutdown_button=builder.get_object("shutdown_button")
		
		self.user_entry=builder.get_object("user_entry")
		self.password_entry=builder.get_object("password_entry")
		self.server_ip_entry=builder.get_object("server_ip_entry")
		
		self.login_msg_label=builder.get_object("login_msg_label")
		self.detected_clients_label=builder.get_object("detected_clients_label")
		self.automatic_shutdown_label=builder.get_object("automatic_shutdown_label")
		self.cron_switch=builder.get_object("cron_switch")
		self.hour_spinbutton=builder.get_object("hour_spinbutton")
		self.minute_spinbutton=builder.get_object("minute_spinbutton")
		self.monday_tb=builder.get_object("monday_togglebutton")
		self.tuesday_tb=builder.get_object("tuesday_togglebutton")
		self.wednesday_tb=builder.get_object("wednesday_togglebutton")
		self.thursday_tb=builder.get_object("thursday_togglebutton")
		self.friday_tb=builder.get_object("friday_togglebutton")
		self.server_shutdown_cb=builder.get_object("server_shutdown_checkbutton")

		self.weekdays=[]
		self.weekdays.append(self.monday_tb)
		self.weekdays.append(self.tuesday_tb)
		self.weekdays.append(self.wednesday_tb)
		self.weekdays.append(self.thursday_tb)
		self.weekdays.append(self.friday_tb)
		
		self.login_button.grab_focus()
		
		self.connect_signals()
		self.set_css_info()
		
		if self.standalone_mode:
		
			#box3=builder.get_object("box3")
			box4=builder.get_object("box4")
			box4.set_margin_bottom(20)
			self.automatic_shutdown_label.set_text("Enable automatic shutdown")
			box8=builder.get_object("box8")
			self.server_ip_entry.set_text("localhost")
			self.server_ip_entry.hide()
			
			
			self.standalone_items=[self.server_shutdown_cb,self.cron_box_client]
			
			
		
		self.main_window.show()
		
	#def start_gui
	
	
	def connect_signals(self):
		
		self.main_window.connect("destroy",self.quit)
		self.main_window.connect("delete_event",self.check_changes)
		self.login_button.connect("clicked",self.login_clicked)
		self.user_entry.connect("activate",self.entries_press_event)
		self.password_entry.connect("activate",self.entries_press_event)
		self.server_ip_entry.connect("activate",self.entries_press_event)
		
		self.cron_switch.connect("notify::active",self.cron_switch_changed)
		#self.close_button.connect("clicked",self.check_changes)
		self.shutdown_button.connect("clicked",self.shutdown_button_clicked)
		
	#def connect_signals
	
	
	def change_sensitive_status(self,status):
		
		self.hour_spinbutton.set_sensitive(status)
		self.minute_spinbutton.set_sensitive(status)
		for item in self.weekdays:
			item.set_sensitive(status)
		self.server_shutdown_cb.set_sensitive(status)
					
	#def change_sensitive_status
		
	
	# CSS ###########################################################
	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path(CSS_FILE)
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		self.user_entry.set_name("CUSTOM-ENTRY")
		self.password_entry.set_name("CUSTOM-ENTRY")
		self.server_ip_entry.set_name("CUSTOM-ENTRY")
		self.cron_box_data.set_name("CARD-ITEM")
		self.cron_box_client.set_name("CARD-ITEM")
		self.detected_clients_label.set_name("DEFAULT-LABEL")
		self.automatic_shutdown_label.set_name("DEFAULT-LABEL")

	#def set_css_info	

	# SIGNALS ########################################################
	
	def entries_press_event(self,widget):
		
		self.login_clicked(None)
		
	#def entries_press_event
	
	
	def cron_switch_changed(self,widget,data):
		
		status=widget.get_active()
		self.change_sensitive_status(status)

	#def cron_switch_changed
	
	
	def check_changes(self,widget=True,event=True):
		
		
		if self.stack.get_visible_child_name()=="cron":
		
			new_var=self.gather_values()
			if new_var!=self.n4d_man.shutdowner_var:
				self.n4d_man.shutdowner_var=new_var
				print("[LliurexShutdowner] Updating value on close signal...")
				self.n4d_man.set_shutdowner_values()
			
			day_configured=False
			for cb in self.weekdays:
				if cb.get_active():
					day_configured=True
					break
			
			if self.cron_switch.get_active() and not day_configured:
				
				return True
				
		sys.exit(0)
		
	#def check_changes
	
	
	def shutdown_button_clicked(self,widget):
		
		self.n4d_man.shutdown_clients()
		
	#def shutdown_button
	
	
	def login_clicked(self,widget):
		
		user=self.user_entry.get_text()
		password=self.password_entry.get_text()
		server=self.server_ip_entry.get_text()
		
		# HACK
		
		if server!="":
			self.n4d_man.set_server(server)
		
		
		self.login_msg_label.set_text(_("Validating user..."))
		
		self.login_button.set_sensitive(False)
		self.validate_user(user,password)
		
		
	#def login_clicked
	
	# ##################### ##########################################
	
	def validate_user(self,user,password):
		
		
		t=threading.Thread(target=self.n4d_man.validate_user,args=(user,password,))
		t.daemon=True
		t.start()
		GLib.timeout_add(500,self.validate_user_listener,t)
		
	#def validate_user
	
	
	def validate_user_listener(self,thread):
			
		if thread.is_alive():
			return True
				
		self.login_button.set_sensitive(True)
		if not self.n4d_man.user_validated:
			self.login_msg_label.set_markup("<span foreground='red'>"+_("Invalid user")+"</span>")
		else:
			group_found=False
			for g in ["sudo","admins","teachers"]:
				if g in self.n4d_man.user_groups:
					group_found=True
					break
					
			if group_found:
				self.login_msg_label.set_text("")
				
				#self.cron_frame.set_sensitive(self.n4d_man.is_cron_enabled())
				self.cron_switch.set_active(self.n4d_man.is_cron_enabled())
				
				if not self.cron_switch.get_active():
					self.change_sensitive_status(False)
				
				self.detected_clients_label.set_text(_("Currently detected clients: %s")%self.n4d_man.detected_clients)
				GLib.timeout_add(2000,self.client_list_listener)
				GLib.timeout_add(5000,self.save_values_thread)

				values=self.n4d_man.get_cron_values()
				if values!=None:
					self.monday_tb.set_active(values["weekdays"][0])
					self.tuesday_tb.set_active(values["weekdays"][1])
					self.wednesday_tb.set_active(values["weekdays"][2])
					self.thursday_tb.set_active(values["weekdays"][3])
					self.friday_tb.set_active(values["weekdays"][4])
					self.hour_spinbutton.set_value(values["hour"])
					self.minute_spinbutton.set_value(values["minute"])
					self.server_shutdown_cb.set_active(values["server_shutdown"])
				
				
				self.stack.set_visible_child_name("cron")
				
				for item in self.standalone_items:
					item.hide()
					
			else:
				self.login_msg_label.set_markup("<span foreground='red'>"+_("Invalid user")+"</span>")
				
		return False
			
	#def validate_user_listener
	
	
	def client_list_listener(self):
		
		self.detected_clients_label.set_text(_("Currently detected clients: %s")%self.n4d_man.detected_clients)
		return True
		
	#def  client_list_listener
	
	
	def save_values_thread(self):
		
		new_var=self.gather_values()

		if new_var!=self.n4d_man.shutdowner_var:
			self.n4d_man.shutdowner_var=new_var
			print("[LliurexShutdowner] Updating shutdowner variable...")
			t=threading.Thread(target=self.n4d_man.set_shutdowner_values)
			t.daemon=True
			t.start()
			
		return True
		
	#def save_values_thread
	

	def gather_values(self):
		
		new_var=copy.deepcopy(self.n4d_man.shutdowner_var)
		new_var["cron_enabled"]=self.cron_switch.get_active()
		if self.cron_switch.get_active():
			
			day_configured=False
			
			for cb in self.weekdays:
				if cb.get_active():
					day_configured=True
					break

			if day_configured:
				
				minute=self.minute_spinbutton.get_value_as_int()
				hour=self.hour_spinbutton.get_value_as_int()
				
				new_var["cron_values"]["weekdays"][0]=self.monday_tb.get_active()
				new_var["cron_values"]["weekdays"][1]=self.tuesday_tb.get_active()
				new_var["cron_values"]["weekdays"][2]=self.wednesday_tb.get_active()
				new_var["cron_values"]["weekdays"][3]=self.thursday_tb.get_active()
				new_var["cron_values"]["weekdays"][4]=self.friday_tb.get_active()
				new_var["cron_values"]["server_shutdown"]=self.server_shutdown_cb.get_active()
				new_var["cron_values"]["hour"]=hour
				new_var["cron_values"]["minute"]=minute
			
				days=""
				
				count=1
				for day in new_var["cron_values"]["weekdays"]:
					if day:
						days+="%s,"%count
					count+=1
			
				days=days.rstrip(",")
				new_var["cron_content"]=self.cron_content%(minute,hour,days,self.shutdown_bin)
				
			else:
				new_var["cron_enabled"]=False
				
		return new_var
		
	#def gather_values

	def quit(self,widget):

		self.check_changes()
		Gtk.main_quit()	

	#def quit		
	
#class LliurexShutdowner


if __name__=="__main__":
	
	pass
	
