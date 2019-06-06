
#!/usr/bin/python

#Importing modules
import paramiko
import sys
import time



#setting parameters like host IP, username, passwd and number of iterations to gather cmds
#HOST = "18.85.7.24"
USER = "admin"
PASS = *****************add the default password in here

#list of ip address

list1 = ['18.85.7.234', '18.85.7.23', '18.85.7.24','18.85.7.25', '18.85.7.26']


#A function that logins and execute commands
def ssh_fn():
  client1=paramiko.SSHClient()
  #Add missing client key
  client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  #connect to switch
  client1.connect(HOST,username=USER,password=PASS)
  print "SSH connection to %s established" %HOST
  #Gather commands and read the output from stdout
  stdin, stdout, stderr = client1.exec_command('/usr/bin/free -m\n')
  freemem = stdout.read()
  #print freemem
  memavailable = freemem.index('Mem:')
  lastline = (freemem[memavailable: memavailable + 45])
  total_left = (lastline[36:40])
  print ("FREE left on %s is"  % HOST)
  result =  (int(total_left) / 3463.0) * 100 
  print "%i Percent Free" % result 
  client1.close()
  
  #print "Logged out of device %s" % HOST 
  print "\n"

if __name__ == '__main__':
  for HOST in list1:
   # print "About to call function to ssh %s" %HOST
    ssh_fn()

