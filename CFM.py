from tkinter import *
from tkinter import messagebox
import time
from tkinter import ttk
import mysql.connector
from mysql.connector import errorcode
import datetime
from datetime import date
import matplotlib.pyplot as mds
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import RPi.GPIO as GPIO
import clx.xms
import requests
import csv
import socket
from speedtest import Speedtest
import pickle
import sys
import os
import re
import shutoff


everyday = date.today()
d = everyday.strftime("%b_%d_%Y")
for_date = everyday.strftime("%d")
for_month = everyday.strftime("%m")
num_month = everyday.strftime("%m")
for_year = everyday.strftime("%Y")
et = everyday.strftime("%Y-%m-%d")
ct = everyday.strftime("%m")

root = Tk()
hour = time.strftime("%H")
minute = time.strftime("%M")
second = time.strftime("%S")
te = hour+':'+minute+':'+second

class datalog:
    def con_mysql(self):
        try:
            self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
            if self.cat.is_connected():
                tab_name='transaction_data'
                self.datacursor = self.cat.cursor(buffered=True)
                #self.datacursor.execute("SET SESSION MAX_EXECUTION_TIME=1000")
                check_table = ("SELECT count(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME=%s")
                self.datacursor.execute(check_table, (tab_name,))
                result = self.datacursor.fetchall()
                if result == [(1,)]:
                    self.success_login()
                    self.info_display.insert(END, "Info:\n Database connected...!\n Please select tool and start weighing...")
                    self.datacursor.execute("select YYYY_MM_DD from {today} order by YYYY_MM_DD DESC LIMIT 1".format(today= 'transaction_data'))
                    self.newtoken=  self.datacursor.fetchone()
                    if self.newtoken!=None:
                        self.newtoken=str(self.newtoken[0])
                    self.datacursor.execute("select * from {today} ORDER BY Sl_no DESC LIMIT 1".format(today= 'transaction_data'))
                    self.dq= self.datacursor.fetchone()

                else:
                    self.error_func()
                    self.error_display.insert(0.0, "Error:\n Critical file is missing in Database...!") 
            else:
                self.error_func()
                self.error_display.insert(0.0, "Error:\n Connecting Database failed...!")
        except mysql.connector.ProgrammingError as erlog:
            self.all_log=erlog
            self.error_func()
            self.error_display.insert(0.0, "Error: 1812A\n %s"%(self.all_log.msg))
            self.writing_log()
            
        except mysql.connector.errors.InterfaceError as erlog:
            self.all_log=erlog
            self.interface_error_handle()
            self.writing_log()
            
        except requests.exceptions.SSLError as erlog:
            self.all_log=erlog
            self.error_func()
            self.error_display.insert(0.0, "Error: 1812C\n %s"%(self.all_log))
            self.writing_log()
        
        except mysql.connector.errors.OperationalError as erlog:
            self.all_log=erlog
            self.error_func()
            self.error_display.insert(0.0, "Error: 1812D\n %s"%(self.all_log))
            self.writing_log()
        
        except Exception as erlog:
            self.all_log=erlog
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error: 1812H\n %s"%(self.all_log))
            self.writing_log()
    
    def writing_log(self):
        error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        te = hour+':'+minute+':'+second
        error_logging.write("{} {}, while starting the process {}\n".format(et,te,self.all_log))
        error_logging.close()
            
    def brokenpipe_error_handle(self):
        self.to_place_error_display()
        self.error_display.insert(0.0,"Error: 1812E\n BrokenPipe Error occured,|nPlease restart Application...!")
        error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        te = hour+':'+minute+':'+second
        error_logging.write("{} {}, Error code: 1812E, That means, that you there was a Linux pipe on your system. Then some process accessed that pipe to read from it. Then your Python process came and accessed to write to it. Then the first process closed its end of the pipe. But your process tried to write to the pipe. That caused your error. Either that or your process was the reader and the writer process closed its end of the pipe.\n".format(et,te))
        error_logging.close()
    
    def interface_error_handle(self):
        self.to_place_error_display()
        self.error_display.insert(0.0,"Error: 1812B\n Unable to communicate with Server...!\nCheck Internet, Server status & its Hostname...!")
        error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        te = hour+':'+minute+':'+second
        error_logging.write("{} {}, Error code: 1812B, This exception is raised for errors related to the interface (in our case interface is MySQL Connector/Python) rather than the database itself.\n".format(et,te))
        error_logging.close()

    def contact_num_error_handle(self):
        self.to_place_error_display()
        self.error_display.insert(0.0,"Error: 1201Q\n Entered Shopper contact num is not valid or it's empty...!\nCheck Please re-enter once again...!")
        error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        te = hour+':'+minute+':'+second
        error_logging.write("{} {}, Error code: 1201Q, Operator entered invalid Customer's contact number.\n".format(et,te))
        error_logging.close()
    
    def add_to_table(self):
        today= 'transaction_data'
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        te = hour+':'+minute+':'+second        
        try:
            self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
            if self.cat.is_connected():
                self.datacursor = self.cat.cursor(buffered=True)   
                check_table = ("SELECT count(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME=%s")
                self.datacursor.execute(check_table, (today,))
                result = self.datacursor.fetchall()
                if result == [(1,)]:
                    try:
                        self.datacursor.execute("SELECT count(*) as tot FROM {today}".format(today= 'transaction_data'))
                        data = self.datacursor.fetchall()                    
                        if data == [(0,)]:  # to check whether table is empty or not
                            try:
                                if self.push_contents!=[]:
                                    self.datacursor.execute("INSERT INTO {today} VALUES (%s,%s,%s,%s,NULL,%s,%s,%s,%s,%s,%s,%s,%s)".format(today= 'transaction_data'),(1,self.push_contents[0],et,te,self.push_contents[1],self.push_contents[4],self.push_contents[6],self.push_contents[7],self.discount,for_date,num_month,for_year,),)
                                    self.cat.commit()                        
                                    self.to_place_inform_display()
                                    self.info_display.insert(0.0, "info:\n Started running Token no 1")
                                    self.Internet_status = "Good"
                                    if (self.push_contents[2] == "F Mc_1"):  # setting machine status
                                        self.M1_status = "Busy"
                                        GPIO.output(self.m1_start_P,GPIO.LOW)
                                        self.M1_Sl_no =  1#(1,)
                                        self.M1_item = self.push_contents[1]
                                        self.M1_Token_no=self.push_contents[0]
                                        self.M1_drop_no = [self.push_contents[0],self.push_contents[1],self.push_contents[2],"Running...",self.push_contents[4],
                                            self.push_contents[5],self.push_contents[6],self.push_contents[7],]
                                    elif (self.push_contents[2] == "F Mc_2"):  # setting machine status
                                        self.M2_status = "Busy"
                                        GPIO.output(self.m2_start_P,GPIO.LOW)
                                        self.M2_Sl_no = 1#(1,)
                                        self.M2_item = self.push_contents[1]
                                        self.M2_Token_no=self.push_contents[0]
                                        self.M2_drop_no = [self.push_contents[0],self.push_contents[1],self.push_contents[2],"Running...",self.push_contents[4],self.push_contents[5],
                                            self.push_contents[6],self.push_contents[7],]
                                    elif (self.push_contents[2] == "F Mc_3"):  # setting machine status
                                        self.M3_status = "Busy"
                                        GPIO.output(self.m3_start_P,GPIO.LOW)
                                        self.M3_Sl_no = 1#(1,)
                                        self.M3_item = self.push_contents[1]
                                        self.M3_Token_no=self.push_contents[0]
                                        self.M3_drop_no = [self.push_contents[0],self.push_contents[1],self.push_contents[2],"Running...",self.push_contents[4],self.push_contents[5],self.push_contents[6],self.push_contents[7],]
                                    self.push_contents = []
                            except AttributeError as erlog:
                                self.all_log=erlog
                                self.to_place_error_display()
                                self.error_display.insert(0.0,"Error: 1812F\n Please select the Token_no from Queue and click RUN",)
                            except mysql.connector.errors.InterfaceError as erlog:
                                self.all_log=erlog
                                self.interface_error_handle()
                            except BrokenPipeError as erlog:
                                self.all_log=erlog
                                self.brokenpipe_error_handle()
                                self.writing_log()
                                
                        else:
                            try:
                                if self.push_contents != []:
                                    self.datacursor.execute("INSERT INTO {today} VALUES (NULL,%s,%s,%s,NULL,%s,%s,%s,%s,%s,%s,%s,%s)".format(today= 'transaction_data'),
                                        (self.push_contents[0],et,te,self.push_contents[1],self.push_contents[4],self.push_contents[6],self.push_contents[7],self.discount,for_date,num_month,for_year,),)
                                    self.cat.commit()
                                    self.to_place_inform_display()
                                    self.info_display.insert(0.0,"info:\n Started running Token no {}".format(self.push_contents[0]),)
                                    self.Internet_status = "Good"
                                    if self.push_contents[2] == "F Mc_1":
                                        self.M1_status = "Busy"
                                        GPIO.output(self.m1_start_P,GPIO.LOW)
                                        self.datacursor.execute("select Token_no from {today} order by Sl_no DESC LIMIT 1".format(today= 'transaction_data'))
                                        temp_serial=  self.datacursor.fetchone()
                                        self.M1_Sl_no = temp_serial[0] # saving serial no to update end_time into database
                                        self.M1_item = self.push_contents[1]
                                        self.M1_Token_no=self.push_contents[0]
                                        self.cat.commit()
                                        self.M1_drop_no = [self.push_contents[0],self.push_contents[1],self.push_contents[2],"Running...",self.push_contents[4],self.push_contents[5],self.push_contents[6],self.push_contents[7],]
                                    elif self.push_contents[2] == "F Mc_2":
                                        self.M2_status = "Busy"
                                        GPIO.output(self.m2_start_P,GPIO.LOW)
                                        self.datacursor.execute("select Token_no from {today} order by Sl_no DESC LIMIT 1".format(today= 'transaction_data'))
                                        temp_serial=  self.datacursor.fetchone()
                                        self.M2_Sl_no = temp_serial[0] # saving serial no to update end_time into database
                                        self.M2_item = self.push_contents[1]
                                        self.M2_Token_no=self.push_contents[0]
                                        self.cat.commit()
                                        self.M2_drop_no = [self.push_contents[0],self.push_contents[1],self.push_contents[2],"Running...",self.push_contents[4],self.push_contents[5],self.push_contents[6],self.push_contents[7],]
                                    elif self.push_contents[2] == "F Mc_3":
                                        self.M3_status = "Busy"
                                        GPIO.output(self.m3_start_P,GPIO.LOW)
                                        self.datacursor.execute("select Token_no from {today} order by Sl_no DESC LIMIT 1".format(today= 'transaction_data'))
                                        temp_serial=  self.datacursor.fetchone()
                                        self.M3_Sl_no = temp_serial[0] # saving serial no to update end_time into database
                                        self.M3_item = self.push_contents[1]
                                        self.M3_Token_no=self.push_contents[0]
                                        self.cat.commit()
                                        self.M3_drop_no = [self.push_contents[0],self.push_contents[1],self.push_contents[2],"Running...",self.push_contents[4],self.push_contents[5],self.push_contents[6],self.push_contents[7],]
                                    self.push_contents = []
                                
                            except AttributeError as erlog:
                                self.all_log=erlog
                                self.to_place_error_display()
                                self.error_display.insert(0.0,"Error: 1812F\n Please select the Token_no from Queue and click RUN",)
                            except mysql.connector.errors.InterfaceError as erlog:
                                self.all_log=erlog
                                self.interface_error_handle()
                            except BrokenPipeError as erlog:
                                self.all_log=erlog
                                self.brokenpipe_error_handle()
                                self.writing_log()                                      
                        
                    except BrokenPipeError as erlog:
                        self.all_log=erlog
                        self.brokenpipe_error_handle()
                        self.writing_log()            
                else:
                    self.to_place_error_display()
                    self.error_display.insert(0.0,"Error: 1201C\n Database table is missing, Please re-open the application...!",)
        except mysql.connector.errors.InterfaceError as erlog:
            self.all_log=erlog
            self.interface_error_handle()
            self.offline_token_no = self.push_contents[0]
            self.Internet_status = "Bad"
            self.inform_func()
            self.info_display.delete(0.0, END)
            self.info_display.insert(0.0, "info:\n Started running Token no {} in offline mode".format(self.push_contents[0]))
            if self.push_contents[2] == "F Mc_1":
                self.offline_token_no1 = self.push_contents[0]
                self.offline_start_time1 = te
                self.offline_Item1 = self.push_contents[1]
                self.offline_weight1 = self.push_contents[4]
                self.offline_discount1 = self.push_contents[5]
                self.offline_Amount1 = self.push_contents[6]
                self.offline_contact_no1 = self.push_contents[7]
                self.csv_M1_data_waiting = True
                self.M1_status = "Busy"
                GPIO.output(self.m1_start_P,GPIO.LOW)
                self.M1_drop_no = [self.push_contents[0],self.push_contents[1],self.push_contents[2],"Running...",self.push_contents[4],self.push_contents[5],self.push_contents[6],self.push_contents[7],]
            elif self.push_contents[2] == "F Mc_2":
                self.offline_token_no2 = self.push_contents[0]
                self.offline_start_time2 = te
                self.offline_Item2 = self.push_contents[1]
                self.offline_weight2 = self.push_contents[4]
                self.offline_discount2 = self.push_contents[5]
                self.offline_Amount2 = self.push_contents[6]
                self.offline_contact_no2 = self.push_contents[7]
                self.csv_M2_data_waiting = True
                self.M2_status = "Busy"
                GPIO.output(self.m2_start_P,GPIO.LOW)
                self.M2_drop_no = [self.push_contents[0],self.push_contents[1],self.push_contents[2],"Running...",self.push_contents[4],self.push_contents[5],self.push_contents[6],self.push_contents[7],]
            elif self.push_contents[2] == "F Mc_3":
                self.offline_token_no3 = self.push_contents[0]
                self.offline_start_time3 = te
                self.offline_Item3 = self.push_contents[1]
                self.offline_weight3 = self.push_contents[4]
                self.offline_discount3 = self.push_contents[5]
                self.offline_Amount3 = self.push_contents[6]
                self.offline_contact_no3 = self.push_contents[7]
                self.csv_M3_data_waiting = True
                self.M3_status = "Busy"
                GPIO.output(self.m3_start_P,GPIO.LOW)
                self.M3_drop_no = [self.push_contents[0],self.push_contents[1],self.push_contents[2],"Running...",self.push_contents[4],self.push_contents[5],self.push_contents[6],self.push_contents[7],]
                
    def offline_csv_handling(self):
        filename = d + ".csv"
        with open(filename, "r") as offlinecfm:
            offlinecfmreader = csv.reader(offlinecfm)
            next(offlinecfmreader) #To start reading from 2nd line
            self.datacursor.execute("SELECT count(*) as tot FROM {today}".format(today= 'transaction_data'))
            data = self.datacursor.fetchall()
            for updating in offlinecfmreader:    
                if data == [(0,)]:  # to check whether table is empty or not
                    try:
                        self.datacursor.execute("INSERT INTO {today} VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(today= 'transaction_data'),
                            (1,updating[0],et,updating[1],updating[2],updating[3],updating[4],updating[5],updating[6],updating[7],updating[8],updating[9],for_year,),)
                        self.cat.commit()
                    except:
                        pass
                else:
                    try:
                        self.datacursor.execute("INSERT INTO {today} VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(today= 'transaction_data'),
                        (updating[0],et,updating[1],updating[2],updating[3],updating[4],updating[5],updating[6],updating[7],updating[8],updating[9],for_year,),)
                        self.cat.commit()
                    except:
                        pass
        offlinecfm.close()
        os.remove(filename)

    def update_M1_table(self):
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        te = hour+':'+minute+':'+second
        if self.Internet_status=="Good" and self.csv_M1_data_waiting != True:
            try:
                self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                if self.cat.is_connected():
                    self.datacursor = self.cat.cursor(buffered=True)
                    self.datacursor.execute("UPDATE {today} SET End_time=%s WHERE Token_no=%s".format(today= 'transaction_data'),(te,self.M1_Sl_no,),)
                    self.cat.commit()
                    for afterrun in self.select_treeview.get_children():#To delete specific row in treeview
                        if self.select_treeview.item(afterrun)["values"] == self.M1_drop_no:
                            self.select_treeview.delete(afterrun)
                    self.to_place_inform_display()
                    self.info_display.insert(0.0,"info:\n Token no {} completed...!\n Please select next token_no to run".format(self.M1_Token_no),)
                    self.M1_Sl_no = int
                    self.M1_status = "Ready"
            except mysql.connector.errors.ProgrammingError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812A\n None item is running in F Mc_1")
                error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                hour = time.strftime("%H")
                minute = time.strftime("%M")
                second = time.strftime("%S")
                te = hour+':'+minute+':'+second
                error_logging.write("{} {}, while updating M1 data {}\n".format(et,te,self.all_log))
                error_logging.close()
            except BrokenPipeError as erlog:
                self.all_log=erlog
                self.brokenpipe_error_handle()
                error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                hour = time.strftime("%H")
                minute = time.strftime("%M")
                second = time.strftime("%S")
                te = hour+':'+minute+':'+second
                error_logging.write("{} {}, while updating M1 data {}\n".format(et,te,self.all_log))
                error_logging.close()
            except mysql.connector.errors.InterfaceError as erlog:
                self.all_log=erlog
                self.interface_error_handle()
                error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                hour = time.strftime("%H")
                minute = time.strftime("%M")
                second = time.strftime("%S")
                te = hour+':'+minute+':'+second
                error_logging.write("{} {}, while updating M1 data {}\n".format(et,te,self.all_log))
                error_logging.close()
                for afterrun in self.select_treeview.get_children():#To delete specific row in treeview
                    if self.select_treeview.item(afterrun)["values"] == self.M1_drop_no:
                        self.select_treeview.delete(afterrun)
                self.M1_Sl_no = int
                self.M1_status = "Ready"
        elif self.Internet_status == "Bad" or self.csv_M1_data_waiting == True:     
            self.offline_end_time1= te            
            filename = d + ".csv"
            if os.path.isfile(filename) == True:
                with open(filename, "a") as offlinecfm:
                    offlinecfmWriter = csv.writer(offlinecfm)
                    offlinecfmWriter.writerow([self.offline_token_no1,self.offline_start_time1,self.offline_end_time1,self.offline_Item1,self.offline_weight1,self.offline_Amount1,self.offline_contact_no1,self.offline_discount1,for_date,num_month,])
                offlinecfm.close()
            else:                
                with open(filename, "w") as offlinecfm:
                    offlinecfmWriter = csv.writer(offlinecfm)
                    offlinecfmWriter.writerow(["Token no","YYYY_MM_DD","Start time","End time","Item","Weight","Amount","Contact no","Discount","DD","MM",])
                    offlinecfmWriter.writerow([self.offline_token_no1,et,self.offline_start_time1,self.offline_end_time1,self.offline_Item1,self.offline_weight1,self.offline_Amount1,self.offline_contact_no1,self.offline_discount1,for_date,num_month,])
                offlinecfm.close()
            self.csv_M1_data_waiting =False
            for afterrun in self.select_treeview.get_children():#To delete specific row in treeview
                if self.select_treeview.item(afterrun)["values"] == self.M1_drop_no:
                    self.select_treeview.delete(afterrun)
                self.to_place_inform_display()
                self.info_display.insert(0.0,"info:\n Token no {} completed...!\n Please select next token_no to run".format(self.offline_token_no1),)
                self.M1_Sl_no = int
                self.M1_status = "Ready"

    def update_M2_table(self):
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        te = hour+':'+minute+':'+second
        if self.Internet_status=="Good" and self.csv_M2_data_waiting != True:
            try:
                self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                if self.cat.is_connected():
                    self.datacursor = self.cat.cursor(buffered=True)
                    self.datacursor.execute("UPDATE {today} SET End_time=%s WHERE Token_no=%s".format(today= 'transaction_data'),(te,self.M2_Sl_no,),)
                    self.cat.commit()
                    for afterrun in self.select_treeview.get_children():#To delete specific row in treeview
                        if self.select_treeview.item(afterrun)["values"] == self.M2_drop_no:
                            self.select_treeview.delete(afterrun)
                    self.to_place_inform_display()
                    self.info_display.insert(0.0,"info:\n Token no {} completed...!\n Please select next token_no to run".format(self.M2_Token_no),)
                    self.M2_Sl_no = int
                    self.M2_status = "Ready"
            except mysql.connector.errors.ProgrammingError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812A\n None item is running in F Mc_2")
                error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                hour = time.strftime("%H")
                minute = time.strftime("%M")
                second = time.strftime("%S")
                te = hour+':'+minute+':'+second
                error_logging.write("{} {}, while updating M2 data {}\n".format(et,te,self.all_log))
                error_logging.close()
            except mysql.connector.errors.InterfaceError as erlog:
                self.all_log=erlog
                self.interface_error_handle()
                error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                hour = time.strftime("%H")
                minute = time.strftime("%M")
                second = time.strftime("%S")
                te = hour+':'+minute+':'+second
                error_logging.write("{} {}, while updating M3 data {}\n".format(et,te,self.all_log))
                error_logging.close()
                for afterrun in self.select_treeview.get_children():#To delete specific row in treeview
                    if self.select_treeview.item(afterrun)["values"] == self.M2_drop_no:
                        self.select_treeview.delete(afterrun)
                self.M2_Sl_no = int
                self.M2_status = "Ready"
            except BrokenPipeError as erlog:
                self.all_log=erlog
                self.brokenpipe_error_handle()
                error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                hour = time.strftime("%H")
                minute = time.strftime("%M")
                second = time.strftime("%S")
                te = hour+':'+minute+':'+second
                error_logging.write("{} {}, while updating M2 data {}\n".format(et,te,self.all_log))
                error_logging.close()
        elif self.Internet_status == "Bad" or self.csv_M2_data_waiting == True:
            self.offline_end_time2 = te
            filename = d + ".csv"  # initialising offline data storage
            if os.path.isfile(filename) == True:
                with open(filename, "a") as offlinecfm:
                    offlinecfmWriter = csv.writer(offlinecfm)
                    offlinecfmWriter.writerow([self.offline_token_no2,self.offline_start_time2,self.offline_end_time2,self.offline_Item2,self.offline_weight2,self.offline_Amount2,self.offline_contact_no2,self.offline_discount2,for_date,num_month,])
                offlinecfm.close()
            else:
                with open(filename, "w") as offlinecfm:
                    offlinecfmWriter = csv.writer(offlinecfm)
                    offlinecfmWriter.writerow(["Token no","Start time","End time","Item","Weight","Amount","Contact no","Discount","DD","MM",])
                    offlinecfmWriter.writerow([self.offline_token_no2,self.offline_start_time2,self.offline_end_time2,self.offline_Item2,self.offline_weight2,self.offline_Amount2,self.offline_contact_no2,self.offline_discount2,for_date,num_month,])
                offlinecfm.close()
            self.csv_M2_data_waiting =False
            for afterrun in self.select_treeview.get_children():#To delete specific row in treeview
                if self.select_treeview.item(afterrun)["values"] == self.M2_drop_no:
                    self.select_treeview.delete(afterrun)
                self.to_place_inform_display()
                self.info_display.insert(0.0,"info:\n Token no {} offline process completed...!\n Please select next token_no to run".format(self.offline_token_no2),)
                self.M2_Sl_no = int
                self.M2_status = "Ready"  
        
    def update_M3_table(self):
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        te = hour+':'+minute+':'+second
        if self.Internet_status=="Good" and self.csv_M3_data_waiting != True:
            try:
                self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                if self.cat.is_connected():
                    self.datacursor = self.cat.cursor(buffered=True)
                    self.datacursor.execute("UPDATE {today} SET End_time=%s WHERE Token_no=%s".format(today= 'transaction_data'),(te,self.M3_Sl_no,),)
                    self.cat.commit()
                    for afterrun in self.select_treeview.get_children():#To delete specific row in treeview
                        if self.select_treeview.item(afterrun)["values"] == self.M3_drop_no:
                            self.select_treeview.delete(afterrun)
                    self.to_place_inform_display()
                    self.info_display.insert(0.0,"info:\n Token no {} completed...!\n Please select next token_no to run".format(self.M3_Token_no),)
                    self.M3_Sl_no = int
                    self.M3_status = "Ready"
            except mysql.connector.errors.ProgrammingError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812A\n None item is running in F Mc_3")
                error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                hour = time.strftime("%H")
                minute = time.strftime("%M")
                second = time.strftime("%S")
                te = hour+':'+minute+':'+second
                error_logging.write("{} {}, while updating M3 data {}\n".format(et,te,self.all_log))
                error_logging.close()
            except mysql.connector.errors.InterfaceError as erlog:
                self.all_log=erlog
                self.interface_error_handle()
                error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                hour = time.strftime("%H")
                minute = time.strftime("%M")
                second = time.strftime("%S")
                te = hour+':'+minute+':'+second
                error_logging.write("{} {}, while updating M3 data {}\n".format(et,te,self.all_log))
                error_logging.close()
                for afterrun in self.select_treeview.get_children():#To delete specific row in treeview
                    if self.select_treeview.item(afterrun)["values"] == self.M3_drop_no:
                        self.select_treeview.delete(afterrun)
                self.M3_Sl_no = int
                self.M3_status = "Ready"
            except BrokenPipeError as erlog:
                self.all_log=erlog
                self.brokenpipe_error_handle()
                error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                hour = time.strftime("%H")
                minute = time.strftime("%M")
                second = time.strftime("%S")
                te = hour+':'+minute+':'+second
                error_logging.write("{} {}, while updating M3 data {}\n".format(et,te,self.all_log))
                error_logging.close()
        elif self.Internet_status == "Bad" or self.csv_M3_data_waiting == True:
            self.offline_end_time3 = te
            filename = d + ".csv"
            if os.path.isfile(filename) == True:
                with open(filename, "a") as offlinecfm:
                    offlinecfmWriter = csv.writer(offlinecfm)
                    offlinecfmWriter.writerow([self.offline_token_no3,self.offline_start_time3,self.offline_end_time3,self.offline_Item3,self.offline_weight3,self.offline_Amount3,self.offline_contact_no3,self.offline_discount3,for_date,num_month,])
                offlinecfm.close()
            else:                           
                with open(filename, "w") as offlinecfm:
                    offlinecfmWriter = csv.writer(offlinecfm)
                    offlinecfmWriter.writerow(["Token no","Start time","End time","Item","Weight","Amount","Contact no","Discount","DD","MM",])
                    offlinecfmWriter.writerow(
                        [self.offline_token_no3,self.offline_start_time3,self.offline_end_time3,self.offline_Item3,self.offline_weight3,self.offline_Amount3,for_date,num_month,])
                offlinecfm.close()
            self.csv_M3_data_waiting =False      
            for afterrun in self.select_treeview.get_children():#To delete specific row in treeview
                if self.select_treeview.item(afterrun)["values"] == self.M3_drop_no:
                    self.select_treeview.delete(afterrun)
            self.to_place_inform_display()
            self.info_display.insert(0.0,"info:\n Token no {} offline process completed...!\n Please select next token_no to run".format(self.offline_token_no3),)
            self.M3_Sl_no = int
            self.M3_status = "Ready"
            
    def tally_mysql(self):        
        if self.TDT == False and self.M1_status == "Ready" and self.M2_status == "Ready" and self.M3_status == "Ready":
            self.tally_window = Toplevel(self.root)
            self.tally_window.title("Today's Transaction")
            # self.tally_window.iconbitmap("C:/Users/Subramanya M S/Documents/CFM/process.ico")
            self.tally_window.geometry("525x522")
            self.TDT = True
            tree_total = Frame(self.tally_window, relief=FLAT)
            tree_total.place(x=5, y=5, width=511, height=390)
            self.tally_window.configure(bg="white")
            xscrollbar = Scrollbar(tree_total, orient=HORIZONTAL)
            xscrollbar.pack(side=BOTTOM, fill=X)
            # Vertical (y) Scroll Bar
            yscrollbar = Scrollbar(tree_total)
            yscrollbar.pack(side=RIGHT, fill=Y)
            for_treeview = ttk.Treeview(tree_total,columns=("token_no", "item", "time", "weight", "amount"),xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set,)
            # Configure the scrollbars
            xscrollbar.config(command=for_treeview.xview)
            yscrollbar.config(command=for_treeview.yview)
            for_treeview.heading("token_no", text="Token_no")
            for_treeview.heading("item", text="Item")
            for_treeview.heading("time", text="Time")
            for_treeview.heading("weight", text="Weight")
            for_treeview.heading("amount", text="Amount")
            for_treeview["show"] = "headings"
            for_treeview.column("token_no", width=55, anchor="center")
            for_treeview.column("item", width=50, anchor="center")
            for_treeview.column("time", width=90, anchor="center")
            for_treeview.column("weight", width=60, anchor="center")
            for_treeview.column("amount", width=70, anchor="center")
            for_treeview.pack(fill=BOTH, expand=1)
            monthhrs_label = Label(self.tally_window,text="Mth",font=("Calibri", 10, "bold"),foreground="#d77337",background="white").place(x=127, y=396)
            todayhrs_label = Label(self.tally_window,text="Today",font=("Calibri", 10, "bold"),foreground="#d77337",background="white").place(x=184, y=395)
            M1hrs_label = Label(self.tally_window,text="M1_hrs:",font=("Calibri", 10, "bold"),foreground="dark blue",background="white").place(x=60, y=421)
            M2hrs_label = Label(self.tally_window,text="M2_hrs:",font=("Calibri", 10, "bold"),foreground="dark blue",background="white").place(x=60, y=455)
            M3hrs_label = Label(self.tally_window,text="M3_hrs:",font=("Calibri", 10, "bold"),foreground="dark blue",background="white").place(x=60, y=489)
            self.M1mth_show = Text(master=self.tally_window,height=0.5,width=5,font=("Calibri", 10),foreground="black", background="#FFFFC9",wrap=WORD,)
            self.M1mth_show.tag_configure("center", justify="center")
            self.M1mth_show.place(x=125, y=419)
            self.M1today_show = Text(master=self.tally_window,height=1,width=5,font=("Calibri", 10),foreground="black", background="#FFFFC9",wrap=WORD,)
            self.M1today_show.tag_configure("center", justify="center")
            self.M1today_show.place(x=183, y=419)
            self.M2mth_show = Text(master=self.tally_window,height=1,width=5,font=("Calibri", 10),foreground="black", background="#FFFFC9",wrap=WORD,)
            self.M2mth_show.tag_configure("center", justify="center")
            self.M2mth_show.place(x=125, y=454)
            self.M2today_show = Text(master=self.tally_window,height=1,width=5,font=("Calibri", 10),foreground="black", background="#FFFFC9",wrap=WORD,)
            self.M2today_show.tag_configure("center", justify="center")
            self.M2today_show.place(x=183, y=454)
            self.M3mth_show = Text(master=self.tally_window,height=1,width=5,font=("Calibri", 10),foreground="black", background="#FFFFC9",wrap=WORD,)
            self.M3mth_show.tag_configure("center", justify="center")
            self.M3mth_show.place(x=125, y=488)
            self.M3today_show = Text(master=self.tally_window,height=1,width=5,font=("Calibri", 10),foreground="black", background="#FFFFC9",wrap=WORD,)
            self.M3today_show.tag_configure("center", justify="center")
            self.M3today_show.place(x=183, y=488)
            M1temptoday = 0.0  # temporary variable
            M2temptoday = 0.0  # temporary variable
            M3temptoday = 0.0  # temporary variable
            self.M1timetoday = 0.0
            self.M2timetoday = 0.0
            self.M3timetoday = 0.0
            self.M1timemonth = 0.0
            self.M2timemonth = 0.0
            self.M3timemonth = 0.0
            Total_label = Label(self.tally_window,text="Total:",font=("Calibri", 12),foreground="dark blue",background="white").place(x=350, y=403)
            End_of_day_btn = Button(self.tally_window,command=self.update_time_to_month,cursor="hand2",text="End_of_Day",background="#d77337",activebackground = "#d77337",
                bd=0,highlightthickness=0,foreground="white",font=("calibri", 10, "bold"),relief=FLAT,)
            End_of_day_btn.place(bordermode=OUTSIDE,x=398, y=450, width=80)
            Total_show = Text(master=self.tally_window,height=1,width=7,font=("Calibri", 16),foreground="black", background="#FFFFC9",wrap=WORD,)
            Total_show.tag_configure("center", justify="center")
            Total_show.place(x=397, y=400)
            self.tally_window.protocol("WM_DELETE_WINDOW", self.on_TDT_close_icon)
            try:
                self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                if self.cat.is_connected():
                    self.datacursor = self.cat.cursor(buffered=True)
                    self.datacursor.execute("SELECT * FROM {today} where YYYY_MM_DD=%s".format(today= 'transaction_data'),(et,))
                    cpt = 0
                    for row in self.datacursor:
                        for_treeview.insert("", "end", values=(row[1], row[5], row[3], row[6], row[7]))
                        cpt += 1                    
                    self.datacursor.execute("SELECT * FROM {today} where YYYY_MM_DD=%s".format(today= 'transaction_data'),(et,))
                    ches = self.datacursor.fetchall() # temporary tuple
                    for pow in ches:
                        if pow[5] == self.Rice_data:
                            temp_ricetime = self.Rice_time / 1000
                            M1temptoday = M1temptoday + pow[6]
                            self.M1timetoday = (M1temptoday * temp_ricetime) / 3600
                            M1temptoday = 0.0
                        if pow[5] == self.Wheat_data:
                            temp_wheattime = self.Wheat_time / 1000
                            M1temptoday = M1temptoday + pow[6]
                            M1temptoday = (M1temptoday * temp_wheattime) / 3600
                            self.M1timetoday = self.M1timetoday + M1temptoday
                            M1temptoday = 0.0
                        if pow[5] == self.Chickpea_data:
                            temp_chickpeatime = self.Chickpea_time / 1000
                            M1temptoday = M1temptoday + pow[6]
                            M1temptoday = (M1temptoday * temp_chickpeatime) / 3600
                            self.M1timetoday = self.M1timetoday + M1temptoday
                            M1temptoday = 0.0
                        if pow[5] == self.Ragi_data:
                            temp_ragitime = self.Ragi_time / 1000
                            M2temptoday = M2temptoday + pow[6]
                            M2temptoday = (M2temptoday * temp_ragitime) / 3600
                            self.M2timetoday = self.M2timetoday + M2temptoday
                            M2temptoday = 0.0
                        if pow[5] == self.Chilli_data:
                            temp_chillitime = self.Chilli_time / 1000
                            M3temptoday = M3temptoday + pow[6]
                            M3temptoday = (M3temptoday * temp_chillitime) / 3600
                            self.M3timetoday = self.M3timetoday + M3temptoday
                            M3temptoday = 0.0
                        if pow[5] == self.Dhaniya_data:
                            temp_dhaniyatime = self.Dhaniya_time /1000
                            M3temptoday = M3temptoday + pow[6]
                            M3temptoday = (M3temptoday * temp_dhaniyatime) / 3600
                            self.M3timetoday = self.M3timetoday + M3temptoday
                            M3temptoday = 0.0
                    self.M1today_show.insert(0.0, self.M1timetoday)
                    self.M2today_show.insert(0.0, self.M2timetoday)
                    self.M3today_show.insert(0.0, self.M3timetoday)
                    self.datacursor.execute("SELECT * FROM machine_timelog_2021 where Sl_no=%s" % (ct))
                    self.thes = (self.datacursor.fetchall())  # temporary variable to save fetched data
                    self.Mmthhrs = self.thes[0]
                    if self.Mmthhrs[2] == None:
                        self.M1mth_show.insert(0.0, 0.0)
                    else:
                        self.M1mth_show.insert(0.0, self.Mmthhrs[2])

                    if self.Mmthhrs[3] == None:
                        self.M2mth_show.insert(0.0, 0.0)
                    else:
                        self.M2mth_show.insert(0.0, self.Mmthhrs[3])

                    if self.Mmthhrs[4] == None:
                        self.M3mth_show.insert(0.0, 0.0)
                    else:
                        self.M3mth_show.insert(0.0, self.Mmthhrs[4])
                    
                    self.datacursor.execute("SELECT SUM(Amount) AS totalsum FROM {today} where YYYY_MM_DD=%s".format(today= 'transaction_data'),(et,))
                    res = self.datacursor.fetchall()  # temporary variable to save fetched data
                    try:
                        for i in res:
                            rus = i[0]
                            Total_show.insert(0.0, rus)
                    except:
                        pass                    
            except mysql.connector.errors.InterfaceError as erlog:
                self.all_log=erlog
                self.interface_error_handle()
            except mysql.connector.errors.OperationalError as erlog:
                self.all_log=erlog
                self.error_func()
                self.error_display.insert(0.0, "Error: 1812D\n %s"%(self.all_log))
                self.writing_log()
        else:
            self.error_func()
            self.error_display.insert(0.0, "Error:\n Check whether TDT window is already opened or else wait untill all machines become idle...!")
            
    def update_time_to_month(self):
        if self.M1_status == "Ready" and self.M2_status == "Ready" and self.M3_status == "Ready":
            wholeupdate = messagebox.askyesno("Closing Mill", "Are you sure want to close Mill for the day?")
            if (wholeupdate > 0 and (self.M1timetoday != 0.0 or self.M2timetoday != 0.0 or self.M3timetoday != 0.0)):
                filename = d + ".csv"
                if os.path.isfile(filename) == True:
                    self.offline_csv_handling()
                taty = []
                taty = list(self.Mmthhrs)
                if self.Mmthhrs[2] == None:
                    taty[2] = 0.0
                pt = taty[2] + self.M1timetoday  # variable to add day time into month
                if self.Mmthhrs[3] == None:
                    taty[3] = 0.0
                kt = taty[3] + self.M2timetoday  # variable to add day time into month
                if self.Mmthhrs[4] == None:
                    taty[4] = 0.0
                tt = taty[4] + self.M3timetoday  # variable to add day time into month
                self.datacursor.execute("update machine_timelog_2021 set M1_hrs=%s,M2_hrs=%s,M3_hrs=%s where Sl_no=%s"% (pt, kt, tt, ct))
                self.cat.commit()
                self.datacursor.execute("SELECT * FROM machine_timelog_2021 where Sl_no=%s" % (ct))
                self.thes = (self.datacursor.fetchall())  # temporary variable to save fetched data
                self.Mmthhrs = self.thes[0]
                self.M1mth_show.insert(0.0, self.Mmthhrs[2])
                self.M2mth_show.insert(0.0, self.Mmthhrs[3])
                self.M3mth_show.insert(0.0, self.Mmthhrs[4])
                self.M1timetoday = 0.0
                self.M2timetoday = 0.0
                self.M3timetoday = 0.0
                self.M1today_show.insert(0.0, self.M1timetoday)
                self.M2today_show.insert(0.0, self.M2timetoday)
                self.M3today_show.insert(0.0, self.M3timetoday)

    def closing_mysql(self):
        self.datacursor.close()
        self.cat.close()

    def TPD_retrive(self):  # loading all parameter into settings window display
        sqt = "SELECT * from price_list"
        try:
            self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
            self.datacursor = self.cat.cursor(buffered=True)
            self.datacursor.execute(sqt)
            jdata = self.datacursor.fetchmany(1)
            for row in jdata:
                self.Chickpea_entry.insert(0, row[2])
                self.Chickpea_disc_entry.insert(0, row[3])
                self.Chickpea_price_entry.insert(0, row[4])
                self.Chickpea_disc_value_entry.insert(0, row[5])
                self.Chickpea_max_disc_limit.insert(0,row[6])
            jdata = self.datacursor.fetchmany(1)
            for row in jdata:
                self.Rice_entry.insert(0, row[2])
                self.Rice_disc_entry.insert(0, row[3])
                self.Rice_price_entry.insert(0, row[4])
                self.Rice_disc_value_entry.insert(0, row[5])
                self.Rice_max_disc_limit.insert(0,row[6])
            jdata = self.datacursor.fetchmany(1)
            for row in jdata:
                self.Wheat_entry.insert(0, row[2])
                self.Wheat_disc_entry.insert(0, row[3])
                self.Wheat_price_entry.insert(0, row[4])
                self.Wheat_disc_value_entry.insert(0, row[5])
                self.Wheat_max_disc_limit.insert(0,row[6])
            jdata = self.datacursor.fetchmany(1)
            for row in jdata:
                self.Ragi_entry.insert(0, row[2])
                self.Ragi_disc_entry.insert(0, row[3])
                self.Ragi_price_entry.insert(0, row[4])
                self.Ragi_disc_value_entry.insert(0, row[5])
                self.Ragi_max_disc_limit.insert(0,row[6])
            jdata = self.datacursor.fetchmany(1)
            for row in jdata:
                self.Chilli_entry.insert(0, row[2])
                self.Chilli_disc_entry.insert(0, row[3])
                self.Chilli_price_entry.insert(0, row[4])
                self.Chilli_disc_value_entry.insert(0, row[5])
                self.Chilli_max_disc_limit.insert(0,row[6])
            jdata = self.datacursor.fetchmany(1)
            for row in jdata:
                self.Dhaniya_entry.insert(0, row[2])
                self.Dhaniya_disc_entry.insert(0, row[3])
                self.Dhaniya_price_entry.insert(0, row[4])
                self.Dhaniya_disc_value_entry.insert(0, row[5])
                self.Dhaniya_max_disc_limit.insert(0,row[6])
        except mysql.connector.errors.InterfaceError as erlog:
            self.all_log=erlog
            self.interface_error_handle()
        except BrokenPipeError as erlog:
            self.all_log=erlog
            self.brokenpipe_error_handle()
            error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
            hour = time.strftime("%H")
            minute = time.strftime("%M")
            second = time.strftime("%S")
            te = hour+':'+minute+':'+second
            error_logging.write("{} {}, While loading all parameter into settings window {}\n".format(et,te,self.all_log))
            error_logging.close()

    def saving_user(self):
        self.new_user = self.adduser_uname.get()
        self.new_user_pass = self.adduser_pass.get()
        self.re_enter_user_pass = self.re_enter_pass.get()
        entered_pass_add = (self.re_enter_user_pass)  # To add password inside the single quotes(else Mysql will not accept)
        if self.new_user != "" and self.new_user_pass == self.re_enter_user_pass:
            chat = "INSERT INTO user_details VALUES (NULL,%s,%s)"
            phat = (self.new_user,entered_pass_add,)
            try:
                self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                self.datacursor = self.cat.cursor(buffered=True)
                self.datacursor.execute(chat, phat)
                self.cat.commit()
                self.adduser_uname.delete(0, END)
                self.adduser_pass.delete(0, END)
                self.re_enter_pass.delete(0, END)
            except mysql.connector.errors.InterfaceError as erlog:
                self.all_log=erlog
                self.interface_error_handle()
            except mysql.connector.errors.ProgrammingError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812A\n Codding error, Please evalute the script once...!")
            except mysql.connector.errors.IntegrityError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0,"Error: 1812I\n Entered Password is not accepted by Database, Please try some other password...!",)
                error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                hour = time.strftime("%H")
                minute = time.strftime("%M")
                second = time.strftime("%S")
                te = hour+':'+minute+':'+second
                error_logging.write("{} {}, Error code: 1812B, This exception is raised when the foreign key constraint fails.\n".format(et,te))
                error_logging.close()
        elif (self.new_user == "" or self.new_user_pass == "" or self.re_enter_user_pass == ""):
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error: 1201B\n All fields are manditory...!")
        else:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error: 1201M\n Password not matching...!")

    def find_ip(self):
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        self.inform_func()
        self.info_display.insert(0.0, "info:\nComputer Name: {}\nCurrent IP Address: {}".format(hostname,IPAddr))

    def login_function(self):
        try:
            self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
            if self.cat.is_connected():
                self.datacursor = self.cat.cursor(buffered=True)
                self.datacursor.execute("select Sl_no from user_details ORDER BY Sl_no DESC LIMIT 1")
                sl_count = self.datacursor.fetchone()
                self.datacursor.execute("SELECT User_name,User_pass FROM user_details")
                for_passbox = self.datacursor.fetchall()
                final_error = ""
                loginmatched = False
                self.user_entered_name = self.txt_user.get()
                self.user_entered_pass = (self.txt_pass.get())
                for checkinto in for_passbox:
                    if (self.user_entered_name == checkinto[0] and self.user_entered_pass == checkinto[1]):
                        self.uname = self.user_entered_name
                        self.Uname = "Welcome " + self.uname
                        final_error = ""
                        loginmatched = True
                        self.con_mysql()
                        if self.cat.is_connected():
                            self.Frame_login.destroy()
                            error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                            hour = time.strftime("%H")
                            minute = time.strftime("%M")
                            second = time.strftime("%S")
                            te = hour+':'+minute+':'+second
                            error_logging.write("{} {}, {} logged in successfully...!\n".format(et,te,self.user_entered_name))
                            error_logging.close()
                        break
                    elif (self.user_entered_name == "" or self.user_entered_pass == "" or self.user_entered_pass == "Password" or self.user_entered_name == "User name"):
                        self.empty_pass_error()
                    elif (self.user_entered_pass != checkinto[1] and self.user_entered_name != checkinto[0]):
                        final_error = "invalid"

                if loginmatched == False and final_error == "invalid":
                    self.to_place_error_display()
                    self.error_display.insert(0.0, "Error: 1201A\n Invalid user name/Password...!")
                    self.txt_pass.delete(0, END)
                    self.to_analyse_issue()
                    error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                    hour = time.strftime("%H")
                    minute = time.strftime("%M")
                    second = time.strftime("%S")
                    te = hour+':'+minute+':'+second
                    error_logging.write("{} {}, User attempted with invalid credentials using User name:{}, Password:{}\n".format(et,te,self.user_entered_name,self.user_entered_pass))
                    error_logging.close()
            else:
                self.error_func()
                self.error_display.insert(0.0, "Error:\n Connecting Database failed...!")
        except mysql.connector.errors.InterfaceError as erlog:
            self.all_log=erlog
            self.to_place_error_display()
            self.error_display.insert(0.0,"Error: 1812B\n Unable to communicate with Database...!\nCheck Server status & its Hostname ")
            error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
            hour = time.strftime("%H")
            minute = time.strftime("%M")
            second = time.strftime("%S")
            te = hour+':'+minute+':'+second
            error_logging.write("{} {},During user login validation, failed to connect database(Interface Error)".format(et,te))
            error_logging.close()

    def IP_validation(self):
        self.comp1_ip = self.ip_enter.get()
        self.comp2_ip = self.ip_re_enter.get()
        if self.comp1_ip == "" or self.comp2_ip == "":
            self.empty_pass_error()
        elif self.comp1_ip != self.comp2_ip:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error: 1201D\n Please Enter same IP Address in both the fields...!")
        else:
            # regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
            # if re.search(regex, self.comp1_ip):
            self.to_write_IP()
            self.ip_enter.delete(0, END)
            self.ip_re_enter.delete(0, END)
            try:
                self.to_read_IP()
                self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                self.datacursor = self.cat.cursor(buffered=True)
                self.to_place_inform_display()
                self.info_display.insert(0.0,"info:\n Successfully updated {} (server Address)...!\nCan continue further...".format(self.comp1_ip),)
            except mysql.connector.errors.InterfaceError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0,"Error: 1812B\n Updated the Hostname & tried to ping server\nBut {} is not matching with Server Address...!".format(self.comp1_ip),)
                self.ip_enter.delete(0, END)
                self.ip_re_enter.delete(0, END)

    def cancel_admin_frame(self):
        if self.Settings_Frame == True:
            self.admin_window.destroy()
            self.Settings_Frame = False
        if self.Manual_Frame == True:
            self.Manual_Frame_window.destroy()
            self.Manual_Frame = False
        if self.input_output_Frame == True:
            self.input_output_window.destroy()
            self.input_output_Frame = False
        if self.IP_admin_Frame_login == True:
            self.Frame_admin_window.destroy()
            self.IP_admin_Frame_login = False
        if self.adding_frame == True:
            self.Frame_adduser_window.destroy()
            self.adding_frame = False
        if self.removeuser_frame == True:
            self.Frame_removeuser_window.destroy()
            self.removeuser_frame = False
        if self.changingpswd_frame == True:
            self.Frame_changepswd_window.destroy()
            self.changingpswd_frame = False
        if self.IP_Frame == True:
            self.IP_entry_Frame_window.destroy()
            self.IP_Frame = False
        if self.tool_frame == True:
            self.Frame_Tool_window.destroy()
            self.tool_frame =False

    def admin_name_locating(self):
        if self.txt_admin.winfo_exists() == True:
            self.admin_entered_name = self.txt_admin.get()
            self.txt_admin.destroy()
            self.admin_name_place = Label(self.Frame_admin_window,text=self.admin_entered_name,font=("Calibri", 16),background="white",foreground="black",).place(x=45, y=60)

    def user_name_locating(self):
        if self.changepswd_user.winfo_exists() == True:
            self.for_pass_change = self.changepswd_user.get()
            self.changepswd_user.destroy()
            self.changepswd_user_name_place = Label(self.Frame_changepswd_window,text= self.for_pass_change,font=("Calibri", 16),background="white",foreground="black",).place(x=35, y=50)

    def admin_validation(self):
        if self.IP_admin_Frame_login != True or self.IP_admin_Frame_login == None:
            admin_final_error = ""
            adminloginmatched = False
            try:
                self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                self.datacursor = self.cat.cursor(buffered=True)
                self.datacursor.execute("SELECT User_name,User_pass FROM user_details")
                for_passbox = self.datacursor.fetchall()
                
                self.admin_entered_pass = self.admin_pass.get()
                for checkinto in for_passbox:
                    if (self.admin_entered_name == checkinto[0] and self.admin_entered_pass == checkinto[1]):
                        admin_final_error = ""
                        adminloginmatched = True
                        try:
                            if self.admin_error_display.winfo_exists() == True:
                                self.admin_error_display.destroy()
                        except:
                            pass
                        if self.Settings_Frame == True:
                            self.settings_fun()
                            self.to_place_inform_display()
                            self.info_display.insert(0.0, "info:\n Admin logged in successfully...!")
                            self.Settings_Frame = False                        
                        break
                    elif (self.admin_entered_name == "" or self.admin_entered_name == "Admin" or self.admin_entered_pass == "" or self.admin_entered_pass == "Password"):
                        self.empty_pass_error()
                    elif (self.admin_entered_pass != checkinto[1]
                        and self.admin_entered_name != checkinto[0]):
                        admin_final_error = "invalid"
            except mysql.connector.errors.InterfaceError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0,"Error: 1812B\n Unable to connect Database...!\nCheck Server IPaddress...!\nCheck Network connectivity...!",)
        elif self.IP_admin_Frame_login == True:
            self.admin_entered_name = self.txt_admin.get()
            self.admin_entered_pass = self.admin_pass.get()
            admin_final_error = ""
            adminloginmatched = False
            for verifyname, verifypass in self.Address.items():
                if (verifypass == self.admin_entered_pass and verifyname == self.admin_entered_name):
                    admin_final_error = ""
                    adminloginmatched = True
                    self.IP_entry_Frame()
                    self.IP_admin_Frame_login = False
                elif (self.admin_entered_name == "" or self.admin_entered_name == "Admin" or self.admin_entered_pass == "" or self.admin_entered_pass == "Password"):
                    self.empty_pass_error()
                elif (self.admin_entered_pass != verifypass and self.admin_entered_name != verifyname):
                    admin_final_error = "invalid"

        if adminloginmatched == False and admin_final_error == "invalid":
            if self.info_display.winfo_exists() == True:
                self.info_display.destroy()
                self.admin_error_func()
            elif self.error_display.winfo_exists() == True:
                self.error_display.destroy()
                self.admin_error_func()
            elif self.admin_error_display.winfo_exists() == True:
                self.admin_error_display.delete(0.0, END)                
            else:
                self.admin_error_func()
            self.admin_error_display.insert(0.0, "Error: 1201F\n Invalid Admin name/Password...!")
            error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
            hour = time.strftime("%H")
            minute = time.strftime("%M")
            second = time.strftime("%S")
            te = hour+':'+minute+':'+second
            error_logging.write(
                    "{} {}, Admin attempted with invalid credentials using Admin name:{}, Password:{}\n".format(et,te,self.admin_entered_name,self.admin_entered_pass))
            error_logging.close()
            self.admin_pass.delete(0, END)

    def drop_selected(self):
        try:
            x = self.select_treeview.selection()[0]
            self.select_treeview.delete(x)
        except IndexError as erlog:
            self.all_log=erlog
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error: 1201N\n None Token_no selected to delete")

    def set_torun_window(self):        
        try:
            if self.pgm_opened==True:#To validate 
                self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                if self.cat.is_connected():
                    self.datacursor = self.cat.cursor(buffered=True)
                    self.datacursor.execute("select YYYY_MM_DD from {today} order by YYYY_MM_DD DESC LIMIT 1".format(today= 'transaction_data'))
                    self.newtoken=  self.datacursor.fetchone()
                    if self.newtoken!=None:
                        self.newtoken=str(self.newtoken[0])
            if (self.selection == None and self.select_window.winfo_exists() == True):  # to check selection window exists or not?
                if self.common_item != "" and self.Amount != float:
                    if self.pgm_opened == True:                    
                        try:
                            self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                            self.datacursor = self.cat.cursor(buffered=True)
                            if self.cat.is_connected():
                                self.datacursor.execute("select * from {today} ORDER BY Sl_no DESC LIMIT 1".format(today= 'transaction_data'))
                                self.dq= self.datacursor.fetchone()
                            if self.newtoken==et:#Comparing last token date with today's date
                                if self.dq== None and self.select_treeview.get_children()!= ():  # validation to define first token no
                                    self.tokenno = 1
                                elif self.dq ==None:
                                    self.tokenno = 1
                                else:
                                    self.tokenno = self.dq[1]
                                    self.tokenno += 1
                            elif self.tokenno != None:
                                self.tokenno = self.no_internet_token
                            else:
                                self.tokenno =1
                            self.pgm_opened = False
                            self.select_treeview.insert("","end",iid=self.tokenno,
                                values=(self.tokenno,self.common_item,self.Machine_name,"Pending..",self.weight,self.discount,self.Amount,self.contact_number,),)
                            self.common_item = ""
                            self.Amount = float
                            self.to_place_inform_display()
                            self.info_display.insert(0.0, "info:\n Select Token_no and click 'RUN' button")
                            self.Item_display.delete(0.0, END)
                            self.Dis_display.delete(0.0,END)
                            self.Price_display.delete(0.0,END)
                            self.AM_display.delete(0.0,END)
                        except mysql.connector.errors.InterfaceError as erlog:
                            self.all_log=erlog
                            self.interface_error_handle()
                        except mysql.connector.errors.OperationalError as erlog:
                            self.all_log=erlog
                            self.error_func()
                            self.error_display.insert(0.0, "Error: 1812D\n %s"%(self.all_log))
                            self.writing_log()
                    else:
                        self.tokenno += 1
                        self.select_treeview.insert("","end",iid=self.tokenno,values=(self.tokenno,self.common_item,self.Machine_name,"Pending..",self.weight,self.discount,self.Amount,self.contact_number,),)
                        self.common_item = ""
                        self.Amount = float
                        self.to_place_inform_display()
                        self.info_display.insert(0.0, "info:\n Select Token_no and click 'RUN' button")
                        self.Item_display.delete(0.0, END)
                        self.Dis_display.delete(0.0,END)
                        self.Price_display.delete(0.0,END)
                        self.AM_display.delete(0.0,END)

                else:
                    self.to_place_error_display()
                    self.error_display.insert(0.0, "Error: 1201P\n None Item selected\weighed...!")
            else:
                self.select_to_run()
                if self.common_item != "" and self.Amount != float:
                    if self.pgm_opened == True:                        
                        try:
                            self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                            if self.cat.is_connected():
                                self.datacursor = self.cat.cursor(buffered=True)
                                self.datacursor.execute("select * from {today} ORDER BY Sl_no DESC LIMIT 1".format(today= 'transaction_data'))
                                self.dq= self.datacursor.fetchone()
                                if self.newtoken==et:#Comparing last token date with today's date
                                    if self.dq== None and self.select_treeview.get_children()!= ():  # validation to define first token no
                                        self.tokenno = 1
                                    elif self.dq == None:
                                        self.tokenno = 1                          
                                    else:
                                        self.tokenno = self.dq[1]
                                        self.tokenno += 1
                                elif self.tokenno != None:
                                    self.tokenno = self.no_internet_token
                                else:
                                    self.tokenno =1
                                    self.pgm_opened = False
                                self.pgm_opened = False
                        except mysql.connector.errors.InterfaceError as erlog:
                            self.all_log=erlog
                            self.interface_error_handle()
                        except mysql.connector.errors.OperationalError as erlog:
                            self.all_log=erlog
                            self.error_func()
                            self.error_display.insert(0.0, "Error: 1812D\n %s"%(self.all_log))
                            self.writing_log()
                        self.select_treeview.insert("","end",iid=self.tokenno,
                            values=(self.tokenno,self.common_item,self.Machine_name,"Pending..",self.weight,self.discount,self.Amount,self.contact_number,),)
                        self.common_item = ""
                        self.Amount = float
                        self.to_place_inform_display()
                        self.info_display.insert(0.0, "info:\n Select Token and click 'RUN' button")
                        self.Item_display.delete(0.0, END)
                        self.Dis_display.delete(0.0,END)
                        self.Price_display.delete(0.0,END)
                        self.AM_display.delete(0.0,END)
                    else:
                        self.tokenno += 1
                        self.select_treeview.insert("","end",iid=self.tokenno,
                            values=(self.tokenno,self.common_item,self.Machine_name,"Pending..",self.weight,self.discount,self.Amount,self.contact_number,),)
                        self.common_item = ""
                        self.Amount = float
                        self.to_place_inform_display()
                        self.info_display.insert(0.0, "info:\n Select Token and click 'RUN' button")
                        self.Item_display.delete(0.0, END)
                        self.Dis_display.delete(0.0,END)
                        self.Price_display.delete(0.0,END)
                        self.AM_display.delete(0.0,END)
                else:
                    self.to_place_error_display()
                    self.error_display.insert(0.0, "Error: 1201P\n None Item is selected/weighed...!")
        except mysql.connector.errors.InterfaceError as erlog:
            self.all_log=erlog
            self.interface_error_handle()
            if self.tokenno == None and self.pgm_opened ==True:
                if self.newtoken==et:#Comparing last token date with today's date
                    if self.dq== None and self.select_treeview.get_children()!= ():  # validation to define first token no
                        self.tokenno = 1
                    elif self.dq == None:
                        self.tokenno = 1
                    else:
                        self.tokenno = self.dq[1]
                        self.tokenno += 1
                    self.no_internet_token = self.tokenno
                else:
                    self.tokenno = 1
                    self.no_internet_token = self.tokenno
                self.pgm_opened = False
            elif self.no_internet_token != 1 :
                self.no_internet_token += 1
                self.tokenno = self.no_internet_token
            self.select_treeview.insert("","end",iid=self.no_internet_token,values=(self.no_internet_token,self.common_item,self.Machine_name,"Pending..",self.weight,self.discount,self.Amount,self.contact_number,),)
            self.common_item = ""
            self.Amount = float
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error: Token generated in offline mode...!")
            self.Item_display.delete(0.0, END)
            self.Dis_display.delete(0.0,END)
            self.Price_display.delete(0.0,END)
            self.AM_display.delete(0.0,END)
            
        except mysql.connector.errors.OperationalError as erlog:
            self.all_log=erlog
            self.error_func()
            self.error_display.insert(0.0, "Error: 1812D\n %s"%(self.all_log))
            self.writing_log()

    def parallel_rice_fun(self,event): #When respective Function key is pressed this block will execute
        self.rice_fun()
    
    def parallel_wheat_fun(self,event): #When respective Function key is pressed this block will execute
        self.wheat_fun()
    
    def parallel_chickpea_fun(self,event): #When respective Function key is pressed this block will execute
        self.chickpea_fun()
    
    def parallel_ragi_fun(self,event): #When respective Function key is pressed this block will execute
        self.ragi_fun()
    
    def parallel_chilli_fun(self,event): #When respective Function key is pressed this block will execute
        self.chilli_fun()
    
    def parallel_dhaniya_fun(self,event): #When respective Function key is pressed this block will execute
        self.dhaniya_fun()
    
    def parallel_set_torun_window(self,event):
        self.set_torun_window()

    def parallel_contact_entry_fun(self,event):
        self.contact_entry_fun()
        
    def parallel_trig_rasp_out(self,event):
        self.trig_rasp_out()

    def main_login_click(self, event):
        self.txt_pass.config(state=NORMAL)
        self.txt_pass.delete(0, END)

    def adduser_pass_click(self, event):
        self.adduser_pass.config(state=NORMAL)
        self.adduser_pass.delete(0, END)

    def re_enter_pass_click(self, event):
        self.re_enter_pass.config(state=NORMAL)
        self.re_enter_pass.delete(0, END)

    def IP_entry_click(self, event):
        self.ip_enter.config(state=NORMAL)
        self.ip_enter.delete(0, END)

    def IP_re_entry_click(self, event):
        self.ip_re_enter.config(state=NORMAL)
        self.ip_re_enter.delete(0, END)

    def admin_login_click(self, event):
        self.admin_pass.config(state=NORMAL)
        self.admin_pass.delete(0, END)
        self.admin_name_locating()

    def new_pass_click(self, event):
        self.new_pass.config(state=NORMAL)
        self.new_pass.delete(0, END)
        self.user_name_locating()

    def re_new_pass_click(self, event):
        self.re_new_pass.config(state=NORMAL)
        self.re_new_pass.delete(0, END)
        self.user_name_locating()

    def contact_num_no(self):
        self.contact_number="Null"
        self.number_Frame = False
        self.set_torun_window()
        self.contact_window.destroy()
        self.select_window.lift() # To bring selection window front
    
    def contact_num_yes(self):
        contact_number=self.contact_entry.get()
        if(len(contact_number)==10 and contact_number.isdigit()):
            output = re.findall(r"^[6789]\d{9}$",contact_number)            
            if(len(output)==1):
                self.contact_number=contact_number
                self.contact_window.destroy()
                self.number_Frame = False
                self.set_torun_window()
                self.select_window.lift()# To bring selection window front
            else:
                self.contact_num_error_handle()
                self.contact_entry.delete(0,END)
        else:
            self.contact_num_error_handle()
            self.contact_entry.delete(0,END)

    def weight_comparision(self):
        if self.weight <= 10 and self.weighing_tool == "10Kg":
            self.Process = "Continue"
        elif self.weight >= 10 and self.weight < 25 and self.weighing_tool == "10Kg+":
            self.Process = "Continue"
        elif self.weight >= 25 and self.weighing_tool == "25Kg+":
            self.Process = "Continue"
        elif self.weighing_tool == "No Tool":
            self.Process = "Continue"
        else:
            self.Process = ""
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error:\n Weighing Tool: %s\n Measured Weight: %s\n Please select appropriate tool...!"%(self.weighing_tool,self.weight))
            
    def rice_fun(self):
        self.weight_comparision()
        if self.weighing_tool != "Select_Tool" and self.Process == "Continue":            
            self.Rice_var = True
            self.Item_display.delete(0.0, END)
            self.Item_display.insert("1.0", "RICE")
            self.Item_display.tag_add("center", "1.0", "end")
            self.common_item = self.Rice_data
            self.Machine_name = "F Mc_1"
            if self.weight >= self.Rice_disc_after__kg:
                self.temp_disc=self.weight*self.Rice_disc_value
                if self.temp_disc >= self.Rice_max_disc:
                    self.temp_disc = self.Rice_max_disc
            self.Amount = (self.Rice_price * self.weight)-self.temp_disc
            if self.temp_disc != 0:
                self.temp_disc= int(self.temp_disc)#"%.2f" % round(self.temp_disc, 0)
                self.discount= self.temp_disc
            self.Amount = "%.2f" % round(self.Amount, 2)
            self.Price_display.delete(0.0, END)
            self.Price_display.insert("1.0",self.Rice_price)
            self.Price_display.tag_add("center", "1.0", "end")
            self.Dis_display.delete(0.0, END)
            self.Dis_display.insert("1.0",self.temp_disc)
            self.Dis_display.tag_add("center", "1.0", "end")
            self.AM_display.delete(0.0, END)
            self.AM_display.insert("1.0",self.Amount)
            self.AM_display.tag_add("center", "1.0", "end")
            self.Set.focus_set()
            self.temp_disc= 0
        else:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error:\n Proper Weighing tool not selected...!\n Please click 'Select_Tool' button")
        
    def wheat_fun(self):
        self.weight_comparision()
        if self.weighing_tool != "Select_Tool" and self.Process == "Continue":
            self.Wheat_var = True
            self.Item_display.delete(0.0, END)
            self.Item_display.insert("1.0", "WHEAT")
            self.Item_display.tag_add("center", "1.0", "end")
            self.common_item = self.Wheat_data
            self.Machine_name = "F Mc_1"
            if self.weight >= self.Wheat_disc_after__kg:
                self.temp_disc=self.weight*self.Wheat_disc_value
                if self.temp_disc >= self.Wheat_max_disc:
                    self.temp_disc = self.Wheat_max_disc        
            self.Amount = (self.Wheat_price * self.weight)-self.temp_disc
            if self.temp_disc != 0:
                self.temp_disc= int(self.temp_disc)#"%.2f" % round(self.temp_disc, 0)
                self.discount= self.temp_disc
            self.Amount = "%.2f" % round(self.Amount, 2)
            self.Price_display.delete(0.0, END)
            self.Price_display.insert("1.0",self.Wheat_price)
            self.Price_display.tag_add("center", "1.0", "end")
            self.Dis_display.delete(0.0, END)
            self.Dis_display.insert("1.0",self.temp_disc)
            self.Dis_display.tag_add("center", "1.0", "end")
            self.AM_display.delete(0.0, END)
            self.AM_display.insert("1.0",self.Amount)
            self.AM_display.tag_add("center", "1.0", "end")
            self.Set.focus_set()
            self.temp_disc= 0
        else:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error:\n Proper Weighing tool not selected...!\n Please click 'Select_Tool' button")
        
    def chickpea_fun(self):
        self.weight_comparision()
        if self.weighing_tool != "Select_Tool" and self.Process == "Continue":
            self.Chickpea_var = True
            self.Item_display.delete(0.0, END)
            self.Item_display.insert("1.0", "CHICKPEA")
            self.Item_display.tag_add("center", "1.0", "end")
            self.common_item = self.Chickpea_data
            self.Machine_name = "F Mc_1"
            if self.weight >= self.Chickpea_disc_after__kg:
                self.temp_disc=self.weight*self.Chickpea_disc_value
                if self.temp_disc >= self.Chickpea_max_disc:
                    self.temp_disc = self.Chickpea_max_disc
            self.Amount = (self.Chickpea_price * self.weight)-self.temp_disc
            if self.temp_disc != 0:
                self.temp_disc= int(self.temp_disc)#"%.2f" % round(self.temp_disc, 0)
                self.discount= self.temp_disc
            self.Amount = "%.2f" % round(self.Amount, 2)
            self.Price_display.delete(0.0, END)
            self.Price_display.insert("1.0",self.Chickpea_price)
            self.Price_display.tag_add("center", "1.0", "end")
            self.Dis_display.delete(0.0, END)
            self.Dis_display.insert("1.0",self.temp_disc)
            self.Dis_display.tag_add("center", "1.0", "end")
            self.AM_display.delete(0.0, END)
            self.AM_display.insert("1.0",self.Amount)
            self.AM_display.tag_add("center", "1.0", "end")
            self.Set.focus_set()
            self.temp_disc= 0
        else:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error:\n Proper Weighing tool not selected...!\n Please click 'Select_Tool' button")
            
    def ragi_fun(self):
        self.weight_comparision()
        if self.weighing_tool != "Select_Tool" and self.Process == "Continue":
            self.Ragi_var = True
            self.Item_display.delete(0.0, END)
            self.Item_display.insert("1.0", "RAGI")
            self.Item_display.tag_add("center", "1.0", "end")
            self.common_item = self.Ragi_data
            self.Machine_name = "F Mc_2"
            if self.weight >= self.Ragi_disc_after__kg:#Discount limit validation
                self.temp_disc=self.weight*self.Wheat_disc_value
                if self.temp_disc >= self.Ragi_max_disc:
                    self.temp_disc = self.Ragi_max_disc
            self.Amount = (self.Ragi_price * self.weight)-self.temp_disc
            if self.temp_disc != 0:
                self.temp_disc= int(self.temp_disc)#"%.2f" % round(self.temp_disc, 0)
                self.discount= self.temp_disc
            self.Amount = "%.2f" % round(self.Amount, 2)
            self.Price_display.delete(0.0, END)
            self.Price_display.insert("1.0",self.Ragi_price)
            self.Price_display.tag_add("center", "1.0", "end")
            self.Dis_display.delete(0.0, END)
            self.Dis_display.insert("1.0",self.temp_disc)
            self.Dis_display.tag_add("center", "1.0", "end")
            self.AM_display.delete(0.0, END)
            self.AM_display.insert("1.0",self.Amount)
            self.AM_display.tag_add("center", "1.0", "end")
            self.Set.focus_set()
            self.temp_disc= 0
        else:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error:\n Proper Weighing tool not selected...!\n Please click 'Select_Tool' button")
            
    def chilli_fun(self):
        self.weight_comparision()
        if self.weighing_tool != "Select_Tool" and self.Process == "Continue":
            self.Chilli_var = True
            self.Item_display.delete(0.0, END)
            self.Item_display.insert("1.0", "CHILLI")
            self.Item_display.tag_add("center", "1.0", "end")
            self.common_item = self.Chilli_data
            self.Machine_name = "F Mc_3"
            if self.weight >= self.Chilli_disc_after__kg:
                self.temp_disc=self.weight*self.Chilli_disc_value
                if self.temp_disc >= self.Chilli_max_disc:
                    self.temp_disc = self.Chilli_max_disc
            self.Amount = (self.Chilli_price * self.weight)-self.temp_disc
            if self.temp_disc != 0:
                self.temp_disc= int(self.temp_disc)#"%.2f" % round(self.temp_disc, 0)
                self.discount= self.temp_disc
            self.Amount = "%.2f" % round(self.Amount, 2)
            self.Price_display.delete(0.0, END)
            self.Price_display.insert("1.0",self.Chilli_price)
            self.Price_display.tag_add("center", "1.0", "end")
            self.Dis_display.delete(0.0, END)
            self.Dis_display.insert("1.0",self.temp_disc)
            self.Dis_display.tag_add("center", "1.0", "end")
            self.AM_display.delete(0.0, END)
            self.AM_display.insert("1.0",self.Amount)
            self.AM_display.tag_add("center", "1.0", "end")
            self.Set.focus_set()
            self.temp_disc= 0
        else:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error:\n Proper Weighing tool not selected...!\n Please click 'Select_Tool' button")
        
    def dhaniya_fun(self):
        self.weight_comparision()
        if self.weighing_tool != "Select_Tool" and self.Process == "Continue":
            self.Dhaniya_var = True
            self.Item_display.delete(0.0, END)
            self.Item_display.insert("1.0", "DHANIYA")
            self.Item_display.tag_add("center", "1.0", "end")
            self.common_item = self.Dhaniya_data
            self.Machine_name = "F Mc_3"
            if self.weight >= self.Dhaniya_disc_after__kg:
                self.temp_disc=self.weight*self.Dhaniya_disc_value
                if self.temp_disc >= self.Dhaniya_max_disc:
                    self.temp_disc = self.Dhaniya_max_disc
            self.Amount = (self.Dhaniya_price * self.weight)-self.temp_disc
            if self.temp_disc != 0:
                self.temp_disc= int(self.temp_disc)#"%.2f" % round(self.temp_disc, 0)
                self.discount= self.temp_disc
            self.Amount = "%.2f" % round(self.Amount, 2)
            self.Price_display.delete(0.0, END)
            self.Price_display.insert("1.0",self.Dhaniya_price)
            self.Price_display.tag_add("center", "1.0", "end")
            self.Dis_display.delete(0.0, END)
            self.Dis_display.insert("1.0",self.temp_disc)
            self.Dis_display.tag_add("center", "1.0", "end")
            self.AM_display.delete(0.0, END)
            self.AM_display.insert("1.0",self.Amount)
            self.AM_display.tag_add("center", "1.0", "end")
            self.Set.focus_set()
            self.temp_disc= 0
        else:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error:\n Proper Weighing tool not selected...!\n Please click 'Select_Tool' button")
            
    def stop_M1_Rice_blink(self):
        self.M1_status = "Ready"        
        self.update_M1_table()
        print("wewewe")
        self.RiceCallback()
        GPIO.output(self.m1_stop_P,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.m1_stop_P,GPIO.LOW)

    def stop_M1_Wheat_blink(self):
        self.M1_status = "Ready"
        self.WheatCallback()
        self.update_M1_table()
        GPIO.output(self.m1_stop_P,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.m1_stop_P,GPIO.LOW)

    def stop_M1_Chickpea_blink(self):
        self.M1_status = "Ready"
        self.ChickpeaCallback()
        self.update_M1_table()
        GPIO.output(self.m1_stop_P,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.m1_stop_P,GPIO.LOW)

    def stop_M2_Ragi_blink(self):
        self.M2_status = "Ready"
        self.RagiCallback()
        self.update_M2_table()
        GPIO.output(self.m2_stop_P,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.m2_stop_P,GPIO.LOW)

    def stop_M3_Chilli_blink(self):
        self.M3_status = "Ready"
        self.ChilliCallback()
        self.update_M3_table()
        GPIO.output(self.m3_stop_P,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.m3_stop_P,GPIO.LOW)

    def stop_M3_Dhaniya_blink(self):
        self.M3_status = "Ready"
        self.DhaniyaCallback()
        self.update_M3_table()
        GPIO.output(self.m3_stop_P,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.m3_stop_P,GPIO.LOW)

    def trig_rasp_out(self):  # To start Raspberry Pi function
        try:
            x = self.select_treeview.selection()[0]
            if self.push_contents[1] == self.Rice_data and self.M1_status == "Ready":
                self.select_treeview.item(self.row_to_run,
                    values=(self.repush_contents[0],self.repush_contents[1],self.repush_contents[2],"Running...",self.repush_contents[4],self.repush_contents[5],self.repush_contents[6],self.push_contents[7],),)
                self.add_to_table()
                self.Rice_run_time = self.Rice_time * self.weight
                self.Rice_run_time = int(self.Rice_run_time)
                self.RiceCallback()
                time.sleep(0.5)
                GPIO.output(self.m1_start_P,GPIO.HIGH)
                self.rice_stop = root.after(self.Rice_run_time, self.stop_M1_Rice_blink)
            elif self.push_contents[1] == self.Wheat_data and self.M1_status == "Ready":
                self.select_treeview.item(self.row_to_run,
                    values=(self.repush_contents[0],self.repush_contents[1],self.repush_contents[2],"Running...",self.repush_contents[4],self.repush_contents[5],self.repush_contents[6],self.push_contents[7],),)
                self.add_to_table()
                self.Wheat_run_time = self.Wheat_time * self.weight
                self.Wheat_run_time = int(self.Wheat_run_time)
                self.WheatCallback()
                time.sleep(0.5)
                GPIO.output(self.m1_start_P,GPIO.HIGH)
                root.after(self.Wheat_run_time, self.stop_M1_Wheat_blink)
            elif (self.push_contents[1] == self.Chickpea_data and self.M1_status == "Ready"):
                self.select_treeview.item(self.row_to_run,
                    values=(self.repush_contents[0],self.repush_contents[1],self.repush_contents[2],"Running...",self.repush_contents[4],self.repush_contents[5],self.repush_contents[6],self.push_contents[7],),)
                self.add_to_table()
                self.Chickpea_run_time = self.Chickpea_time * self.weight
                self.Chickpea_run_time = int(self.Chickpea_run_time)
                self.ChickpeaCallback()
                time.sleep(0.5)
                GPIO.output(self.m1_start_P,GPIO.HIGH)
                root.after(self.Chickpea_run_time, self.stop_M1_Chickpea_blink)
            elif self.push_contents[1] == self.Ragi_data and self.M2_status == "Ready":
                self.select_treeview.item(self.row_to_run,
                    values=(self.repush_contents[0],self.repush_contents[1],self.repush_contents[2],"Running...",self.repush_contents[4],self.repush_contents[5],self.repush_contents[6],self.push_contents[7],),)
                self.add_to_table()
                self.Ragi_run_time = self.Ragi_time * self.weight
                self.Ragi_run_time = int(self.Ragi_run_time)
                self.RagiCallback()
                time.sleep(0.5)
                GPIO.output(self.m2_start_P,GPIO.HIGH)
                root.after(self.Ragi_run_time, self.stop_M2_Ragi_blink)
            elif (self.push_contents[1] == self.Chilli_data and self.M3_status == "Ready"):
                self.select_treeview.item(self.row_to_run,
                    values=(self.repush_contents[0],self.repush_contents[1],self.repush_contents[2],"Running...",self.repush_contents[4],self.repush_contents[5],self.repush_contents[6],self.push_contents[7],),)
                self.add_to_table()
                self.Chilli_run_time = self.Chilli_time * self.weight
                self.Chilli_run_time = int(self.Chilli_run_time)
                self.ChilliCallback()
                time.sleep(0.5)
                GPIO.output(self.m3_start_P,GPIO.HIGH)
                root.after(self.Chilli_run_time, self.stop_M3_Chilli_blink)

            elif (self.push_contents[1] == self.Dhaniya_data and self.M3_status == "Ready"):
                self.select_treeview.item(self.row_to_run,
                    values=(self.repush_contents[0],self.repush_contents[1],self.repush_contents[2],"Running...",self.repush_contents[4],self.repush_contents[5],self.repush_contents[6],self.push_contents[7],),)
                self.add_to_table()
                self.Dhaniya_run_time = self.Dhaniya_time * self.weight
                self.Dhaniya_run_time = int(self.Dhaniya_run_time)
                self.DhaniyaCallback()
                time.sleep(0.5)
                GPIO.output(self.m3_start_P,GPIO.HIGH)
                root.after(self.Dhaniya_run_time, self.stop_M3_Dhaniya_blink)

            else:
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1201O\nPlease wait...!\nMachine is Busy...!")
            x = ()
        except IndexError as erlog:
            self.all_log=erlog
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error: 1201N\nNone Token_no selected to Run")

    def Tool_frame_close(self):
        temp_tool = (self.Tool_10kg_below_value_entry.get(),self.Tool_10kg_above_value_entry.get(),self.Tool_25kg_above_value_entry.get(),)
        chesh_count = 1
        if (temp_tool[0] != "" or temp_tool[1] != "" or temp_tool[2] != ""):  # validation of empty entry box
            try:
                for chish in temp_tool:
                    sqt = "UPDATE tool_table SET Tool_weight='%s' WHERE Sl_no= '%s'" % (chish,chesh_count,)
                    self.datacursor.execute(sqt)
                    chesh_count += 1
                self.cat.commit()
                self.inform_func()
                self.info_display.insert(0.0, "info:\n Tool Weight updated sucessfully...!")
                sqt = "SELECT Amount From price_list WHERE Sl_no= 1"
                self.datacursor.execute(sqt)
                new_chickpea = self.datacursor.fetchone()
                self.Chickpea_price = new_chickpea[0]
                self.Frame_Tool_window.destroy()
            except mysql.connector.errors.ProgrammingError as er:
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812A\n" + er.msg)
            except mysql.connector.errors.DatabaseError:
                self.Numeric_value_errors()
        else:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error: 1201K\n Entry fields can't be empty...!")

    def selected_to_remove(self):
        try:
            self.datacursor.execute("select * from user_details")
            neet = self.datacursor.fetchall()
            for peet in neet:
                if peet[1] == self.remove_user.get():
                    keet = peet[0]
            self.datacursor.execute("DELETE FROM user_details WHERE Sl_no={}".format(keet))
            self.cat.commit()
            try:
                self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                if self.cat:
                    self.datacursor = self.cat.cursor(buffered=True)
                    self.datacursor.execute("SELECT User_name FROM user_details")
                    for_combobox = self.datacursor.fetchall()
                    for moveinto in for_combobox:
                        self.remove_user["values"] = (moveinto,)
                    self.remove_user.current(0)
            except mysql.connector.errors.InterfaceError as erlog:
                self.all_log=erlog
                self.interface_error_handle()
            self.remove_user.current(0)
        except UnboundLocalError as erlog:
            self.all_log=erlog
            self.error_func()
            self.error_display.insert(0.0, "Error: 1812K\n User not found to remove")

    def selected_changepswd(self):
        if self.new_pass.get() != self.re_new_pass.get():
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error:\n Please enter same password in both the fields...!")
        elif self.new_pass.get() == "" or self.re_new_pass.get() == "":
            self.empty_pass_error()
        elif self.new_pass.get() == self.re_new_pass.get():            
            entered_pass_change = ("'" + self.re_new_pass.get() + "'")  # To add password inside the single quotes(else Mysql will not accept)
            try:
                self.datacursor.execute("select * from user_details")
                neet = self.datacursor.fetchall()  # here neet is a temparary variable
                for peet in neet:
                    if (peet[1] == self.for_pass_change):  # confirming user before updating inot databasepeet[0]=serial no, peet[1]=user name,peet[2]=user pass
                        keet = peet[0]
                self.datacursor.execute("UPDATE user_details SET User_pass={} WHERE Sl_no={}".format(entered_pass_change, keet))
                self.cat.commit()
                for off_check in self.Address.keys():
                    if self.for_pass_change == off_check:
                        self.Address[off_check] = self.re_new_pass.get()
                self.to_place_inform_display()
                self.info_display.insert(0.0, "info:\n New Password Updated successfully...!")
                self.Frame_changepswd_window.destroy()
            except UnboundLocalError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812K\n User not found to change Pswd...!")
            except mysql.connector.errors.ProgrammingError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812A\n Codding error, Please evalute the script once...!")
            except mysql.connector.errors.IntegrityError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0,"Error:\n Entered Password is not accepted by Database, Please try some other password...!",)
                error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                hour = time.strftime("%H")
                minute = time.strftime("%M")
                second = time.strftime("%S")
                te = hour+':'+minute+':'+second
                error_logging.write("{} {}, while changing user pswd, IntegrityError (Error code:1812J), This exception is raised when the foreign key constraint fails. {}\n".format(et,te,self.all_log))
                error_logging.close()

    def Numeric_value_errors(self):
        self.to_place_error_display()
        self.error_display.insert(0.0, "Error: 1812G\n Please enter only Numeric values...!")

    def empty_pass_error(self):
        self.to_place_error_display()
        self.error_display.insert(0.0, "Error: 1201B\n All fields are required...!")

    def Price_entry_field_empty_error(self):  # this func works when entry fields of settings window is empty
        self.to_place_error_display()
        self.error_display.insert(0.0, "Error: 1201K\n Entry fields can't be empty...!")

    def to_place_error_display(self):
        if self.info_display.winfo_exists() == True:
            self.info_display.destroy()
            self.error_func()
        elif self.error_display.winfo_exists() == True:
            self.error_display.delete(0.0, END)
        else:
            self.error_func()

    def to_place_inform_display(self):
        if self.error_display.winfo_exists() == True:
            self.error_display.destroy()
            self.inform_func()
        elif self.info_display.winfo_exists() == True:
            self.info_display.delete(0.0, END)
            self.inform_func()
        else:
            self.inform_func()        

    def Chickpea_save_price(self):
        if (self.Chickpea_entry.get() != "" and self.Chickpea_disc_entry.get() != "" and self.Chickpea_price_entry.get() != "" and self.Chickpea_disc_value_entry.get() != "" and self.Chickpea_max_disc_limit.get() !=""):
            try:
                sqt = "UPDATE price_list SET Time='%s', Discount='%s',Amount='%s',Discount_value='%s',Max_disc='%s' WHERE Item= '%s'" % (
                    self.Chickpea_entry.get(),self.Chickpea_disc_entry.get(),self.Chickpea_price_entry.get(),self.Chickpea_disc_value_entry.get(),self.Chickpea_max_disc_limit.get(),self.Chickpea_data,)
                self.datacursor.execute(sqt)
                self.cat.commit()
                self.inform_func()
                self.info_display.insert(0.0, "info:\n Chickpea parameter updated...!")
                sqt = "SELECT Amount From price_list WHERE Sl_no= 1"
                self.datacursor.execute(sqt)
                new_chickpea = self.datacursor.fetchone()
                self.Chickpea_price = new_chickpea[0]
            except mysql.connector.errors.ProgrammingError as er:
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812A\n %s"%(self.all_log))
            except mysql.connector.errors.DatabaseError as erlog:
                self.all_log=erlog
                self.Numeric_value_errors()
        else:
            self.Price_entry_field_empty_error()

    def Wheat_save_price(self):
        if (self.Wheat_entry.get() != "" and self.Wheat_disc_entry.get() != "" and self.Wheat_price_entry.get() != "" and self.Wheat_disc_value_entry.get() != "" and self.Wheat_max_disc_limit.get() !=""):
            try:
                sqt = "UPDATE price_list SET Time='%s', Discount='%s',Amount='%s',Discount_value='%s',Max_disc='%s' WHERE Item= '%s'" % (
                    self.Wheat_entry.get(),self.Wheat_disc_entry.get(),self.Wheat_price_entry.get(),self.Wheat_disc_value_entry.get(),self.Wheat_max_disc_limit.get(),self.Wheat_data,)
                self.datacursor.execute(sqt)
                self.cat.commit()
                self.inform_func()
                self.info_display.insert(0.0, "info:\n Wheat parameter updated...!")
                sqt = "SELECT Amount From price_list WHERE Sl_no= 3"
                self.datacursor.execute(sqt)
                new_wheat = self.datacursor.fetchone()
                self.Wheat_price = new_wheat[0]
            except mysql.connector.errors.ProgrammingError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812A\n %s"%(self.all_log))
            except mysql.connector.errors.DatabaseError as erlog:
                self.all_log=erlog
                self.Numeric_value_errors()
        else:
            self.Price_entry_field_empty_error()

    def Rice_save_price(self):
        if (self.Rice_entry.get() != "" and self.Rice_disc_entry.get() != "" and self.Rice_price_entry.get() != "" and self.Rice_disc_value_entry.get() != "" and self.Rice_max_disc_limit.get() !=""):
            try:
                sqt = "UPDATE price_list SET Time='%s', Discount='%s',Amount='%s',Discount_value='%s',Max_disc='%s' WHERE Item= '%s'" % (
                    self.Rice_entry.get(),self.Rice_disc_entry.get(),self.Rice_price_entry.get(),self.Rice_disc_value_entry.get(),self.Rice_max_disc_limit.get(),self.Rice_data,)
                self.datacursor.execute(sqt)
                self.cat.commit()
                self.inform_func()
                self.info_display.insert(0.0, "info:\n Rice parameter updated...!")
                sqt = "SELECT Amount From price_list WHERE Sl_no= 2"
                self.datacursor.execute(sqt)
                new_rice = self.datacursor.fetchone()
                self.Rice_price = new_rice[0]
            except mysql.connector.errors.ProgrammingError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812A\n%s"%(self.all_log))
            except mysql.connector.errors.DatabaseError as erlog:
                self.all_log=erlog
                self.Numeric_value_errors()
        else:
            self.Price_entry_field_empty_error()

    def Ragi_save_price(self):
        if (self.Ragi_entry.get() != "" and self.Ragi_disc_entry.get() != "" and self.Ragi_price_entry.get() != "" and self.Ragi_disc_value_entry.get() != "" and self.Ragi_max_disc_limit.get()!=""):
            try:
                sqt = "UPDATE price_list SET Time='%s', Discount='%s',Amount='%s',Discount_value='%s',Max_disc='%s' WHERE Item= '%s'" % (
                    self.Ragi_entry.get(),self.Ragi_disc_entry.get(),self.Ragi_price_entry.get(),self.Ragi_disc_value_entry.get(),self.Ragi_max_disc_limit.get(),self.Ragi_data,)
                self.datacursor.execute(sqt)
                self.cat.commit()
                self.inform_func()
                self.info_display.insert(0.0, "info:\n Ragi parameter updated...!")
                sqt = "SELECT Amount From price_list WHERE Sl_no= 4"
                self.datacursor.execute(sqt)
                new_ragi = self.datacursor.fetchone()
                self.Ragi_price = new_ragi[0]
            except mysql.connector.errors.ProgrammingError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812A\n%s"%(self.all_log))
            except mysql.connector.errors.DatabaseError as erlog:
                self.all_log=erlog
                self.Numeric_value_errors()
        else:
            self.Price_entry_field_empty_error()

    def Chilli_save_price(self):
        if (self.Chilli_entry.get() != "" and self.Chilli_disc_entry.get() != "" and self.Chilli_price_entry.get() != "" and self.Chilli_disc_value_entry.get() != "" and self.Chilli_max_disc_limit.get() !=""):
            try:
                sqt = "UPDATE price_list SET Time='%s', Discount='%s',Amount='%s',Discount_value='%s',Max_disc='%s' WHERE Item= '%s'" % (
                    self.Chilli_entry.get(),self.Chilli_disc_entry.get(),self.Chilli_price_entry.get(),self.Chilli_disc_value_entry.get(),self.Chilli_max_disc_limit.get(),self.Chilli_data,)
                self.datacursor.execute(sqt)
                self.cat.commit()
                self.inform_func()
                self.info_display.insert(0.0, "info:\n Chilli parameter updated...!")
                sqt = "SELECT Amount From price_list WHERE Sl_no= 5"
                self.datacursor.execute(sqt)
                new_chilli = self.datacursor.fetchone()
                self.Chilli_price = new_chilli[0]
            except mysql.connector.errors.ProgrammingError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812A\n%s"%(self.all_log))
            except mysql.connector.errors.DatabaseError as erlog:
                self.all_log=erlog
                self.Numeric_value_errors()
        else:
            self.Price_entry_field_empty_error()

    def Dhaniya_save_price(self):
        if (self.Dhaniya_entry.get() != "" and self.Dhaniya_disc_entry.get() != "" and self.Dhaniya_price_entry.get() != "" and self.Dhaniya_disc_value_entry.get() != "" and self.Dhaniya_max_disc_limit.get()!=""):
            try:
                sqt = "UPDATE price_list SET Time='%s', Discount='%s',Amount='%s',Discount_value='%s',Max_disc='%s' WHERE Item= '%s'" % (self.Dhaniya_entry.get(),self.Dhaniya_disc_entry.get(),
                    self.Dhaniya_price_entry.get(),self.Dhaniya_disc_value_entry.get(),self.Dhaniya_max_disc_limit.get(),self.Dhaniya_data,)
                self.datacursor.execute(sqt)
                self.cat.commit()
                self.inform_func()
                self.info_display.insert(0.0, "info:\n Dhaniya parameter updated...!")
                sqt = "SELECT Amount From price_list WHERE Sl_no= 6"
                self.datacursor.execute(sqt)
                new_dhaniya = self.datacursor.fetchone()
                self.Dhaniya_price = new_dhaniya[0]
            except mysql.connector.errors.ProgrammingError as erlog:
                self.all_log=erlog
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812A\n%s"%(self.all_log))
            except mysql.connector.errors.DatabaseError as erlog:
                self.all_log=erlog
                self.Numeric_value_errors()
        else:
            self.Price_entry_field_empty_error()

    def update_txt(self):
        if self.M1_status == "Ready" and self.M2_status == "Ready" and self.M3_status == "Ready":
            try:
                speed_test = Speedtest()
                download = speed_test.download()
                upload = speed_test.upload()
                download_speed = round(download / (10 ** 6), 2)
                upload_speed = round(upload / (10 ** 6), 2)
                self.to_place_inform_display()
                self.info_display.insert(0.0, "info:\n     ↑{}Mbps\n     ↓{}Mbps".format(upload_speed,download_speed))
            except:
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1201J\n No Internet connection\nCheck Wifi/Network cable...!")

    def on_close_icon(self):
        try:        
            icon_press = messagebox.askokcancel("Close", "Do you want to close Application?")
            if (icon_press == 1 and self.M1_status == "Ready" and self.M2_status == "Ready" and self.M3_status == "Ready"):
                GPIO.cleanup()
                self.log_flash = not self.log_flash
                self.closing_mysql()
                self.root.quit()
            elif icon_press == 1:
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1201L\n Machine status is 'Busy', Can't close application...!")
             
        except AttributeError:
            if (icon_press == 1 and self.M1_status == "Ready" and self.M2_status == "Ready" and self.M3_status == "Ready"):
                self.root.quit()
            else:
                self.to_place_error_display()
                self.error_display.insert(0.0, "Error: 1812F\n Machine status is 'Busy', Can't close application...!")
        except Exception as erlog:
            self.all_log=erlog
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error: 1812H\n'%s'"%(self.all_log))
            icon_press = messagebox.askokcancel("Close", "Do you want to close Application?")
            if icon_press == 1:
                self.root.quit()

    def power_cut_activity(self):
        iExit = messagebox.askyesno("Logout", "Are you sure of Power Cut?")
        if (iExit > 0):
            self.log_flash = not self.log_flash
            self.closing_mysql()
            if self.M1_status =="Busy" and self.M1_item == "Rice":
                self.root.after_cancel(self.rice_stop)
                print("nonono")
            self.root.after_cancel(self.join)
            shutoff.off_command()
            self.root.destroy()

    def AutoSMS(self):
        self.machine_collect = self.Machine_names.get()
        self.mode_collect = self.Select_mode.get()
        if (self.machine_collect != "Machine Name"and self.mode_collect != "Select_Mode"):
            if self.mode_collect == "Auto":
                client = clx.xms.Client(service_plan_id="3b9e7dae8c484747bad93bccbad6bd6b",
                    token="e60bac91271a44af86fb7414817459f5",)
                create = clx.xms.api.MtBatchTextSmsCreate()
                create.sender = "447537404817"
                create.recipients = {"917795284155"}
                create.body = "{} Switched to {} mode at {}".format(self.machine_collect, self.mode_collect, te)
                if self.machine_collect == "F Mc_1":
                    GPIO.output(self.m1_manual_start,GPIO.HIGH)
                elif self.machine_collect == "F Mc_2":
                    GPIO.output(self.m2_manual_start,GPIO.HIGH)
                elif self.machine_collect == "F Mc_3":
                    GPIO.output(self.m3_manual_start,GPIO.HIGH)
                elif self.machine_collect == "All_Machines":
                    GPIO.output(self.m1_manual_start,GPIO.HIGH)
                    GPIO.output(self.m2_manual_start,GPIO.HIGH)
                    GPIO.output(self.m3_manual_start,GPIO.HIGH)
                
                try:
                    batch = client.create_batch(create)
                except (requests.exceptions.RequestException,clx.xms.exceptions.ApiException,) as ex:
                    self.to_place_error_display()
                    self.error_display.insert(0.0, "Failed to communicate with XMS: %s" % str(ex))
                error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                error_logging.write("{} {}, {} switched {} to {}\n".format(et,te,self.user_entered_name,self.machine_collect,self.mode_collect))
                error_logging.close()

            if self.mode_collect == "Manual":
                client = clx.xms.Client(service_plan_id="3b9e7dae8c484747bad93bccbad6bd6b",
                    token="e60bac91271a44af86fb7414817459f5",)
                create = clx.xms.api.MtBatchTextSmsCreate()
                create.sender = "447537404817"
                create.recipients = {"917795284155"}
                create.body = "{} Switched to Manual mode at {}".format(self.machine_collect, te)
                if self.machine_collect == "F Mc_1":
                    GPIO.output(self.m1_manual_start,GPIO.LOW)
                elif self.machine_collect == "F Mc_2":
                    GPIO.output(self.m2_manual_start,GPIO.LOW)
                elif self.machine_collect == "F Mc_3":
                    GPIO.output(self.m3_manual_start,GPIO.LOW)
                elif self.machine_collect == "All_Machines":
                    GPIO.output(self.m1_manual_start,GPIO.LOW)
                    GPIO.output(self.m2_manual_start,GPIO.LOW)
                    GPIO.output(self.m3_manual_start,GPIO.LOW)
                    
                try:
                    batch = client.create_batch(create)
                except (requests.exceptions.RequestException,clx.xms.exceptions.ApiException,) as ex:
                    self.to_place_error_display()
                    self.error_display.insert(0.0, "Failed to communicate with XMS: %s" % str(ex))
                error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                error_logging.write("{} {}, {} switched {} to {}\n".format(et,te,self.user_entered_name,self.machine_collect,self.mode_collect))
                error_logging.close()
        else:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error:\n Please select the Machine & Mode to switch...!")

flash_delay = 500  # msec between colour change
flash_colours = ("white", "black")  # Two colours to swap between


class Login(datalog):
    def to_read_IP(self):
        try:
            if os.access("/lib/subba/Temp_data.pkl", os.R_OK):
                with open("/lib/subba/Temp_data.pkl", "rb") as self.for_address:
                    self.Address = pickle.load(self.for_address)
                    self.for_address.close()
                    print(self.Address)
        except FileNotFoundError:
            self.to_place_error_display()
            self.error_display.insert(0.0,"Error: 1201G\nSource file not found...!\nPlease Please install back-up file...!",)
            self.iExit = messagebox.showerror("Error!", "Application has error, Pls refer Error box...!")
            sys.exit()
        except NameError:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error: 1201H\nCoding Error, Try with backup Script...!")
            if os.access("C:/Users/Subramanya M S/Documents/CFM/Temp_data.pkl", os.W_OK):
                with open("/lib/subba/Temp_data.pkl", "wb") as self.for_address:
                    self.for_address.close()
            self.iExit = messagebox.showerror("Error!", "Application has error, Pls refer Error box...!")
            sys.exit()
        except EOFError as erlog:
            self.all_log=erlog
            self.all_log = str(self.all_log)
            if self.all_log == "Ran out of input":
                self.to_place_error_display()
                self.error_display.insert(0.0,"Error: 1201I\n Temp data is empty...!\nPlease Please install back-up file...!",)

            if os.access("/lib/subba/Temp_data.pkl", os.W_OK):
                with open("/lib/subba/Temp_data.pkl", "wb") as self.for_address:
                    self.for_address.close()
            self.iExit = messagebox.showerror("Error!", "Application has error, Pls refer Error box...!")
            sys.exit()

    def to_write_IP(self):
        try:
            with open("/lib/subba/Temp_data.pkl", "wb") as self.for_address:
                pickle.dump(self.Address, self.for_address,protocol=2)
                self.for_address.close()
        except EOFError:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error: 1201I\n Source file is empty or not closed properly...!")
            self.for_address.close()
        except NameError:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error: 1201H\n Coding Error, Please check script...!")
            self.for_address.close()
        
    def __init__(self, root):
        self.root = root
        self.root.title("CꟻM")
        # self.root.iconbitmap("/home/pi/Documents/CFM/process.ico")#C:/Users/Subramanya M S/Documents/CFM
        self.root.geometry("1200x670+30+40")
        self.root.resizable(False, False)
        self.flash_delay = 500
        self.flash_colours = ("white","#050800",)  # color storing for running indication display
        # ----BGImage----#
        self.bg = PhotoImage(file="/lib/subba/New_Flour.png")
        self.bg_image = Label(self.root, image=self.bg, background="white").place(x=0, y=0, relwidth=1, relheight=1)
        self.log_flash = None
        self.mill_name = PhotoImage(file="/lib/subba/Operator-view.png")
        self.mill_name_image = Label(self.root, image=self.mill_name, background="white").place(x=905, y=15)
        self.Frame_login = Frame(self.root, background="white")
        self.Frame_login.place(x=2, y=15, height=300, width=280)
        self.inform_func()  # Initializing information display
        self.info_display.destroy()
        self.admin_error_func()  # Initializing admin error display
        self.admin_error_display.destroy()
        self.error_func()  # Initializing error display
        self.error_display.destroy()
        self.Settings_Frame = False  # variable for inspecting frame existance
        self.IP_Frame = False  # variable for inspecting frame existance
        self.Manual_Frame = False  # variable for inspecting frame existance
        self.number_Frame = False
        self.input_output_Frame = False
        self.adding_frame = False  # variable for inspecting frame existance
        self.tool_frame = False  # variable for inspecting frame existance
        self.changingpswd_frame = False  # variable for inspecting frame existance
        self.removeuser_frame = False  # variable for inspecting frame existance
        self.IP_admin_Frame_login = False  # variable for inspecting frame existance
        self.to_read_IP()  # reading IP to connect database
        self.Internet_status = None  # variable to save internet status
        self.M1_status = "Ready"
        self.M2_status = "Ready"
        self.M3_status = "Ready"
        self.M1_drop_no = []
        self.M2_drop_no = []
        self.M3_drop_no = []
        self.csv_M1_data_waiting=None
        self.csv_M2_data_waiting=None
        self.csv_M3_data_waiting=None
        title = Label(self.Frame_login,text="User Login Area",font=("Calibri", 22, "bold"),foreground="#d77337",background="white",).place(x=40, y=30)
        combostyle = ttk.Style()
        
        combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'white','fieldbackground': 'white','background': 'light gray','foreground':'black','selectforeground':'black'}}})
# ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
        combostyle.theme_use('combostyle')
        self.txt_user = ttk.Combobox(self.Frame_login,font=("calibri", 14),state="readonly",justify=CENTER,)
        self.txt_user["values"] = ("User name",)
        try:  # connecting to database to fetch user name and store into login box
            self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
            if self.cat:
                self.datacursor = self.cat.cursor(buffered=True)
                self.datacursor.execute("SELECT User_name FROM user_details")
                for_combobox = self.datacursor.fetchall()
                for moveinto in for_combobox:
                    self.txt_user["values"] = self.txt_user["values"] + (moveinto,)
                self.Internet_status = "Good"
        except mysql.connector.errors.ProgrammingError as erlog:
            self.all_log=erlog
            self.error_func()
            #self.error_display.insert(0.0,"Error: 1812A\nUnable to connect Database...!\nCheck DB User name/pswd/DB name...!",)
            self.error_display.insert(0.0, "Error: 1812A\n'%s'"%(self.all_log.msg))
            self.to_analyse_issue()
        except mysql.connector.errors.InterfaceError as erlog:
            self.all_log=erlog
            print(self.all_log)
            self.interface_error_handle()
            self.Internet_status = "Bad"
            self.to_analyse_issue()
        except requests.exceptions.SSLError as erlog:
            self.all_log=erlog
            self.error_func()
            self.error_display.insert(0.0, "Error: 1812C\n'%s'"%(self.all_log))
            self.writing_log()
        
        except mysql.connector.errors.OperationalError as erlog:
            self.all_log=erlog
            self.error_func()
            self.error_display.insert(0.0, "Error: 1812D\n'%s'"%(self.all_log))
            self.writing_log()
        except KeyError:
            self.error_func()
            self.error_display.insert(0.0,"Error:1812C\nServer Address might got manipulated & is not in Dot decimal notation format...!\nTo correct, Click Change IP Address button...",)
            self.to_analyse_issue()
        self.txt_user.place(x=50, y=90, height=26, width=180)
        self.txt_user.bind("<Return>", lambda event=None: self.login_btn.invoke())
        self.txt_user.current(0)
        self.txt_pass = Entry(self.Frame_login,font=("calibri", 15),show="•",background="#FFFFC9",bd=1,justify="center",)
        self.txt_pass.insert(0, "Password")
        self.txt_pass.config(state=DISABLED)
        self.txt_pass.bind("<Button-1>", self.main_login_click)
        self.txt_pass.place(x=50, y=135, height=26, width=180)
        self.txt_pass.bind("<Return>", lambda event=None: self.login_btn.invoke())
        # self.txt_pass.bind('<Enter>', self.login_function)
        self.login_btn = Button(self.Frame_login,command=self.login_function,cursor="hand2",background="#d77337",text="Login",foreground="white",activebackground="#d77337",highlightthickness =0, bd=0,
            font=("calibri", 15, "bold"),relief=FLAT,)
        self.login_btn.place(bordermode=OUTSIDE,x=50, y=180, height=30)
        root.protocol("WM_DELETE_WINDOW", self.on_close_icon)
                        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.m1_start_P=3 # Defining variable for Pi I/O
        self.m1_stop_P=5 # Defining variable for Pi I/O
        self.m2_start_P=7 # Defining variable for Pi I/O
        self.m2_stop_P=11 # Defining variable for Pi I/O
        self.m3_start_P=13 # Defining variable for Pi I/O
        self.m3_stop_P=15 # Defining variable for Pi I/O
        self.m1_manual_start=19 # Defining variable for Pi I/O
        self.m2_manual_start=21 # Defining variable for Pi I/O
        self.m3_manual_start=23 # Defining variable for Pi I/O
        GPIO.setup(self.m1_start_P,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(self.m1_stop_P,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.m2_start_P,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(self.m2_stop_P,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.m3_start_P,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(self.m3_stop_P,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.m1_manual_start,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(self.m2_manual_start,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(self.m3_manual_start,GPIO.OUT,initial=GPIO.HIGH)

    def admin_Frame_ip_change(self):  # Admin login window for offline IP change
        if self.error_display.winfo_exists() == True:
            self.error_display.destroy()
        if self.info_display.winfo_exists() == True:
            self.info_display.destroy()
        self.Frame_admin_window = Frame(self.root, bg="white")
        self.Frame_admin_window.place(x=495, y=155, height=210, width=230)
        self.IP_admin_Frame_login = True
        self.admin_login = Label(
            self.Frame_admin_window,text="Admin Login Area",font=("Calibri", 16, "bold"),background="white",foreground="#d77337",).place(x=23, y=18)
        self.txt_admin = ttk.Combobox(self.Frame_admin_window,font=("calibri", 13),state="readonly",justify=CENTER,)
        self.txt_admin["values"] = ("Admin",)
        for to_combobox in self.Address.keys():
            if to_combobox != "Database_address":
                self.txt_admin["values"] = self.txt_admin["values"] + (to_combobox,)
        self.txt_admin.place(x=35, y=60, height=26, width=130)
        self.txt_admin.bind("<Return>", lambda event=None: login_btn.invoke())
        self.txt_admin.current(0)
        self.admin_pass = Entry(self.Frame_admin_window,font=("calibri", 14),show="•",background="#FFFFC9",justify="center",)
        self.admin_pass.insert(0, "Password")
        self.admin_pass.config(state=DISABLED)
        self.admin_pass.bind("<Button-1>", self.admin_login_click)
        self.admin_pass.place(x=35, y=100, height=26, width=130)
        self.admin_pass.bind("<Return>", lambda event=None: login_btn.invoke())
        login_btn = Button(self.Frame_admin_window,
            command=lambda: self.admin_validation(),cursor="hand2",text="Login",background="#d77337",activebackground="#d77337",
            bd=0,highlightthickness =0,foreground="white",font=("calibri", 12, "bold"),relief=FLAT,)
        login_btn.place(bordermode=OUTSIDE,x=30, y=148, height=25, width=70)
        cancel_btn = Button(self.Frame_admin_window,command=self.cancel_admin_frame,cursor="hand2",text="Cancel",activebackground="white",
            bd=0,highlightthickness =0,foreground="#d77337",background="white",font=("calibri", 12, "bold"),relief=FLAT,)
        cancel_btn.place(bordermode=OUTSIDE,x=110, y=148)

    def to_analyse_issue(self):
        change_ip_btn = Button(self.Frame_login,command=self.admin_Frame_ip_change,cursor="hand2",text="|Change IP Address|",foreground="#d77337",activebackground="white",font=("calibri", 11),background="white",highlightthickness =0, bd=0,
            relief=FLAT)
        change_ip_btn.place(bordermode=OUTSIDE,x=133, y=173, width=120)
        check_internet_btn = Button(self.Frame_login,command=self.update_txt,cursor="hand2",text="|Check Internet Speed|",fg="#d77337",background="white",activebackground="white",highlightthickness =0, bd=0, 
            font=("calibri", 11),relief=FLAT)
        check_internet_btn.place(bordermode=OUTSIDE,x=133, y=208, width=138)

    def IP_entry_Frame(self):
        self.Frame_admin_window.destroy()
        self.IP_Frame = True
        self.IP_entry_Frame_window = Frame(self.root, bg="white")
        self.IP_entry_Frame_window.place(x=495, y=155, height=215, width=230)
        self.Address_label = Label(self.IP_entry_Frame_window,text="Enter Database Address",font=("Calibri", 13, "bold"),background="white",foreground="#d77337",).place(x=15, y=18)
        enter_ip = Label(self.IP_entry_Frame_window,text="Enter:",font=("Calibri", 10),background="white",foreground="dark blue",).place(x=2, y=68)
        self.ip_enter = Entry(self.IP_entry_Frame_window,font=("calibri", 13),background="#FFFFC9",justify="center",)
        self.ip_enter.insert(0, "IP Address")
        self.ip_enter.config(state=DISABLED)
        self.ip_enter.bind("<Button-1>", self.IP_entry_click)
        self.ip_enter.place(x=55, y=68, height=26, width=130)
        re_enter_ip = Label(self.IP_entry_Frame_window,text="Re-enter:",font=("Calibri", 10),background="white",foreground="dark blue",).place(x=2, y=106)
        self.ip_re_enter = Entry(self.IP_entry_Frame_window,font=("calibri", 13),background="#FFFFC9",justify="center",)
        self.ip_re_enter.insert(0, "IP Address")
        self.ip_re_enter.config(state=DISABLED)
        self.ip_re_enter.bind("<Button-1>", self.IP_re_entry_click)
        self.ip_re_enter.place(x=55, y=106, height=26, width=130)
        check_ip_btn = Button(self.IP_entry_Frame_window,command=self.find_ip,cursor="hand2",text="|Check IP Address|",foreground="#d77337",
            background="white",highlightthickness=0, bd=0,font=("calibri", 9),relief=FLAT)
        check_ip_btn.place(bordermode=OUTSIDE,x=48, y=135, width=110)
        Set_btn = Button(self.IP_entry_Frame_window,command=lambda: self.IP_validation(),cursor="hand2",text="Set",activebackground="#d77337",background="#d77337",
            bd=0,highlightthickness=0,foreground="white",font=("calibri", 13, "bold"),relief=FLAT)
        Set_btn.place(bordermode=OUTSIDE,x=55, y=168, height=25, width=50)
        cancel_btn = Button(self.IP_entry_Frame_window,command=self.cancel_admin_frame,cursor="hand2",text="Cancel",activebackground="white",bd=0,highlightthickness=0,
            foreground="#d77337",background="white",font=("calibri", 13, "bold"),relief=FLAT,)
        cancel_btn.place(bordermode=OUTSIDE,x=120, y=168)

    # *************User login_bsckground*************#

    def admin_error_func(self):
        self.admin_error_display = Text(master=root,height=5,width=33,font=("Calibri", 12),foreground="red",background="#FFFFC9",wrap=WORD,)
        self.admin_error_display.tag_configure("center", justify="center")
        self.admin_error_display.place(x=20, y=270)

    def error_func(self):
        self.error_display = Text(master=root,height=5,width=33,font=("Calibri", 12),foreground="red",background="#FFFFC9",wrap=WORD,)
        self.error_display.tag_configure("center", justify="center")
        self.error_display.place(x=20, y=270)

    def inform_func(self):
        self.info_display = Text(master=root,height=5,width=33,font=("Calibri", 12),foreground="green",background="#FFFFC9",wrap=WORD,)
        self.info_display.place(x=20, y=270)

    def clock(self):
        if self.log_flash == True:
            hour = time.strftime("%H")
            minute = time.strftime("%M")
            second = time.strftime("%S")
            hour= int(hour)
            if hour < 12:
                self.trial_clock.config(foreground="red")
            elif hour >= 12:
                self.trial_clock.config(foreground="black")
            hour = str(hour)
            # everyday = date.today()
            # d = everyday.strftime("%d/%m/%Y")
            self.trial_clock.config(text=hour + ":" + minute + ":" + second)
            self.join = self.root.after(200, self.clock)

    # *************User logout*************#

    def logout(self):
        iExit = messagebox.askyesno("Logout", "Are you sure want to logout?")
        iExit.config(bg = "white",font=("calibri", 13, "bold"))
        if (iExit > 0 and self.M1_status == "Ready" and self.M2_status == "Ready" and self.M3_status == "Ready"):
            self.log_flash = not self.log_flash
            self.closing_mysql()
            self.root.after_cancel(self.join)
            self.root.destroy()
            
    def settings_logout(self):
        self.admin_window.destroy()

    # *************Machine running indication(flashing)*****************#
    def flashColour(self, object, colour_index):
        if self.log_flash == True:
            object.config(foreground=self.flash_colour[colour_index])
            root.after(self.flashdelay, self.flashColour, object, 1 - colour_index)

    def riceflashColour(self, Rice_btn, colour_index):
        if self.rice_flashing:
            self.Rice_btn.config(foreground=self.flash_colours[colour_index])
            root.after(flash_delay, self.riceflashColour, self.Rice_btn, 1 - colour_index)
        else:
            Rice_btn.config(foreground=self.flash_colours[0])

    def RiceCallback(self):
        self.rice_flashing
        self.rice_flashing = not self.rice_flashing
        if self.rice_flashing:
            self.riceflashColour(self, 0)
        else:
            pass

    def wheatflashColour(self, Wheat_btn, colour_index):
        if self.wheat_flashing:
            self.Wheat_btn.config(foreground=self.flash_colours[colour_index])
            root.after(flash_delay, self.wheatflashColour, self.Wheat_btn, 1 - colour_index)
        else:
            Wheat_btn.config(foreground=self.flash_colours[0])

    def WheatCallback(self):
        self.wheat_flashing
        self.wheat_flashing = not self.wheat_flashing
        if self.wheat_flashing:
            self.wheatflashColour(self, 0)
        else:
            pass

    def chickpeaflashColour(self, Chickpea_btn, colour_index):
        if self.chickpea_flashing:
            self.Chickpea_btn.config(foreground=self.flash_colours[colour_index])
            root.after(flash_delay,self.chickpeaflashColour,self.Chickpea_btn,1 - colour_index,)
        else:
            Chickpea_btn.config(foreground=self.flash_colours[0])

    def ChickpeaCallback(self):
        self.chickpea_flashing
        self.chickpea_flashing = not self.chickpea_flashing
        if self.chickpea_flashing:
            self.chickpeaflashColour(self, 0)
        else:
            pass

    def ragiflashColour(self, Ragi_btn, colour_index):
        if self.ragi_flashing:
            self.Ragi_btn.config(foreground=self.flash_colours[colour_index])
            root.after(flash_delay, self.ragiflashColour, self.Ragi_btn, 1 - colour_index)
        else:
            Ragi_btn.config(foreground=self.flash_colours[0])

    def RagiCallback(self):
        self.ragi_flashing
        self.ragi_flashing = not self.ragi_flashing
        if self.ragi_flashing:
            self.ragiflashColour(self, 0)
        else:
            pass

    def chilliflashColour(self, Chilli_btn, colour_index):
        if self.chilli_flashing:
            self.Chilli_btn.config(foreground=self.flash_colours[colour_index])
            root.after(flash_delay, self.chilliflashColour, self.Chilli_btn, 1 - colour_index)
        else:
            Chilli_btn.config(foreground=self.flash_colours[0])

    def ChilliCallback(self):
        self.chilli_flashing
        self.chilli_flashing = not self.chilli_flashing
        if self.chilli_flashing:
            self.chilliflashColour(self, 0)
        else:
            pass

    def dhaniyaflashColour(self, Dhaniya_btn, colour_index):
        if self.dhaniya_flashing:
            self.Dhaniya_btn.config(foreground=self.flash_colours[colour_index])
            root.after(flash_delay, self.dhaniyaflashColour, self.Dhaniya_btn, 1 - colour_index)
        else:
            Dhaniya_btn.config(foreground=self.flash_colours[0])

    def DhaniyaCallback(self):
        self.dhaniya_flashing
        self.dhaniya_flashing = not self.dhaniya_flashing
        if self.dhaniya_flashing:
            self.dhaniyaflashColour(self, 0)
        else:
            pass
    
    def manual_fun(self):
        if self.Manual_Frame_window.winfo_exists() == False:
            self.Manual_Frame = True
            self.Manual_Frame_window = Frame(self.root, bg="white")
            self.Manual_Frame_window.place(x=495, y=200, height=230, width=210)
            self.Changeover_label = Label(self.Manual_Frame_window,text="Auto/Manual mode",font=("Calibri", 14, "bold"),
                background="white",foreground="#d77337",).place(x=23, y=18)
            self.Machine_names = ttk.Combobox(self.Manual_Frame_window,font=("calibri", 13),state="readonly",justify=CENTER,)
            self.Machine_names["values"] = ("Machine Name","F Mc_1","F Mc_2","F Mc_3","All_Machines",)
            self.Machine_names.place(x=27, y=68, height=26, width=140)
            self.Machine_names.current(0)
            self.Select_mode = ttk.Combobox(self.Manual_Frame_window,font=("calibri", 13),state="readonly",justify=CENTER,)
            self.Select_mode["values"] = ("Select_Mode", "Auto", "Manual")
            self.Select_mode.place(x=27, y=106, height=26, width=140)
            self.Select_mode.current(0)
            self.Select_mode.bind("<Return>", lambda event=None: Confirm_btn.invoke())
            power_cut_btn = Button(self.Manual_Frame_window,command=self.power_cut_activity,
                cursor="hand2",text="|Power Cut off|",bd=0,highlightthickness =0,foreground="#d77337",background="white",activebackground="white",font=("calibri", 11),relief=FLAT,)
            power_cut_btn.place(bordermode=OUTSIDE,x=20, y=135)
            Confirm_btn = Button(self.Manual_Frame_window,command=lambda: self.AutoSMS(),
                cursor="hand2",text="Confirm",background="#d77337",bd=0,highlightthickness =0,foreground="white",activebackground="#d77337",font=("calibri", 11, "bold"),relief=FLAT,)
            Confirm_btn.place(bordermode=OUTSIDE,x=28, y=168,width=70)            
            cancel_btn = Button(self.Manual_Frame_window,command=self.cancel_admin_frame,
                cursor="hand2",text="Cancel",bd=0,highlightthickness =0,foreground="#d77337",background="white",activebackground="white",font=("calibri", 11, "bold"),relief=FLAT,)
            cancel_btn.place(bordermode=OUTSIDE,x=106, y=168)

    def input_output_status_window(self):
        if self.input_output_Frame_window.winfo_exists() == False:
            self.input_output_Frame = True
            self.input_output_Frame_window = Frame(self.root, bg="white")
            self.input_output_Frame_window.place(x=495, y=200, height=230, width=250)
            status_label = Label(self.input_output_Frame_window,text="I/O Status",font=("Calibri", 14, "bold"),background="white",foreground="#d77337",).place(x=23, y=18)
            name1 = Label(self.input_output_Frame_window,text="Internet Status:",font=("Calibri", 12),background="light gray",foreground="dark blue",).place(x=15, y=60)
            status1 = Label(self.input_output_Frame_window,text=self.Internet_status,font=("Calibri", 14),background="light gray",foreground="black",).place(x=122, y=58)
            name2 = Label(self.input_output_Frame_window,text="F Mc_1:",font=("Calibri", 12),background="light gray",foreground="dark blue",).place(x=15, y=85)
            status2 = Label(self.input_output_Frame_window,text=self.M1_status,font=("Calibri", 14),background="white",foreground="black",).place(x=122, y=83)
            name3 = Label(self.input_output_Frame_window,text="F Mc_2:",font=("Calibri", 12),background="white",foreground="dark blue",).place(x=15, y=110)
            status3 = Label(self.input_output_Frame_window,text=self.M2_status,font=("Calibri", 14),background="white",foreground="black",).place(x=122, y=108)
            name4 = Label(self.input_output_Frame_window,text="F Mc_3:",font=("Calibri", 12),background="white",foreground="dark blue",).place(x=15, y=135)
            status4 = Label(self.input_output_Frame_window,text=self.M3_status,font=("Calibri", 14),background="white",foreground="black",).place(x=122, y=133)
            name5 = Label(self.input_output_Frame_window,text="Power Status:",font=("Calibri", 12),background="white",foreground="dark blue",).place(x=15, y=160)
            statusR5 = Label(self.input_output_Frame_window,text=self.M3_status,font=("Calibri", 14),background="white",foreground="black",).place(x=122, y=158)
            statusY5 = Label(self.input_output_Frame_window,text=self.M3_status,font=("Calibri", 14),background="white",foreground="black",).place(x=135, y=158)
            statusB5 = Label(self.input_output_Frame_window,text=self.M3_status,font=("Calibri", 14),background="white",foreground="black",).place(x=122, y=158)
            
            close_btn = Button(self.input_output_Frame_window,command=self.cancel_admin_frame,
                cursor="hand2",text="Close",bd=0,highlightthickness =0,foreground="#d77337",background="white",activebackground="white",font=("calibri", 12, "bold"),relief=FLAT,)
            close_btn.place(bordermode=OUTSIDE,x=120, y=175)

    def contact_entry_fun(self):
        if self.contact_window.winfo_exists() == False and self.common_item != "":
            self.number_Frame = True
            self.contact_window=Frame(self.root, bg="white")
            self.contact_window.place(x=480, y=200,height=220, width=240)
            self.contact_label = Label(self.contact_window,text="Shopper\n Contact no:",font=("Calibri", 16, "bold"),background="white",
                    foreground="#d77337",).place(x=27, y=20)
            self.contact_entry = Entry(self.contact_window,font=("calibri", 14),background="#FFFFC9",justify="center",)
            self.contact_entry.focus_set()
            self.contact_entry.bind("<Escape>", lambda event=None: skip_btn.invoke())
            self.contact_entry.bind("<Return>", lambda event=None: continue_btn.invoke())
            self.contact_entry.place(x=30, y=100, height=28, width=150)
            continue_btn = Button(self.contact_window,command=lambda: self.contact_num_yes(),cursor="hand2",text="Continue",activebackground="#d77337",
                    background="#d77337",bd=0,highlightthickness =0,foreground="white",font=("calibri", 12, "bold"),relief=FLAT,)
            continue_btn.place(bordermode=OUTSIDE,x=27, y=150, width=70)
            skip_btn = Button(self.contact_window,command= lambda : self.contact_num_no(),cursor="hand2",text="Skip",bd=0,activebackground="white",highlightthickness=0,
                foreground="#d77337",background="white",font=("calibri", 13, "bold"),relief=FLAT,)
            skip_btn.place(bordermode=OUTSIDE,x=135, y=150)
        elif self.weighing_tool == "Select_Tool":
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error:\n Weighing tool not selected...!\n Please click 'Select_Tool' button")
            

    def select_to_run(self):
        self.select_window = Toplevel(root)
        self.select_window.title("Selection")
        # self.select_window.iconbitmap("C:/Users/Subramanya M S/Documents/CFM/process.ico")
        self.select_window.geometry("735x542+1100+350")
        self.select_bg = PhotoImage(file="/lib/subba/process.png")
        self.select_bg_image = Label(self.select_window, image=self.select_bg,background="white",).place(x=0, y=0, relwidth=1, relheight=1)
        select_run = Frame(self.select_window, relief=FLAT, background="white")
        select_run.place(x=5, y=5, width=725, height=400)

        xscrollbar = Scrollbar(select_run, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)

        # Vertical (y) Scroll Bar
        yscrollbar = Scrollbar(select_run)
        yscrollbar.pack(side=RIGHT, fill=Y)

        selection_style = ttk.Style()
        selection_style.theme_use("clam")
        self.select_treeview = ttk.Treeview(select_run,columns=("token no","item","machine_name","status","weight","discount","amount","contact no"),
            xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set,)
        # Configure the scrollbars
        xscrollbar.config(command=self.select_treeview.xview)
        yscrollbar.config(command=self.select_treeview.yview)
        self.select_treeview.heading("token no", text="Token_no")
        self.select_treeview.heading("item", text="Item")
        self.select_treeview.heading("machine_name", text="Machine_Name")
        self.select_treeview.heading("status", text="Status")
        self.select_treeview.heading("weight", text="Weight")
        self.select_treeview.heading("discount", text="Discount")
        self.select_treeview.heading("amount", text="Amount")
        self.select_treeview.heading("contact no", text="Contact_No")
        self.select_treeview["show"] = "headings"
        self.select_treeview.column("token no", width=70, anchor="center")
        self.select_treeview.column("item", width=50, anchor="center")
        self.select_treeview.column("machine_name", width=105, anchor="center")
        self.select_treeview.column("status", width=60, anchor="center")
        self.select_treeview.column("weight", width=60, anchor="center")
        self.select_treeview.column("discount", width=55, anchor="center")
        self.select_treeview.column("amount", width=55, anchor="center")
        self.select_treeview.column("contact no", width=75, anchor="center")
        self.select_treeview.pack(fill=BOTH, expand=1)
        self.select_treeview.bind("<ButtonRelease-1>", self.row_clicked)
        Drop = Button(self.select_window,command=self.drop_selected,
            cursor="hand2",text="Drop",background="#d77337",bd=0,highlightthickness =0,foreground="white",activebackground="#d77337",font=("calibri",12,"bold",),relief=SUNKEN,)
        Drop.place(bordermode=OUTSIDE,x=145, y=435, width=65)
        Start = Button(self.select_window,command=self.trig_rasp_out,
            cursor="hand2",text="Run <F11>",background="#d77337",bd=0,highlightthickness =0,foreground="white",activebackground="#d77337",font=("calibri",12,"bold",),relief=SUNKEN,)
        Start.place(bordermode=OUTSIDE,x=500, y=435, width=85)
        root.bind("<F11>",self.parallel_trig_rasp_out)
        
    def row_clicked(self, ev):
        self.row_to_run = self.select_treeview.focus()
        run_contents = self.select_treeview.item(self.row_to_run)
        self.push_contents = run_contents["values"]#Capture the data of row selected and storing in list
        self.repush_contents = self.select_treeview.item(self.row_to_run, "values")
                
    def admin_fun(self):
        if self.Settings_Frame == False and self.admin_window.winfo_exists() == False:
            self.admin_window = Toplevel(self.root)
            self.admin_window.title("Settings")
            # self.admin_window.iconbitmap("C:/Users/Subramanya M S/Documents/CFM/process.ico")
            self.admin_window.geometry("622x512+410+50")
            self.admin_bg = PhotoImage(file="/lib/subba/process.png")
            self.admin_bg_image = Label(self.admin_window, image=self.admin_bg,background="white").place(x=0, y=0, relwidth=1, relheight=1)
            self.Frame_admin_window = Frame(self.admin_window, bg="white")
            self.Frame_admin_window.place(x=200, y=108, height=210, width=220)
            self.admin_login = Label(self.Frame_admin_window,text="Admin Login Area",font=("Calibri", 16, "bold"),background="white",
                foreground="#d77337",).place(x=25, y=18)
            self.txt_admin = ttk.Combobox(self.Frame_admin_window,font=("calibri", 13),state="readonly",justify=CENTER,)
            self.txt_admin["values"] = ("Admin", "Subramanya")
            self.txt_admin.place(x=30, y=60, height=26, width=150)
            self.txt_admin.bind("<Return>", lambda event=None: login_btn.invoke())
            self.txt_admin.current(0)
            self.admin_pass = Entry(self.Frame_admin_window,font=("calibri", 14),show="•",background="#FFFFC9",justify="center",)
            self.admin_pass.insert(0, "Password")
            self.admin_pass.config(state=DISABLED)
            self.admin_pass.bind("<Button-1>", self.admin_login_click)
            self.admin_pass.place(x=30, y=100, height=26, width=150)
            self.admin_pass.bind("<Return>", lambda event=None: login_btn.invoke())
            self.Settings_Frame = True
            login_btn = Button(self.Frame_admin_window,command=lambda: self.admin_validation(),cursor="hand2",text="Login",activebackground="#d77337",
                background="#d77337",bd=0,highlightthickness =0,foreground="white",font=("calibri", 12, "bold"),relief=FLAT,)
            login_btn.place(bordermode=OUTSIDE,x=30, y=148, width=70)
            cancel_btn = Button(self.Frame_admin_window,command=self.cancel_admin_frame,cursor="hand2",text="Cancel",activebackground="white",bd=0,highlightthickness =0,
                foreground="#d77337",background="white",font=("calibri", 13, "bold"),relief=FLAT,)
            cancel_btn.place(bordermode=OUTSIDE,x=110, y=148)

    def settings_fun(self):
        self.Frame_admin_window.destroy()
        self.Frame_settings_window = Frame(self.admin_window)
        self.Frame_settings_window.place(x=0, y=0, relheight=1, relwidth=1)
        self.settings_bg = PhotoImage(file="/lib/subba/process.png")
        self.settings_bg_image = Label(self.Frame_settings_window, image=self.settings_bg,background="white").place(x=0, y=0, relwidth=1, relheight=1)
        Item_list = Label(self.Frame_settings_window,text="Item",font=("Calibri", 11, "bold"),foreground="black",background="white",justify="center")
        Item_list.place(x=12, y=1)
        time_label = Label(self.Frame_settings_window,text="Time\n(min)/Kg",font=("Calibri", 11, "bold"),foreground="black",background="white")
        time_label.place(x=90, y=1, width=80)
        set_price_label = Label(self.Frame_settings_window,text="Price\nKg",font=("Calibri", 11, "bold"),foreground="black",background="white")
        set_price_label.place(x=168, y=1,width=70)
        Discount_on_label = Label(self.Frame_settings_window,text=">__Kg\nDisc",font=("Calibri", 11, "bold"),foreground="black",background="white")
        Discount_on_label.place(x=232, y=1,width=90)
        Discount_value_label = Label(self.Frame_settings_window,text="Disc\nvalue",font=("Calibri", 11, "bold"),foreground="black",background="white")
        Discount_value_label.place(x=308, y=1,width=80)
        Discount_max_disc_label = Label(self.Frame_settings_window,text="Max\nDisc",font=("Calibri", 11, "bold"),foreground="black",background="white")
        Discount_max_disc_label.place(x=398, y=1,width=80)
        Chickpea_time = Label(self.Frame_settings_window,text="Chickpea:",font=("Calibri", 14, "bold"),foreground="dark blue",background="white")
        Chickpea_time.place(x=20, y=50)
        self.Chickpea_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Chickpea_entry.place(x=105, y=50, height=30, width=50)
        self.Chickpea_entry.bind("<Return>", lambda event=None: self.Chickpea_save_btn.invoke())
        self.Chickpea_price_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Chickpea_price_entry.place(x=180, y=50, height=30, width=50)
        self.Chickpea_price_entry.bind("<Return>", lambda event=None: self.Chickpea_save_btn.invoke())
        self.Chickpea_disc_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Chickpea_disc_entry.place(x=255, y=50, height=30, width=50)
        self.Chickpea_disc_entry.bind("<Return>", lambda event=None: self.Chickpea_save_btn.invoke())
        self.Chickpea_disc_value_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Chickpea_disc_value_entry.place(x=330, y=50, height=30, width=50)
        self.Chickpea_disc_value_entry.bind("<Return>", lambda event=None: self.Chickpea_save_btn.invoke())        
        self.Chickpea_max_disc_limit = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Chickpea_max_disc_limit.place(x=410, y=50, height=30, width=50)
        self.Chickpea_max_disc_limit.bind("<Return>", lambda event=None: self.Chickpea_save_btn.invoke())
        self.Chickpea_save_btn = Button(self.Frame_settings_window,command=lambda: self.Chickpea_save_price(),cursor="hand2",
            text="Set",background="#d77337",bd=0,highlightthickness=0,foreground="white",activebackground="#d77337",font=("calibri", 13, "bold"),relief=FLAT,)
        self.Chickpea_save_btn.place(bordermode=OUTSIDE,x=500, y=49, width=60)
        Wheat_time = Label(self.Frame_settings_window,text="Wheat:",font=("Calibri", 14, "bold"),foreground="dark blue",background="white")
        Wheat_time.place(x=20, y=100)
        self.Wheat_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Wheat_entry.place(x=105, y=100, height=30, width=50)
        self.Wheat_entry.bind("<Return>", lambda event=None: self.Wheat_save_btn.invoke())
        self.Wheat_price_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Wheat_price_entry.place(x=180, y=100, height=30, width=50)
        self.Wheat_price_entry.bind("<Return>", lambda event=None: self.Wheat_save_btn.invoke())
        self.Wheat_disc_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Wheat_disc_entry.place(x=255, y=100, height=30, width=50)
        self.Wheat_disc_entry.bind("<Return>", lambda event=None: self.Wheat_save_btn.invoke())
        self.Wheat_disc_value_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Wheat_disc_value_entry.place(x=330, y=100, height=30, width=50)
        self.Wheat_disc_value_entry.bind("<Return>", lambda event=None: self.Wheat_save_btn.invoke())
        self.Wheat_max_disc_limit = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Wheat_max_disc_limit.place(x=410, y=100, height=30, width=50)
        self.Wheat_max_disc_limit.bind("<Return>", lambda event=None: self.Wheat_save_btn.invoke())
        self.Wheat_save_btn = Button(self.Frame_settings_window,command=lambda: self.Wheat_save_price(),cursor="hand2",text="Set",background="#d77337",
            bd=0,highlightthickness=0,foreground="white",activebackground="#d77337",font=("calibri", 13, "bold"),relief=FLAT,)
        self.Wheat_save_btn.place(bordermode=OUTSIDE,x=500, y=99, width=60)
        Rice_time = Label(self.Frame_settings_window,text="Rice:",font=("Calibri", 14, "bold"),foreground="dark blue",background="white")
        Rice_time.place(x=20, y=150)
        self.Rice_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Rice_entry.place(x=105, y=150, height=30, width=50)
        self.Rice_entry.bind("<Return>", lambda event=None: self.Rice_save_btn.invoke())
        self.Rice_price_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Rice_price_entry.place(x=180, y=150, height=30, width=50)
        self.Rice_price_entry.bind("<Return>", lambda event=None: self.Rice_save_btn.invoke())
        self.Rice_disc_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Rice_disc_entry.place(x=255, y=150, height=30, width=50)
        self.Rice_disc_entry.bind("<Return>", lambda event=None: self.Rice_save_btn.invoke())
        self.Rice_disc_value_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Rice_disc_value_entry.place(x=330, y=150, height=30, width=50)
        self.Rice_disc_value_entry.bind("<Return>", lambda event=None: self.Rice_save_btn.invoke())
        self.Rice_max_disc_limit = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Rice_max_disc_limit.place(x=410, y=150, height=30, width=50)
        self.Rice_max_disc_limit.bind("<Return>", lambda event=None: self.Rice_save_btn.invoke())
        self.Rice_save_btn = Button(self.Frame_settings_window,command=lambda: self.Rice_save_price(),cursor="hand2",text="Set",activebackground="#d77337",background="#d77337",bd=0,highlightthickness=0,
            foreground="white",font=("calibri", 13, "bold"),relief=FLAT,)
        self.Rice_save_btn.place(bordermode=OUTSIDE,x=500, y=149, width=60)
        Ragi_time = Label(self.Frame_settings_window,text="Ragi:",font=("Calibri", 14, "bold"),foreground="dark blue",background="white")
        Ragi_time.place(x=20, y=200)
        self.Ragi_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Ragi_entry.place(x=105, y=200, height=30, width=50)
        self.Ragi_entry.bind("<Return>", lambda event=None: self.Ragi_save_btn.invoke())
        self.Ragi_price_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Ragi_price_entry.place(x=180, y=200, height=30, width=50)
        self.Ragi_price_entry.bind("<Return>", lambda event=None: self.Ragi_save_btn.invoke())
        self.Ragi_disc_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Ragi_disc_entry.place(x=255, y=200, height=30, width=50)
        self.Ragi_disc_entry.bind("<Return>", lambda event=None: self.Ragi_save_btn.invoke())
        self.Ragi_disc_value_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Ragi_disc_value_entry.place(x=330, y=200, height=30, width=50)
        self.Ragi_disc_value_entry.bind("<Return>", lambda event=None: self.Ragi_save_btn.invoke())
        self.Ragi_max_disc_limit = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Ragi_max_disc_limit.place(x=410, y=200, height=30, width=50)
        self.Ragi_max_disc_limit.bind("<Return>", lambda event=None: self.Ragi_save_btn.invoke())
        self.Ragi_save_btn = Button(self.Frame_settings_window,command=lambda: self.Ragi_save_price(),
            cursor="hand2",text="Set",background="#d77337",activebackground="#d77337",bd=0,highlightthickness=0,foreground="white",font=("calibri", 13, "bold"),relief=FLAT,)
        self.Ragi_save_btn.place(bordermode=OUTSIDE,x=500, y=199, width=60)
        Chilli_time = Label(self.Frame_settings_window,text="Chilli:",font=("Calibri", 14, "bold"),foreground="dark blue",background="white")
        Chilli_time.place(x=20, y=250)
        self.Chilli_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Chilli_entry.place(x=105, y=250, height=30, width=50)
        self.Chilli_entry.bind("<Return>", lambda event=None: self.Chilli_save_btn.invoke())
        self.Chilli_price_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Chilli_price_entry.place(x=180, y=250, height=30, width=50)
        self.Chilli_price_entry.bind("<Return>", lambda event=None: self.Chilli_save_btn.invoke())
        self.Chilli_disc_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Chilli_disc_entry.place(x=255, y=250, height=30, width=50)
        self.Chilli_disc_entry.bind("<Return>", lambda event=None: self.Chilli_save_btn.invoke())
        self.Chilli_disc_value_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Chilli_disc_value_entry.place(x=330, y=250, height=30, width=50)
        self.Chilli_disc_value_entry.bind("<Return>", lambda event=None: self.Chilli_save_btn.invoke())
        self.Chilli_max_disc_limit = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Chilli_max_disc_limit.place(x=410, y=250, height=30, width=50)
        self.Chilli_max_disc_limit.bind("<Return>", lambda event=None: self.Chilli_save_btn.invoke())
        self.Chilli_save_btn = Button(self.Frame_settings_window,command=lambda: self.Chilli_save_price(),cursor="hand2",text="Set",background="#d77337",activebackground="#d77337",bd=0,highlightthickness=0,
            foreground="white",font=("calibri", 13, "bold"),relief=FLAT,)
        self.Chilli_save_btn.place(bordermode=OUTSIDE,x=500, y=249, width=60)
        Dhaniya_time = Label(self.Frame_settings_window,text="Dhaniya:",font=("Calibri", 14, "bold"),foreground="dark blue",background="white")
        Dhaniya_time.place(x=20, y=300)
        self.Dhaniya_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Dhaniya_entry.place(x=105, y=300, height=30, width=50)
        self.Dhaniya_entry.bind("<Return>", lambda event=None: self.Dhaniya_save_btn.invoke())
        self.Dhaniya_price_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Dhaniya_price_entry.place(x=180, y=300, height=30, width=50)
        self.Dhaniya_price_entry.bind("<Return>", lambda event=None: self.Dhaniya_save_btn.invoke())
        self.Dhaniya_disc_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Dhaniya_disc_entry.place(x=255, y=300, height=30, width=50)
        self.Dhaniya_disc_entry.bind("<Return>", lambda event=None: self.Dhaniya_save_btn.invoke())
        self.Dhaniya_disc_value_entry = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Dhaniya_disc_value_entry.place(x=330, y=300, height=30, width=50)
        self.Dhaniya_disc_value_entry.bind("<Return>", lambda event=None: self.Dhaniya_save_btn.invoke())
        self.Dhaniya_max_disc_limit = Entry(self.Frame_settings_window,font=("calibri", 12), background="#FFFFC9",justify="center",)
        self.Dhaniya_max_disc_limit.place(x=410, y=300, height=30, width=50)
        self.Dhaniya_max_disc_limit.bind("<Return>", lambda event=None: self.Dhaniya_save_btn.invoke())
        self.Dhaniya_save_btn = Button(self.Frame_settings_window,command=lambda: self.Dhaniya_save_price(),cursor="hand2",text="Set",activebackground="#d77337",background="#d77337",
            bd=0,highlightthickness=0,foreground="white",font=("calibri", 13, "bold"),relief=FLAT,)
        self.Dhaniya_save_btn.place(bordermode=OUTSIDE,x=500, y=299, width=60)
        settings_Logout_btn = Button(self.Frame_settings_window,command=self.settings_logout,cursor="hand2",text="Logout",background="#d77337",bd=0,highlightthickness=0,activebackground="#d77337",
            foreground="white",font=("calibri",10,"bold",),relief=RAISED,)
        settings_Logout_btn.place(bordermode=OUTSIDE,x=480, y=410, width=76)
        remove_user_btn = Button(self.Frame_settings_window,command=self.removing_user,cursor="hand2",text="Remove User",activebackground="#d77337",background="#d77337",
            bd=0,highlightthickness=0,foreground="white",font=("calibri", 10, "bold"),)
        remove_user_btn.place(bordermode=OUTSIDE,x=33, y=370)
        add_user_btn = Button(self.Frame_settings_window,command=self.adding_user,cursor="hand2",text="Add new User",activebackground="#d77337",background="#d77337",bd=0,highlightthickness=0,
            foreground="white",font=("calibri", 10, "bold"),)
        add_user_btn.place(bordermode=OUTSIDE,x=31, y=410)
        change_pass_btn = Button(self.Frame_settings_window,command=self.changing_pswd,cursor="hand2",text="Change Pswd",background="#d77337",activebackground="#d77337",bd=0,highlightthickness=0,foreground="white",
            font=("calibri", 10, "bold"),)
        change_pass_btn.place(bordermode=OUTSIDE,x=34, y=450)
        Tool_manage_btn = Button(self.Frame_settings_window,command=self.Tool_settings,cursor="hand2",text="Tool Settings",background="#d77337",activebackground="#d77337",bd=0,highlightthickness=0,foreground="white",
            font=("calibri", 10, "bold"),)
        Tool_manage_btn.place(bordermode=OUTSIDE,x=145, y=370)
        Month_data_btn = Button(self.Frame_settings_window,command=self.month_trans_view,cursor="hand2",text="TMT",background="#d77337",activebackground="#d77337",bd=0,highlightthickness=0,
            foreground="white",font=("calibri", 10, "bold"),)
        Month_data_btn.place(bordermode=OUTSIDE,x=145, y=410, width=70)
        self.TPD_retrive()
        self.admin_window.protocol("WM_DELETE_WINDOW", self.on_settings_close_icon)

    def month_trans_view(self):
        self.month_window = Toplevel(root)
        self.month_window.title("Monthly Transaction Tracking")
        # self.month_window.iconbitmap("C:/Users/Subramanya M S/Documents/CFM/process.ico")
        self.month_window.geometry("745x522+410+50")
        monthly_tree_total = Frame(self.month_window, relief=FLAT, bg="white")
        monthly_tree_total.place(x=5, y=5, width=735, height=390)
        self.month_window.configure(bg="white")
        self.Y_graph_list = []
        self.X_graph_list = []
        xscrollbar = Scrollbar(monthly_tree_total, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)
        # Vertical (y) Scroll Bar
        yscrollbar = Scrollbar(monthly_tree_total)
        yscrollbar.pack(side=RIGHT, fill=Y)
        self.for_month_treeview = ttk.Treeview(monthly_tree_total,columns=("sl_no","token no","item","contact no","date","time","weight","amount",),
            xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set,)
        # Configure the scrollbars
        xscrollbar.config(command=self.for_month_treeview.xview)
        yscrollbar.config(command=self.for_month_treeview.yview)
        self.for_month_treeview.heading("sl_no", text="Sl no")
        self.for_month_treeview.heading("token no", text="Token no")
        self.for_month_treeview.heading("item", text="Item")
        self.for_month_treeview.heading("contact no", text="Contact no")
        self.for_month_treeview.heading("time", text="Time")
        self.for_month_treeview.heading("date", text="Date")
        self.for_month_treeview.heading("weight", text="Weight")
        self.for_month_treeview.heading("amount", text="Amount")
        self.for_month_treeview["show"] = "headings"
        self.for_month_treeview.column("sl_no", width=37, anchor="center")
        self.for_month_treeview.column("token no", width=50, anchor="center")
        self.for_month_treeview.column("item", width=50, anchor="center")
        self.for_month_treeview.column("contact no", width=75, anchor="center")
        self.for_month_treeview.column("time", width=75, anchor="center")
        self.for_month_treeview.column("date", width=75, anchor="center")
        self.for_month_treeview.column("weight", width=50, anchor="center")
        self.for_month_treeview.column("amount", width=53, anchor="center")
        self.for_month_treeview.pack(fill=BOTH, expand=1)
        self.month_select = ttk.Combobox(self.month_window, font=("calibri", 15), state="readonly", justify=CENTER)
        self.month_select["values"] = ("User name",)
        self.date_dropbox = ttk.Combobox(self.month_window,font=("calibri", 10),state="readonly",background="white",justify=CENTER,)
        self.date_dropbox["values"] = (
            "Date","All","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31",)
        self.date_dropbox.place(x=20, y=400, height=25, width=55)
        self.date_dropbox.current(0)
        self.month_dropbox = ttk.Combobox(self.month_window,font=("calibri", 10),state="readonly",background="white",justify=CENTER,)
        self.month_dropbox["values"] = ("Month","01","02","03","04","05","06","07","08","09","10","11","12",)
        self.month_dropbox.place(x=80, y=400, height=25, width=65)
        self.month_dropbox.current(0)
        self.year_dropbox = ttk.Combobox(self.month_window,font=("calibri", 10),state="readonly",background="white",justify=CENTER,)
        self.year_dropbox["values"] = ("Year", "2020", "2021")
        self.year_dropbox.place(x=150, y=400, height=25, width=60)
        self.year_dropbox.current(0)
        check_btn = Button(self.month_window,command=lambda: self.load_treeview(),cursor="hand2",text="Show data",bd=0,activebackground="white", highlightthickness =0,background="white",
            foreground="#d77337",font=("calibri", 10, "bold"),relief=FLAT,)
        check_btn.place(bordermode=OUTSIDE,x=20, y=433)
        trans_graph_btn = Button(self.month_window,command=self.graph_ploting,cursor="hand2",text="Show Trans Trend",bd=0,activebackground="white",highlightthickness =0,background="white",
             foreground="#d77337",font=("calibri", 10, "bold"),relief=FLAT,)
        trans_graph_btn.place(bordermode=OUTSIDE,x=20, y=455)
        mc_graphic_btn = Button(self.month_window,command=self.graph_ploting,cursor="hand2",text="Show Machine Trend",bd=0,activebackground="white",highlightthickness=0,background="white",foreground="#d77337",
            font=("calibri", 10, "bold"),relief=FLAT,)
        mc_graphic_btn.place(bordermode=OUTSIDE,x=20, y=477)
        Total_label = Label(self.month_window,text="Total:",font=("Calibri", 12,"bold"),foreground="dark blue",background="white").place(x=475, y=427)
        self.month_Total_show = Text(master=self.month_window,height=1,width=9,font=("Calibri", 16),foreground="black",background="#FFFFC9",wrap=WORD,)
        self.month_Total_show.tag_configure("center", justify="center")
        self.month_Total_show.place(x=525, y=423, width=80)

    def load_treeview(self):
        self.for_month_treeview.delete(*self.for_month_treeview.get_children())
        self.month_Total_show.delete(0.0, END)
        into_total = 0.0
        cpt = 1
        self.drop_date = self.date_dropbox.get()
        self.drop_month = self.month_dropbox.get()
        drop_year = self.year_dropbox.get()
        self.Y_graph_list = []
        self.X_graph_list = []
        if self.info_display.winfo_exists() == True:
            self.info_display.destroy()
        elif self.error_display.winfo_exists() == True:
            self.error_display.destroy()
        if self.drop_date == "Date" or self.drop_month == "Month" or drop_year == "Year":
            self.to_place_error_display()
            self.error_display.insert(0.0,"Error:\n Please select all selction(Date,Month,Year) and click 'Show' button...!",)
        if self.drop_date != "Date" and self.drop_month != "Month" and drop_year != "Year":
            drop_year = int(drop_year)#Converting string into int for year comparision purpose
            if (drop_year % 400 == 0) or ((drop_year % 4 == 0) and (drop_year % 100 != 0)):  # validating whether it's leap year or not
                leap_year = True
            else:
                leap_year = False
            drop_year = str(drop_year)
            if (leap_year == True and self.drop_month == "02"):  # saving days for leap year
                self.feb_date = 29
            elif leap_year == False and self.drop_month == "02":
                self.feb_date = 28
            if self.drop_date == "All" and self.drop_month == "02":
                self.max_date = self.feb_date
            elif self.drop_date == "All" and (self.drop_month == "01"or "03"or "05"or "07"or "08"or "10"or "12"):
                self.max_date = 31
            else:
                self.max_date = 30
            if self.drop_date == "30" or self.drop_date == "31":
                if self.drop_month == "02":
                    self.to_place_error_display()
                    self.error_display.insert(0.0, "Error:\nFebruary month has no 30 and 31 date...!")

            elif self.drop_date == "29" and self.drop_month == "02" and leap_year == False:
                self.to_place_error_display()
                self.error_display.insert(0.0,"Error:\nDate 29 can't accept, Since selected year is not a Leap year...!",)

            elif self.drop_date == "All" and self.drop_month != "Month":
                check_table = "SELECT * FROM {today} where MM=%s".format(today= 'transaction_data')
                self.datacursor.execute(check_table, (self.drop_month,))
                result = self.datacursor.fetchall()
                into_total = float(into_total)
                self.datacursor.execute("SELECT * FROM {today} where MM=%s and YYYY=%s".format(today='transaction_data'),(self.drop_month,for_year,),)
                forinto = self.datacursor.fetchall()
                x_graph_variable= None
                y_graph_variable= None
                for row in forinto:                    
                    self.for_month_treeview.insert("","end",values=(cpt,row[1],row[5],row[8],row[2],row[3],row[6],row[7],),)
                    if x_graph_variable == row[10] or x_graph_variable == None:
                        if y_graph_variable == None:
                            y_graph_variable = row[7]
                        else:
                            y_graph_variable+= row[7]
                        y_graph_variable = int(y_graph_variable)
                    else:
                        self.Y_graph_list.append(y_graph_variable)
                    if x_graph_variable != row[10]:
                        x_graph_variable = row[10]
                        self.X_graph_list.append(row[10])
                        y_graph_variable= None
                    cpt += 1
                if len(self.X_graph_list) != len(self.Y_graph_list):
                    if y_graph_variable == None:
                            y_graph_variable = row[7]
                    else:
                        y_graph_variable+= row[7]
                    self.Y_graph_list.append(y_graph_variable)
                self.datacursor.execute("SELECT SUM(Amount) AS totalsum FROM {today} where MM=%s".format(today='transaction_data'),(self.drop_month,),)
                res = (self.datacursor.fetchall())  # temporary variable to save fetched data
                for sit in res:
                    for sat in sit:
                        if sat != None:
                            sat = float(sat)
                            into_total += sat
                self.month_Total_show.delete(0.0, END)
                into_total = "%.2f" % round(into_total, 2)
                self.month_Total_show.insert(1.0, into_total)
                self.month_Total_show.tag_add("center", "1.0", "end")
            else:
                try:
                    self.datacursor.execute("SELECT * FROM {today} where DD=%s".format(today='transaction_data'),(self.drop_date,),)
                    result = self.datacursor.fetchall()
                    into_total = float(into_total)
                    print(result)
                    if result != []:
                        x_graph_variable= None
                        for row in result:
                            self.for_month_treeview.insert("","end",values=(cpt,row[1],row[5],row[8],row[2],row[3],row[6],row[7],),)
                            if x_graph_variable != row[10]:
                                x_graph_variable = row[10]
                                self.X_graph_list.append(row[10])
                            cpt += 1
                        self.datacursor.execute("SELECT SUM(Amount) AS totalsum FROM {today} where DD=%s and YYYY=%s".format(today='transaction_data'),(self.drop_date,for_year,),) # to add all transaction amount of respective date
                        res = (self.datacursor.fetchall())  # temporary variable to save fetched data
                        for sit in res:
                            for sat in sit:
                                if sat != None:
                                    sat = float(sat)
                                    into_total += sat
                        if res != [(None,)]:
                            self.Y_graph_list.append(sat)
                        elif res == [(None,)]:
                            self.Y_graph_list.append(0)
                        self.month_Total_show.delete(0.0, END)
                        into_total = "%.2f" % round(into_total, 2)
                        self.month_Total_show.insert(1.0, into_total)
                        self.month_Total_show.tag_add("center", "1.0", "end")
                    elif result == []:
                        self.to_place_error_display()
                        self.error_display.insert(0.0, "Error:\n No data found for selected date...!\n Might have not done transaction on selected date...!")
                except mysql.connector.errors.ProgrammingError as erlog:
                    self.all_log=erlog
                    self.to_place_error_display()
                    self.error_display.insert(0.0, "Error: 1812A\nNone item is running in F Mc_3")
                    error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                    hour = time.strftime("%H")
                    minute = time.strftime("%M")
                    second = time.strftime("%S")
                    te = hour+':'+minute+':'+second
                    error_logging.write("{} {}, while updating M3 data {}\n".format(et,te,self.all_log))
                    error_logging.close()
                except mysql.connector.errors.InterfaceError as erlog:
                    self.all_log=erlog
                    self.interface_error_handle()
                    error_logging = open("/home/pi/Documents/CFM/security_tacking.txt", "a")
                    hour = time.strftime("%H")
                    minute = time.strftime("%M")
                    second = time.strftime("%S")
                    te = hour+':'+minute+':'+second
                    error_logging.write("{} {}, while updating M3 data {}\n".format(et,te,self.all_log))
                    error_logging.close()

    def graph_ploting(self):
        if (self.Y_graph_list != [] and self.X_graph_list != [] and len(self.Y_graph_list) > 1 and len(self.X_graph_list) > 1):
            self.trend_window = Toplevel(self.root, background="white")
            self.trend_window.title("Graphic View")
            self.trend_window.geometry("790x562+410+50")
            sig = mds.figure(figsize=(80, 6), dpi=100)
            ssubplot = sig.add_subplot(111)
            ssubplot.plot((self.X_graph_list), (self.Y_graph_list))
            danvas = FigureCanvasTkAgg(sig, master=self.trend_window)
            danvas.draw()
            danvas.get_tk_widget().pack()
            toolbar = NavigationToolbar2Tk(danvas, self.trend_window)
            toolbar.update()
            danvas.get_tk_widget().pack()
            mds.title("Transcation Trend info")
            mds.ylabel("Amount")
            mds.xlabel("Date")

    def Tool_settings(self):
        if self.tool_frame == False and self.adding_frame == False and self.removeuser_frame == False and self.changingpswd_frame == False:
            try:
                self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                self.datacursor = self.cat.cursor(buffered=True)
                self.tool_frame = True
                self.datacursor.execute("SELECT Tool_weight FROM tool_table")
                for_combobox = self.datacursor.fetchall()
                self.Frame_Tool_window = Frame(self.admin_window, bg="white")
                self.Frame_Tool_window.place(x=206, y=105, height=240, width=230)
                Tool_Range = Label(self.Frame_Tool_window,text="Tool\nRange",font=("Calibri", 11, "bold"),background="white",foreground="black",)
                Tool_Range.place(x=27, y=16)
                Tool_Weight = Label(self.Frame_Tool_window,text="Tool\nWeight",font=("Calibri", 11, "bold"),background="white",foreground="black",)
                Tool_Weight.place(x=92, y=16)
                Tool_10kg = Label(self.Frame_Tool_window,text="<10Kg",font=("Calibri", 10, "bold"),background="white",foreground="dark blue",)
                Tool_10kg.place(x=27, y=67)
                Tool_10kg_above = Label(self.Frame_Tool_window,text=">10Kg",font=("Calibri", 10, "bold"),background="white",foreground="dark blue",)
                Tool_10kg_above.place(x=27, y=107)
                Tool_25kg = Label(self.Frame_Tool_window,text=">25Kg",font=("Calibri", 10, "bold"),background="white",foreground="dark blue",)
                Tool_25kg.place(x=27, y=147)
                self.Tool_10kg_below_value_entry = Entry(self.Frame_Tool_window,font=("calibri", 10),background="#FFFF80",justify="center",)
                self.Tool_10kg_below_value_entry.place(x=93, y=66, height=30, width=60)
                self.Tool_10kg_below_value_entry.insert(0, for_combobox[0])
                self.Tool_10kg_above_value_entry = Entry(self.Frame_Tool_window,font=("calibri", 10),background="#FFFF80",justify="center",)
                self.Tool_10kg_above_value_entry.place(x=93, y=106, height=30, width=60)
                self.Tool_10kg_above_value_entry.insert(0, for_combobox[1])
                self.Tool_25kg_above_value_entry = Entry(self.Frame_Tool_window,font=("calibri", 10),background="#FFFF80",justify="center",)
                self.Tool_25kg_above_value_entry.place(x=93, y=146, height=30, width=60)
                self.Tool_25kg_above_value_entry.insert(0, for_combobox[2])
                close_btn = Button(
                    self.Frame_Tool_window,command=self.Tool_frame_close,cursor="hand2",text="Save & Close",background="white",bd=0,activebackground="white", highlightthickness =0,foreground="#d77337",font=("calibri", 11, "bold"),)
                close_btn.place(bordermode=OUTSIDE,x=116, y=195)
            except mysql.connector.errors.InterfaceError as erlog:
                self.all_log=erlog
                self.interface_error_handle()

    def adding_user(self):
        if self.tool_frame == False and self.adding_frame == False and self.removeuser_frame == False and self.changingpswd_frame == False:
            self.Frame_adduser_window = Frame(self.admin_window, bg="white")
            self.Frame_adduser_window.place(x=181, y=131, height=250, width=260)
            self.adding_frame = True
            user_login = Label(self.Frame_adduser_window,text="Enter New User\nCredentials:",font=("Calibri", 14),background="white",foreground="#d77337",).place(x=18, y=12)
            urname = Label(self.Frame_adduser_window,text="Name:",font=("Calibri", 10),background="white",foreground="dark blue",).place(x=8, y=72)
            self.adduser_uname = Entry(self.Frame_adduser_window,font=("calibri", 13),background="#FFFFC9",justify="center",)
            self.adduser_uname.place(x=61, y=70, height=26, width=130)
            self.adduser_uname.focus_set()
            pswd = Label(self.Frame_adduser_window,text="Passwd:",font=("Calibri", 10),background="white",foreground="dark blue",).place(x=8, y=112)
            self.adduser_pass = Entry(self.Frame_adduser_window,font=("calibri", 15),show="•",background="#FFFFC9",justify="center",)
            self.adduser_pass.insert(0, "Password")
            self.adduser_pass.config(state=DISABLED)
            self.adduser_pass.bind("<Button-1>", self.adduser_pass_click)
            self.adduser_pass.place(x=61, y=110, height=32, width=130)
            self.re_enter_pass = Entry(self.Frame_adduser_window,font=("calibri", 15),show="•",background="#FFFFC9",justify="center",)
            self.re_enter_pass.insert(0,"Password")
            self.re_enter_pass.config(state=DISABLED)
            self.re_enter_pass.bind("<Button-1>", self.re_enter_pass_click)
            self.re_enter_pass.place(x=61, y=150, height=26, width=130)
            repswd = Label(self.Frame_adduser_window,text="Passwd:",font=("Calibri", 10),background="white",foreground="dark blue",).place(x=2, y=152)
            Set_btn = Button(self.Frame_adduser_window,command=lambda: self.saving_user(),cursor="hand2",text="Save_User",
                background="#d77337",bd=0,activebackground="#d77337",foreground="white", highlightthickness =0,font=("calibri", 11, "bold"),relief=FLAT,)
            Set_btn.place(bordermode=OUTSIDE,x=40, y=205, width=85)
            cancel_btn = Button(self.Frame_adduser_window,command=self.cancel_admin_frame,cursor="hand2",text="Cancel",bd=0,activebackground="white",foreground="#d77337",
                background="white", highlightthickness =0,font=("calibri", 12, "bold"),relief=FLAT,)
            cancel_btn.place(bordermode=OUTSIDE,x=150, y=205)

    def removing_user(self):
        if self.tool_frame == False and self.adding_frame == False and self.removeuser_frame == False and self.changingpswd_frame == False:
            self.Frame_removeuser_window = Frame(self.admin_window, bg="white")
            self.Frame_removeuser_window.place(x=211, y=176, height=160, width=200)
            self.removeuser_frame = True
            remove_label = Label(self.Frame_removeuser_window,text="Select User:",font=("Calibri", 14),
                background="white",foreground="#d77337",).place(x=15, y=15)
            self.remove_user = ttk.Combobox(self.Frame_removeuser_window,font=("calibri", 13),state="readonly",justify=CENTER,)
            self.remove_user["values"] = ("User name",)
            try:
                self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                self.datacursor = self.cat.cursor(buffered=True)
                self.datacursor.execute("SELECT User_name FROM user_details")
                for_combobox = self.datacursor.fetchall()
                for moveinto in for_combobox:
                    self.remove_user["values"] = self.remove_user["values"] + (moveinto,)
            except mysql.connector.errors.InterfaceError as erlog:
                self.all_log=erlog
                self.interface_error_handle()
            self.remove_user.place(x=20, y=60, height=26, width=130)
            self.remove_user.current(0)
            Remove_btn = Button(self.Frame_removeuser_window,command=self.selected_to_remove,cursor="hand2",text="Remove",background="#d77337",bd=0,
                foreground="white", highlightthickness =0,activebackground = "#d77337",font=("calibri", 10, "bold"),relief=FLAT,)
            Remove_btn.place(bordermode=OUTSIDE,x=30, y=115, width=60)
            cancel_btn = Button(self.Frame_removeuser_window,command=self.cancel_admin_frame,cursor="hand2",text="Cancel",bd=0,
                foreground="#d77337",background="white", highlightthickness =0,activebackground="white",font=("calibri", 11, "bold"),relief=FLAT,)
            cancel_btn.place(bordermode=OUTSIDE,x=112, y=115)
    
    def changing_pswd(self):
        if self.tool_frame == False and self.adding_frame == False and self.removeuser_frame == False and self.changingpswd_frame == False:
            self.Frame_changepswd_window = Frame(self.admin_window, bg="white")
            self.Frame_changepswd_window.place(x=120, y=108, height=230, width=220)
            self.changingpswd_frame = True
            changepswd_label = Label(self.Frame_changepswd_window,text="Select User:",font=("Calibri", 14),background="white",foreground="#d77337",).place(x=18, y=13)
            self.changepswd_user = ttk.Combobox(self.Frame_changepswd_window,font=("calibri", 12),state="readonly",justify=CENTER,)
            self.changepswd_user["values"] = ("User name",)
            try:
                self.cat = mysql.connector.connect(host=self.Address["Database_address"],user="subramanya_m_s",passwd="Lakshmi9611",database="CFM",)
                if self.cat:
                    self.datacursor = self.cat.cursor(buffered=True)
                    self.datacursor.execute("SELECT User_name FROM user_details")
                    for_combobox = self.datacursor.fetchall()
                    for moveinto in for_combobox:
                        self.changepswd_user["values"] = self.changepswd_user["values"] + (moveinto,)
            except mysql.connector.errors.InterfaceError as erlog:
                self.all_log=erlog
                self.interface_error_handle()
            self.changepswd_user.place(x=35, y=50, height=26, width=130)
            self.changepswd_user.current(0)
            self.new_pass = Entry(self.Frame_changepswd_window,font=("calibri", 15),show="•",background="#FFFFC9",justify="center",)
            self.new_pass.insert(0, "Password")
            self.new_pass.config(state=DISABLED)
            self.new_pass.bind("<Button-1>", self.new_pass_click)
            self.new_pass.place(x=35, y=90, height=26, width=130)
            self.re_new_pass = Entry(self.Frame_changepswd_window,font=("calibri", 15),show="•",background="#FFFFC9",justify="center",)
            self.re_new_pass.insert(0, "Password")
            self.re_new_pass.config(state=DISABLED)
            self.re_new_pass.bind("<Button-1>", self.re_new_pass_click)
            self.re_new_pass.place(x=35, y=130, height=26, width=130)
            self.re_new_pass.bind("<Return>", lambda event=None: confirm_btn.invoke())
            confirm_btn = Button(self.Frame_changepswd_window,command=lambda: self.selected_changepswd(),cursor="hand2",text="Confirm",activebackground="#d77337",background="#d77337",bd=0,
                foreground="white", highlightthickness =0,font=("calibri", 11, "bold"),relief=FLAT,)
            confirm_btn.place(bordermode=OUTSIDE,x=30, y=185)
            cancel_btn = Button(self.Frame_changepswd_window,command=self.cancel_admin_frame,cursor="hand2",
                text="Cancel",bd=0, highlightthickness =0,foreground="#d77337",background="white",activebackground="white",font=("calibri", 11, "bold"),relief=FLAT,)
            cancel_btn.place(bordermode=OUTSIDE,x=110, y=185)
    
                # ********************saving into database********************
    
    def weight_window(self):
        Weight = Label(root,text="Weight",font=("Calibri", 13, "bold"),foreground="dark blue",background="white")
        Weight.place(x=645, y=20)
        self.display = Text(master=root, height=2, width=10, font=("Helvetica", 10), background="#FFFFC9",wrap=WORD)
        self.display.place(x=640, y=64)
        self.Set = Button(root,command=self.contact_entry_fun,cursor="hand2",text="Set <F10>",background="#d77337",
            bd=0, highlightthickness =0,activebackground = "#d77337",foreground="white",font=("calibri",12,"bold",),relief=SUNKEN,)
        self.Set.place(bordermode=OUTSIDE,x=1040, y=136, width=80)
        self.Set.bind("<Return>", lambda event: self.contact_entry_fun())     
        root.bind("<F10>",self.parallel_contact_entry_fun)# set_torun_window
        self.display.insert(0.0, self.uname)
        self.display.tag_add("center", "1.0", "end")
        Item = Label(root,text="Item   \nSelected",font=("Calibri", 10, "bold"),foreground="dark blue",background="white")
        Item.place(x=749, y=16)
        self.Item_display = Text(master=root, height=2, width=10, font=("Helvetica", 10), background="#FFFFC9", wrap=WORD)
        self.Item_display.tag_configure("center", justify="center")
        self.Item_display.place(x=740, y=64)
        Price = Label(root,text="Rate:",font=("Calibri", 13, "bold"),foreground="dark blue",background="white")
        Price.place(x=871, y=37)
        self.Price_display = Text(master=root, height=1, width=7, font=("Helvetica", 14), background="#FFFFC9", wrap=WORD)
        self.Price_display.tag_configure("center", justify="center")
        self.Price_display.place(x=930, y=34)
        Discount = Label(root,text="Discount:",font=("Calibri", 13, "bold"),foreground="dark blue",background="white")
        Discount.place(x=849, y=85)
        self.Dis_display = Text(master=root, height=1, width=7, font=("Helvetica", 14), background="#FFFFC9", wrap=WORD)
        self.Dis_display.tag_configure("center", justify="center")
        self.Dis_display.place(x=930, y=85)
        Amount = Label(root,text="Total:",font=("Calibri", 13, "bold"),foreground="dark blue",background="white")
        Amount.place(x=873, y=136)
        self.AM_display = Text(master=root, height=1, width=7, font=("Helvetica", 14), background="#FFFFC9", wrap=WORD)
        self.AM_display.tag_configure("center", justify="center")
        self.AM_display.place(x=930, y=134)
        self.Select_tool_btn= Button(root,command=self.selecting_tool,cursor="hand2",text="Select_Tool",background="#d77337",activebackground="#d77337",
            bd=0, highlightthickness =0,foreground="white",font=("calibri",12,"bold",),relief=SUNKEN,)
        self.Select_tool_btn.place(bordermode=OUTSIDE,x=990, y=195, width=90)
        
    def selecting_tool(self):
        if self.Select_tool_btn.winfo_exists() == 1:
            self.Select_tool_btn.destroy()
        elif self.Change_tool_btn.winfo_exists() == 1:
            self.Change_tool_btn.destroy()
        if self.weighing_tool != "Select_Tool":
            self.weighing_tool = "Select_Tool"
        self.common_item = ""
        self.Item_display.delete(0.0, END)
        self.Price_display.delete(0.0, END)
        self.Dis_display.delete(0.0, END)
        self.AM_display.delete(0.0, END)
        self.Set_tool_btn = Button(root,command=self.setting_tool,cursor="hand2",text="Set_Tool",background="#d77337",activebackground="#d77337",
            bd=0, highlightthickness =0,foreground="white",font=("calibri",12,"bold",),relief=SUNKEN,)
        self.Set_tool_btn.place(bordermode=OUTSIDE,x=990, y=195, width=90)
        self.Tool_label = Label(root, text="Tool:", font=("Calibri", 12, "bold"), foreground="dark blue",background="white")
        self.Tool_label.place(x=940, y=237)
        self.Select_tool = ttk.Combobox(root,font=("calibri", 10),state="readonly",justify=CENTER,)
        self.Select_tool["values"] = ("Select_Tool","No Tool","10Kg","10Kg+","25Kg+",)
        self.Select_tool.place(x=980, y=235, height=25, width=100)
        self.Select_tool.current(0)
        
    def setting_tool(self):
        if self.Select_tool.get() != "Select_Tool":
            self.weighing_tool=self.Select_tool.get()
            self.Process = "Continue"
            self.Set_tool_btn.destroy()
            self.Tool_label.destroy()
            self.Select_tool.destroy()
            self.Change_tool_btn = Button(root,command=self.selecting_tool,cursor="hand2",background="#d77337",activebackground="#d77337",
            bd=0, highlightthickness =0,foreground="white",font=("calibri",12,"bold",),relief=SUNKEN,)
            self.Change_tool_btn.place(bordermode=OUTSIDE,x=990, y=195, width=90)
            self.Change_tool_btn.config(text=self.weighing_tool)
            self.to_place_inform_display()
            if self.weighing_tool == "No Tool":
                self.info_display.insert(0.0, "info:\n %s selected for weighing..."%(self.weighing_tool))
            elif self.weighing_tool != "No Tool":
                self.info_display.insert(0.0, "info:\n %s Tool selected for weighing..."%(self.weighing_tool))
        else:
            self.to_place_error_display()
            self.error_display.insert(0.0, "Error:\n Weighing tool not selected...!\n Please click 'Select_Tool' button")
            
    def on_settings_close_icon(self):
        icon_press = messagebox.askokcancel("Quit", "Do you want to close?")
        if icon_press > 0:
            self.admin_window.destroy()

    def on_TDT_close_icon(self):
        icon_press = messagebox.askokcancel("Quit", "Do you want to close?")
        if icon_press > 0:
            self.tally_window.destroy()
            self.TDT = False

        # **************If login is successful will open this window**************#

    def success_login(self):        
        self.tokenno = None
        self.no_internet_token = 1
        self.selection = None  # initializing this variable, further it's used to check selection window exists or not
        self.M1_Sl_no = int  # initializing sl_no variable to avoid errors
        self.M2_Sl_no = int  # initializing sl_no variable to avoid errors
        self.M3_Sl_no = int  # initializing sl_no variable to avoid errors
        self.M1_Token_no = int
        self.M2_Token_no = int
        self.M3_Token_no = int
        self.Machine_name = ""
        self.Rice_data = "Rice"  # variable for updating database and comparision of treeview data        
        self.Wheat_data = "Wheat"  # variable for updating database and comparision of treeview data        
        self.Chickpea_data = "Chickpea"  # variable for updating database and comparision of treeview data
        self.Ragi_data = "Ragi"  # variable for updating database and comparision of treeview data
        self.Chilli_data = "Chilli"  # variable for updating database and comparision of treeview data        
        self.Dhaniya_data = "Dhaniya"  # variable for updating database and comparision of treeview data        
        self.rice_flashing = False  # variable to handle rice btn flash function
        self.wheat_flashing = False  # variable to handle wheat btn flash function
        self.chickpea_flashing = False  # variable to handle chickpea btn flash function
        self.ragi_flashing = False  # variable to handle ragi btn flash function
        self.chilli_flashing = False  # variable to handle chilli btn flash function
        self.dhaniya_flashing = False  # variable to handle dhaniya btn flash function
        self.common_item = ""  # variable to store item selected by user before set to run        
        self.weight = 15.2  # variable to store weight read from scale
        self.discount = float  # initializing discount variable to avoid errors
        self.Amount = float  # initializing amount variable to avoid errors
        self.pgm_opened = True  # initializing programopened status variable to avoid errors
        self.log_flash = True
        self.TDT = False  # initializing track daily transaction variable to avoid errors
        self.flashdelay = 500  # msec between colour change
        self.flash_colour = ("white", "black")  # Two colours to swap between
        self.temp_disc= 0
        self.weighing_tool="Select_Tool"
        self.Process = ""
        self.after_login = Frame(self.root).place(x=0, y=0, height=550, width=1200)
        self.nextbg_image = Label(self.root, image=self.bg, background="white").place(x=0, y=0, relwidth=1, relheight=1)
        self.weight_window()        
        corner_name = Label(self.after_login,text=self.Uname,font=("Calibri", 15, "bold"),background="white",)
        corner_name.place(x=13, y=8)
        Machine_1 = Label(self.after_login,text="F Mc_1",font=("Calibri", 19, "bold"),foreground="dark blue",background="white",)
        Machine_1.place(x=20, y=60)
        Machine_2 = Label(self.after_login,text="F Mc_2",font=("Calibri", 19, "bold"),foreground="dark blue",background="white",)
        Machine_2.place(x=20, y=125)
        Machine_3 = Label(self.after_login,text="F Mc_3",font=("Calibri", 19, "bold"),foreground="dark blue",background="white",)
        Machine_3.place(x=20, y=190)        
        self.Rice_btn = Button(self.after_login,command=self.rice_fun,cursor="hand2",
            text=f"Rice <F1>",background="#d77337",bd=0,highlightthickness =0,activebackground="#d77337",foreground=self.flash_colours[0],font=("calibri",14,"bold",),relief=SUNKEN)
        self.Rice_btn.place(bordermode=OUTSIDE,x=140, y=60, width=100)
        root.bind("<F1>",self.parallel_rice_fun)
        self.Wheat_btn = Button(self.after_login,command=self.wheat_fun,cursor="hand2",text="Wheat <F2>",background="#d77337",bd=0,activebackground="#d77337", highlightthickness =0,
            foreground=self.flash_colours[0],font=("calibri",14,"bold",),relief=SUNKEN,)
        self.Wheat_btn.place(bordermode=OUTSIDE,x=270, y=60, width=110)
        root.bind("<F2>",self.parallel_wheat_fun)
        self.Chickpea_btn = Button(self.after_login,command=self.chickpea_fun,cursor="hand2",text="Chickpea <F3>",background="#d77337",bd=0,activebackground="#d77337", highlightthickness=0,
            foreground=self.flash_colours[0],font=("calibri",14,"bold",),relief=SUNKEN,)
        self.Chickpea_btn.place(bordermode=OUTSIDE,x=410, y=60, width=118)
        root.bind("<F3>",self.parallel_chickpea_fun)
        self.Ragi_btn = Button(self.after_login,command=self.ragi_fun,cursor="hand2",text="Ragi <F4>",background="#d77337",activebackground="#d77337",
            bd=0,highlightthickness =0,foreground=self.flash_colours[0],font=("calibri",14,"bold",),relief=SUNKEN,)
        self.Ragi_btn.place(bordermode=OUTSIDE, x=140, y=125, width=100)
        root.bind("<F4>",self.parallel_ragi_fun)
        self.Chilli_btn = Button(self.after_login,command=self.chilli_fun,
            cursor="hand2",text="Chilli <F5>",background="#d77337",bd=0,highlightthickness=0,activebackground="#d77337",foreground=self.flash_colours[0],font=("calibri",14,"bold",),relief=SUNKEN,)
        self.Chilli_btn.place(bordermode=OUTSIDE, x=140, y=190, width=100)
        root.bind("<F5>",self.parallel_chilli_fun)
        self.Dhaniya_btn = Button(self.after_login,command=self.dhaniya_fun,cursor="hand2",text="Dhaniya <F6>",background="#d77337",activebackground="#d77337",
            bd=0,highlightthickness =0,foreground=self.flash_colours[0],font=("calibri",14,"bold",),relief=SUNKEN,)
        self.Dhaniya_btn.place(bordermode=OUTSIDE, x=270, y=190, width=110)
        root.bind("<F6>",self.parallel_dhaniya_fun)
        # check_weight = Button(root,command=self.add_to_table,
        #     cursor="hand2",text="Check \n weight",background="#d77337",bd=0,highlightthickness=0,activebackground="#d77337",foreground="white",font=("calibri",14,"bold",),relief=SUNKEN,)
        # check_weight.place(bordermode=OUTSIDE, x=635, y=111, width=85)
        self.inform_func()
        check_internet_btn = Button(self.after_login,command=self.update_txt,cursor="hand2",text="|Check Internet Speed|",activebackground="white",
            bd=0, highlightthickness =0,foreground="#d77337",background="white",font=("calibri", 13),relief=FLAT,)
        check_internet_btn.place(bordermode=OUTSIDE,x=30, y=380)
        io_btn = Button(self.after_login, command=self.input_output_status_window,cursor="hand2",text="|I/O Status|",activebackground="white",
            bd=0, highlightthickness =0,foreground="#d77337",background="white",font=("calibri", 13),relief=FLAT,)
        io_btn.place(bordermode=OUTSIDE,x=30, y=415)
        Manual_btn = Button(self.after_login,command=self.manual_fun,
            cursor="hand2",text="Manual run",background="#d77337",bd=0,highlightthickness =0,activebackground="#d77337",foreground=self.flash_colours[0],font=("calibri",12,"bold",),relief=SUNKEN,)
        Manual_btn.place(bordermode=OUTSIDE, x=35, y=460, width=90)
        Settings_btn = Button(self.after_login,command=self.admin_fun,cursor="hand2",text="Settings",background="#d77337",activebackground="#d77337",
            bd=0,highlightthickness =0,foreground=self.flash_colours[0],font=("calibri",12,"bold",),relief=SUNKEN,)
        Settings_btn.place(bordermode=OUTSIDE, x=35, y=510, width=90)
        Tally_btn = Button(self.after_login,command=self.tally_mysql,cursor="hand2",text="TDT",background="#d77337",bd=0,activebackground="#d77337",highlightthickness =0,
            foreground=self.flash_colours[0],font=("calibri",12,"bold",),relief=SUNKEN,)
        Tally_btn.place(bordermode=OUTSIDE, x=35, y=560, width=90)
        self.trial_clock = Label(root, text="", font=("calibri", 17, "bold"),background="white")
        self.trial_clock.place(x=25, y=620)
        self.clock()  # calling digi clock function into user window
        self.Manual_Frame_window = Frame(self.root)
        self.Manual_Frame_window.destroy()
        self.input_output_Frame_window = Frame(self.root)
        self.input_output_Frame_window.destroy()
        self.contact_window =Frame(self.root)
        self.contact_window.destroy()
        self.admin_window = Toplevel(self.root)
        self.admin_window.destroy()
        # *************Fetching parameters from database****************
        sqt = "SELECT * from price_list"
        self.datacursor.execute(sqt)
        jdata = self.datacursor.fetchmany(1)
        for row in jdata:
            self.Chickpea_time = row[2]
            self.Chickpea_time = self.Chickpea_time * 1000  # converting sec into milisec
            self.Chickpea_disc_after__kg = row[3]
            self.Chickpea_price = row[4]
            self.Chickpea_disc_value = row[5]
            self.Chickpea_max_disc = row[6]
        jdata = self.datacursor.fetchmany(1)
        for row in jdata:
            self.Rice_time = row[2]
            self.Rice_time = self.Rice_time * 1000  # converting sec into milisec
            self.Rice_disc_after__kg = row[3]
            self.Rice_price = row[4]
            self.Rice_disc_value = row[5]
            self.Rice_max_disc = row[6]
        jdata = self.datacursor.fetchmany(1)
        for row in jdata:
            self.Wheat_time = row[2]
            self.Wheat_time = self.Wheat_time * 1000  # converting sec into milisec
            self.Wheat_disc_after__kg = row[3]
            self.Wheat_price = row[4]
            self.Wheat_disc_value = row[5]
            self.Wheat_max_disc = row[6]
        jdata = self.datacursor.fetchmany(1)
        for row in jdata:
            self.Ragi_time = row[2]
            self.Ragi_time = self.Ragi_time * 1000  # converting sec into milisec
            self.Ragi_disc_after__kg = row[3]
            self.Ragi_price = row[4]
            self.Ragi_disc_value = row[5]
            self.Ragi_max_disc = row[6]
        jdata = self.datacursor.fetchmany(1)
        for row in jdata:
            self.Chilli_time = row[2]
            self.Chilli_time = self.Chilli_time * 1000  # converting sec into milisec            
            self.Chilli_disc_after__kg = row[3]
            self.Chilli_price = row[4]
            self.Chilli_disc_value = row[5]
            self.Chilli_max_disc = row[6]
        jdata = self.datacursor.fetchmany(1)
        for row in jdata:
            self.Dhaniya_time = row[2]
            self.Dhaniya_time = self.Dhaniya_time * 1000  # converting sec into milisec            
            self.Dhaniya_disc_after__kg = row[3]
            self.Dhaniya_price = row[4]
            self.Dhaniya_disc_value = row[5]
            self.Dhaniya_max_disc = row[6]
        # ***********Opens Selection window*************
        self.select_to_run()
        self.error_func()
        self.error_display.destroy()
        self.datacursor.execute("select * from {today} order by Sl_no DESC LIMIT 3".format(today= 'transaction_data'))
        recheck_run= self.datacursor.fetchall()
        for incomplete in recheck_run:
            tmp_date = str(incomplete[2])
            if tmp_date == et:
                print("hahaha")
                if incomplete[5] == ('Rice' or 'Wheat' or 'Chickpea') and incomplete[4] == None:
                    self.M1_Sl_no = incomplete[0]
                    if incomplete[5] == 'Rice':
                        self.RiceCallback()
                    elif incomplete[5] == 'Wheat':
                        self.WheatCallback()
                    elif incomplete[5] == 'Chickpea':
                        self.ChickpeaCallback()
                    GPIO.output(self.m1_start_P,GPIO.LOW)
                    #root.after(1000, self.stop_M1_Rice_blink)
                    time.sleep(0.5)
                    self.select_treeview.insert("","end",iid=self.tokenno,
                            values=(incomplete[1],incomplete[5],"F Mc_1","Restarted..",incomplete[6],incomplete[9],incomplete[7],incomplete[8],),)
                    self.M1_drop_no = [incomplete[1],incomplete[5],"F Mc_1","Restarted..",incomplete[6],incomplete[9],incomplete[7],incomplete[8],]
                    GPIO.output(self.m1_start_P,GPIO.HIGH)
                    self.M1_status = "Busy"
                elif incomplete[5] == "Ragi" and incomplete[4] == None:
                    self.M2_Sl_no = incomplete[0]
                    self.RagiCallback()
                    GPIO.output(self.m2_start_P,GPIO.LOW)
                    #root.after(1000, self.stop_M1_Rice_blink)
                    time.sleep(0.5)
                    self.select_treeview.insert("","end",iid=self.tokenno,
                            values=(incomplete[1],incomplete[5],"F Mc_2","Restarted..",incomplete[6],incomplete[9],incomplete[7],incomplete[8],),)
                    self.M2_drop_no = [incomplete[1],incomplete[5],"F Mc_1","Restarted..",incomplete[6],incomplete[9],incomplete[7],incomplete[8],]
                    GPIO.output(self.m2_start_P,GPIO.HIGH)
                    self.M12status = "Busy"
                elif incomplete[5] == ("Chilli" or "Dhaniya") and incomplete[4] == None:
                    self.M3_Sl_no = incomplete[0]
                    if incomplete[5] == 'Chilli':
                        self.ChilliCallback()
                    elif incomplete[5] == 'Dhaniya':
                        self.DhaniyaCallback()
                    GPIO.output(self.m3_start_P,GPIO.LOW)
                    #root.after(1000, self.stop_M1_Rice_blink)
                    time.sleep(0.5)
                    self.select_treeview.insert("","end",iid=self.tokenno,
                            values=(incomplete[1],incomplete[5],"F Mc_3","Restarted..",incomplete[6],incomplete[9],incomplete[7],incomplete[8],),)
                    self.M3_drop_no = [incomplete[1],incomplete[5],"F Mc_1","Restarted..",incomplete[6],incomplete[9],incomplete[7],incomplete[8],]
                    GPIO.output(self.m3_start_P,GPIO.HIGH)
                    self.M3_status = "Busy"
            
obj = Login(root)
root.mainloop()
