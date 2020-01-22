

"""This program will use paramiko to copy a file from a local server to a remote server"""

import paramiko
import os



ssh_client = paramiko.SSHClient()
hostname = 'tim-mcc-centos.lab.plexxi.com'
PASS = 'plexxi100'
USER = 'plexxi'

def printTotals(transferred, toBeTransferred):
    print "Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred)

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname= hostname, username=USER, password=PASS)
ftp_client = ssh_client.open_sftp()
ftp_client.put('/tmp/test.txt', '/tmp/b4_switch1.pcap', callback=printTotals)









