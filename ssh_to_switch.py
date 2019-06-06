
#!/usr/bin/python

#Importing modules
import paramiko
import sys
import time



#setting parameters like host IP, username, passwd and number of iterations to gather cmds
HOST = "192.168.104.10"
USER = "admin"
PASS = "plexxi"



#A function that logins and execute commands
def ssh_fn():
  client1=paramiko.SSHClient()
  #Add missing client key
  client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  #connect to switch
  client1.connect(HOST,username=USER,password=PASS)
  print "SSH connection to %s established" %HOST
  #Gather commands and read the output from stdout
  stdin, stdout, stderr = client1.exec_command('/opt/plexxi/bin/fabricInfo\n')
  fabric = stdout.read()
  print fabric
  master = fabric.index('Master')
  print (fabric[master: master + 39])
  client1.close()
  print "Logged out of device %s" % HOST




if __name__ == '__main__':
print "About to call function to ssh in"
ssh_fn()

