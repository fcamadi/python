#!/usr/bin/python3

#
# Genesys test exercise - March 2015 - Francisco Camacho
# Version: 2.0
#     Added exceptions, and sending of email 
#

import smtplib
import os
import sys
import time
import base64

#
# constants
#
files_path_linux="/home/fran/genesys/"
files_path_windows="D:/genesys/"

#
# auxiliary functions
#
def path_separator():
# not needed now
    if os.name=="nt":
        return "\\"
    else:
        return "/"
    
def path_of_files():
    if os.name=="nt":
        return files_path_windows
    else:
        return files_path_linux

def current_date():
    return time.strftime("%d/%m/%Y")

def compare_simple_dates(date1,date2):
    try:
        first_date=date1.split("/")
        d1=first_date[0]
        m1=first_date[1]
        second_date=date2.split("/")
        d2=second_date[0]
        m2=second_date[1]
    except IndexError:
        sys.stdout.write("Error in date!\n")
        return False
    return d1==d2 and m1==m2

def calculate_age(date):
    info = date.split("/")
    current_year=time.strftime("%Y")
    age = int(current_year) - int(info[2])
    # sys.stdout.write("calculate_age - age: "+str(age)+"\n")
    return str(age)
      
def read_login_and_pass():
    diccio_login = {}
    
    try:
        login_file = open(path_of_files()+"login.txt","r")
    except (OSError, IOError):
        sys.stdout.write("Login.txt not found!\n")
        # exit()        
        return None
    
    lines = login_file.read().split("\n")
    
    if  os.name=="nt":
        if len(lines)!=6:
            sys.stdout.write("Login file not correct!\n")
            # exit()
            return None
    else:
        if len(lines)!=7:
            sys.stdout.write("Login file not correct!\n")
            # exit()
            return None
     
    diccio_login["server"]=lines[0]
    diccio_login["port"]=lines[1]
    diccio_login["login"]=lines[2]      
    diccio_login["password"]=lines[3]   # "encrypted" in the file (simply encoded ...)
    diccio_login["from"]=lines[4]
    diccio_login["to"]=lines[5]         # at the moment only one receiver (yourself!)
        
    return diccio_login
 
     
def send_email(from_addr, to_addr_list, cc_addr_list,subject, message, 
	login, password, smtpserver='smtp.gmail.com:587'):

    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % to_addr_list
    header += 'Cc: %s\n' % cc_addr_list
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems


#
# previous reminder.py
#
def reminder_message():
    """ function that generates the content of the email """

    msg = "Today is "+current_date()+"\n\n"

    try:
        people_file = open(path_of_files()+"people.txt","r")
    except (OSError, IOError):
        sys.stdout.write("People.txt not found!")
        exit()

    lines = people_file.read().split("\n")
    cumpleanyero = []  # (spanish word for a person who has birthday :)
    cumpleanyero_phone = []
    cumpleanyero_age = []

    for line in lines:
        if not line:
            continue
        data=line.split(",")
        try:
            if compare_simple_dates(data[2],current_date()):
                cumpleanyero.append(data[0])
                cumpleanyero_phone.append(data[1])
                cumpleanyero_age.append(calculate_age(data[2]))
        except IndexError:
            sys.stdout.write("Error in user data!\n")
                
    people_file.close() 

    if (len(cumpleanyero)==0):
        msg += " Today is nobody's birthday! No cake, sorry! \n\n"
    else:
        msg += "Today is the birthday of: \n\n"
        for i, friend in enumerate(cumpleanyero):
            msg += friend+"!("+cumpleanyero_age[i]+") - Phone number: "+cumpleanyero_phone[i]+"\n"
        msg += "\nCall your friend/s! They will be very happy! \n\n"

    return msg


def main():
    
    info_email=read_login_and_pass()
    
    if not info_email:
        sys.stdout.write("No info! Not possible to send reminder email!\n")
    else:    
        subject = "Birthday reminder (v2)"    
        msg = reminder_message()   # here the call to the reminder() function
        problems = send_email(info_email["from"],info_email["to"],"",
        	subject,msg,info_email["login"],
        	info_email["password"],info_email["server"]+":"+info_email["port"])
        # passw = str(base64.b64decode(info_email["password"]))[2:-1]
        # problems = send_email(info_email["from"],info_email["to"],"",
        #        subject,msg,info_email["login"],passw,
        #        info_email["server"]+":"+info_email["port"])
        if not problems:
            sys.stdout.write("Birthday reminder mail was sent with no problem :)\n")
        else:
            sys.stdout.write("There were problems sending the birthday reminder email!\n")
            
main()    
